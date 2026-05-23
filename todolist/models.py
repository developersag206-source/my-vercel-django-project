from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class SiteContent(models.Model):
    site_name = models.CharField(max_length=150, default="Natural Medical Clinic")
    site_tagline = models.CharField(
        max_length=200, default="Natural healing, herbal remedies, and trusted family care"
    )
    footer_text = models.TextField(
        default=(
            "Natural Medical Clinic offers herbal support, guided wellness care, "
            "and an easy order process for trusted home delivery."
        )
    )
    about_badge = models.CharField(
        max_length=120, default="About Natural Medical Clinic"
    )
    about_heading = models.CharField(
        max_length=200,
        default="A calm, trusted clinic experience built around natural medicine.",
    )
    about_description = models.TextField(
        default=(
            "Natural Medical Clinic supports families with herbal remedies, "
            "wellness products, and practical care guidance. Patients can explore "
            "recommended items, review details, and place orders online with ease."
        )
    )
    vision_title = models.CharField(max_length=120, default="Our Vision")
    vision_text = models.TextField(
        default="Make reliable natural medicine and guided wellness care easier to access."
    )
    offerings_title = models.CharField(max_length=120, default="What We Offer")
    offerings_text = models.TextField(
        default=(
            "Herbal tonics, oils, immunity support, digestive care, skin solutions, "
            "and clinic-recommended healing essentials."
        )
    )
    focus_title = models.CharField(max_length=120, default="Patient Focus")
    focus_text = models.TextField(
        default=(
            "Simple guidance, respectful support, and a smooth order process for every patient."
        )
    )
    contact_badge = models.CharField(
        max_length=120, default="Contact Natural Medical Clinic"
    )
    contact_heading = models.CharField(
        max_length=200,
        default="We are here to help with clinic visits, remedies, and order questions.",
    )
    contact_description = models.TextField(
        default=(
            "Reach out for treatment guidance, product support, clinic timings, "
            "or delivery updates."
        )
    )
    phone_number = models.CharField(max_length=30, default="+92 300 1234567")
    secondary_phone = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(default="support@naturalclinicstore.com")
    business_hours = models.CharField(
        max_length=150, default="Monday to Saturday, 10:00 AM to 8:00 PM"
    )
    address = models.TextField(default="Natural Clinic Store, Karachi, Pakistan")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        defaults = {
            field.name: field.default
            for field in cls._meta.fields
            if field.name != "id" and field.default is not models.NOT_PROVIDED
        }
        obj, _ = cls.objects.get_or_create(pk=1, defaults=defaults)
        return obj

    @property
    def brand_initials(self):
        words = self.site_name.split()
        if not words:
            return "NC"
        return "".join(word[0].upper() for word in words[:2])

    class Meta:
        verbose_name = "Site content"
        verbose_name_plural = "Site content"

    def __str__(self):
        return "Website Content"


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100)
    short_description = models.CharField(max_length=220)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock > 0


class CustomerOrder(models.Model):
    PAYMENT_CHOICES = [
        ("cod", "Cash on delivery"),
        ("bank", "Bank transfer"),
    ]

    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=80)
    notes = models.TextField(blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cod")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"

    @property
    def total_amount(self):
        total = Decimal("0.00")
        for item in self.items.all():
            total += item.line_total
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def line_total(self):
        return self.unit_price * self.quantity
