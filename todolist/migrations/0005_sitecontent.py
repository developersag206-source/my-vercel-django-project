from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todolist", "0004_alter_orderitem_quantity"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteContent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("site_name", models.CharField(default="Natural Clinic Store", max_length=150)),
                (
                    "site_tagline",
                    models.CharField(default="Herbal wellness and daily care", max_length=200),
                ),
                (
                    "footer_text",
                    models.TextField(
                        default=(
                            "Natural Clinic Store helps local customers order trusted herbal "
                            "care, wellness products, and clinic essentials online."
                        )
                    ),
                ),
                (
                    "about_badge",
                    models.CharField(default="About Natural Clinic Store", max_length=120),
                ),
                (
                    "about_heading",
                    models.CharField(
                        default="Built for trusted natural care and local e-commerce sales.",
                        max_length=200,
                    ),
                ),
                (
                    "about_description",
                    models.TextField(
                        default=(
                            "Natural Clinic Store is designed for a clinic or wellness "
                            "business that wants to sell herbal and natural products online. "
                            "The website helps customers explore products, read details, add "
                            "items to their cart, and place orders quickly."
                        )
                    ),
                ),
                ("vision_title", models.CharField(default="Our Vision", max_length=120)),
                (
                    "vision_text",
                    models.TextField(
                        default="Make natural wellness products easier to discover and purchase online."
                    ),
                ),
                ("offerings_title", models.CharField(default="What We Sell", max_length=120)),
                (
                    "offerings_text",
                    models.TextField(
                        default=(
                            "Herbal skin care, oils, supplements, immunity support, and "
                            "clinic-recommended essentials."
                        )
                    ),
                ),
                ("focus_title", models.CharField(default="Customer Focus", max_length=120)),
                (
                    "focus_text",
                    models.TextField(
                        default=(
                            "Clear information, simple checkout, and stock visibility for "
                            "better buying decisions."
                        )
                    ),
                ),
                (
                    "contact_badge",
                    models.CharField(default="Contact Natural Clinic Store", max_length=120),
                ),
                (
                    "contact_heading",
                    models.CharField(
                        default="We are here to help with product and order questions.",
                        max_length=200,
                    ),
                ),
                (
                    "contact_description",
                    models.TextField(
                        default=(
                            "Reach out for order support, product guidance, clinic inquiries, "
                            "or delivery updates."
                        )
                    ),
                ),
                ("phone_number", models.CharField(default="+92 300 1234567", max_length=30)),
                ("secondary_phone", models.CharField(blank=True, max_length=30)),
                ("whatsapp_number", models.CharField(blank=True, max_length=30)),
                (
                    "contact_email",
                    models.EmailField(default="support@naturalclinicstore.com", max_length=254),
                ),
                (
                    "business_hours",
                    models.CharField(
                        default="Monday to Saturday, 10:00 AM to 8:00 PM",
                        max_length=150,
                    ),
                ),
                ("address", models.TextField(default="Natural Clinic Store, Karachi, Pakistan")),
                ("facebook_url", models.URLField(blank=True)),
                ("instagram_url", models.URLField(blank=True)),
            ],
            options={
                "verbose_name": "Site content",
                "verbose_name_plural": "Site content",
            },
        ),
    ]
