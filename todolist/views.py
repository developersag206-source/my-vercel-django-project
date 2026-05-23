from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm
from .models import CustomerOrder, OrderItem, Product


CART_SESSION_KEY = "clinic_cart"

TREATMENT_PROGRAMS = [
    {
        "name": "Digestive Balance Care",
        "summary": "Gentle herbal support plans for acidity, bloating, appetite, and daily digestive comfort.",
        "focus": "Digestive wellness",
    },
    {
        "name": "Joint Relief Therapy",
        "summary": "Natural oils, massage blends, and supportive care for stiffness, fatigue, and body aches.",
        "focus": "Pain management",
    },
    {
        "name": "Women's Wellness Support",
        "summary": "Balanced natural care with private consultation guidance and home-delivery products.",
        "focus": "Hormonal health",
    },
    {
        "name": "Immunity & Seasonal Defense",
        "summary": "Herbal tonics and clinic-selected remedies for stronger daily resilience and recovery.",
        "focus": "Immunity support",
    },
]


def _get_cart(request):
    return request.session.setdefault(CART_SESSION_KEY, {})


def _cart_items(request):
    cart = _get_cart(request)
    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)

    items = []
    total = Decimal("0.00")
    for product in products:
        quantity = cart.get(str(product.id), 0)
        if quantity <= 0:
            continue
        line_total = product.price * quantity
        total += line_total
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "line_total": line_total,
            }
        )
    return items, total


def homepage(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:3]
    latest_products = Product.objects.filter(is_active=True)[:6]
    product_count = Product.objects.filter(is_active=True).count()
    context = {
        "featured_products": featured_products,
        "latest_products": latest_products,
        "treatment_programs": TREATMENT_PROGRAMS[:3],
        "product_count": product_count,
        "cart_count": sum(_get_cart(request).values()),
    }
    return render(request, "home.html", context)


def product_list(request):
    selected_category = request.GET.get("category", "").strip()
    products = Product.objects.filter(is_active=True)
    if selected_category:
        products = products.filter(category__iexact=selected_category)

    categories = (
        Product.objects.filter(is_active=True)
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    context = {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
        "cart_count": sum(_get_cart(request).values()),
    }
    return render(request, "product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        is_active=True, category=product.category
    ).exclude(id=product.id)[:3]
    context = {
        "product": product,
        "related_products": related_products,
        "cart_count": sum(_get_cart(request).values()),
    }
    return render(request, "product_detail.html", context)


def add_to_cart(request, product_id):
    if request.method != "POST":
        raise Http404()

    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request)
    current_quantity = cart.get(str(product.id), 0)
    if current_quantity >= product.stock:
        messages.error(request, "Requested quantity is not available in stock.")
    else:
        cart[str(product.id)] = current_quantity + 1
        request.session.modified = True
        messages.success(request, f"{product.name} added to your cart.")

    next_url = request.POST.get("next_url") or "product_list"
    if next_url.startswith("/"):
        return redirect(next_url)
    return redirect(next_url)


def cart_view(request):
    items, cart_total = _cart_items(request)
    context = {
        "items": items,
        "cart_total": cart_total,
        "cart_count": sum(_get_cart(request).values()),
    }
    return render(request, "cart.html", context)


def update_cart(request, product_id):
    if request.method != "POST":
        raise Http404()

    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect("cart")

    if quantity <= 0:
        cart.pop(str(product.id), None)
        messages.success(request, f"{product.name} removed from your cart.")
    else:
        cart[str(product.id)] = min(quantity, product.stock)
        if quantity > product.stock:
            messages.warning(request, f"Only {product.stock} units are available.")
        else:
            messages.success(request, f"{product.name} quantity updated.")

    request.session.modified = True
    return redirect("cart")


@transaction.atomic
def checkout(request):
    items, cart_total = _cart_items(request)
    if not items:
        messages.info(request, "Your cart is empty. Add some products first.")
        return redirect("product_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = CustomerOrder.objects.create(**form.cleaned_data)
            for item in items:
                product = item["product"]
                quantity = item["quantity"]
                if quantity > product.stock:
                    messages.error(
                        request,
                        f"{product.name} no longer has enough stock for this order.",
                    )
                    return redirect("cart")
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                )
                product.stock -= quantity
                product.save(update_fields=["stock"])

            request.session[CART_SESSION_KEY] = {}
            request.session.modified = True
            messages.success(
                request,
                f"Thank you, {order.customer_name}. Your order has been placed successfully.",
            )
            return redirect("homepage")
    else:
        form = CheckoutForm()

    context = {
        "form": form,
        "items": items,
        "cart_total": cart_total,
        "cart_count": sum(_get_cart(request).values()),
    }
    return render(request, "checkout.html", context)


def treatments(request):
    context = {
        "programs": TREATMENT_PROGRAMS,
        "cart_count": sum(_get_cart(request).values()),
    }
    return render(request, "treatments.html", context)


def about(request):
    context = {
        "cart_count": sum(_get_cart(request).values()),
    }
    return render(request, "about.html", context)


def contact(request):
    context = {
        "cart_count": sum(_get_cart(request).values()),
    }
    return render(request, "contact.html", context)
