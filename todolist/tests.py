from django.test import TestCase
from django.urls import reverse

from .models import CustomerOrder, OrderItem, Product, SiteContent


class StoreViewsTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Rose Face Wash",
            slug="rose-face-wash",
            category="Skin Care",
            short_description="Gentle herbal cleanser for daily use.",
            description="A plant-based face wash made for sensitive and acne-prone skin.",
            price="850.00",
            stock=10,
            is_featured=True,
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Al-Momin Dawakhana")

    def test_about_and_contact_pages_use_admin_managed_site_content(self):
        SiteContent.objects.create(
            site_name="Al-Momin Dawakhana",
            phone_number="+92 311 0000000",
            contact_email="hello@seekho.pk",
            about_heading="Custom about heading from admin",
            vision_text="Custom vision from admin panel.",
            contact_heading="Custom contact heading from admin",
            address="Block 5, Karachi",
        )

        about_response = self.client.get(reverse("about"))
        contact_response = self.client.get(reverse("contact"))

        self.assertContains(about_response, "Custom about heading from admin")
        self.assertContains(about_response, "Custom vision from admin panel.")
        self.assertContains(contact_response, "+92 311 0000000")
        self.assertContains(contact_response, "hello@seekho.pk")
        self.assertContains(contact_response, "Block 5, Karachi")

    def test_add_to_cart_and_checkout_creates_order(self):
        self.client.post(reverse("add_to_cart", args=[self.product.id]), {"next_url": reverse("cart")})
        response = self.client.post(
            reverse("checkout"),
            {
                "customer_name": "Areeba Khan",
                "email": "areeba@example.com",
                "phone": "03001234567",
                "city": "Karachi",
                "address": "House 12, Green Avenue",
                "payment_method": "cod",
                "notes": "Please call before delivery.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomerOrder.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)
