from django.db import migrations


def seed_clinic_content(apps, schema_editor):
    SiteContent = apps.get_model("todolist", "SiteContent")
    Product = apps.get_model("todolist", "Product")

    site_content, _ = SiteContent.objects.get_or_create(pk=1)
    site_content.site_name = "Al-Qadeem dawakhana(Al-momin dawakhana)"
    site_content.site_tagline = "Natural healing, herbal remedies, and trusted family care"
    site_content.footer_text = (
        "Natural Medical Clinic offers herbal support, guided wellness care, "
        "and an easy order process for trusted home delivery."
    )
    site_content.about_badge = "About Natural Medical Clinic"
    site_content.about_heading = "A calm, trusted clinic experience built around natural medicine."
    site_content.about_description = (
        "Natural Medical Clinic supports families with herbal remedies, wellness "
        "products, and practical care guidance. Patients can explore recommended "
        "items, review details, and place orders online with ease."
    )
    site_content.vision_title = "Our Vision"
    site_content.vision_text = "Make reliable natural medicine and guided wellness care easier to access."
    site_content.offerings_title = "What We Offer"
    site_content.offerings_text = (
        "Herbal tonics, oils, immunity support, digestive care, skin solutions, "
        "and clinic-recommended healing essentials."
    )
    site_content.focus_title = "Patient Focus"
    site_content.focus_text = (
        "Simple guidance, respectful support, and a smooth order process for every patient."
    )
    site_content.contact_badge = "Contact Natural Medical Clinic"
    site_content.contact_heading = "We are here to help with clinic visits, remedies, and order questions."
    site_content.contact_description = (
        "Reach out for treatment guidance, product support, clinic timings, or delivery updates."
    )
    site_content.phone_number = "+92 300 1234567"
    site_content.whatsapp_number = "+92 300 1234567"
    site_content.contact_email = "care@naturalmedicalclinic.com"
    site_content.business_hours = "Monday to Saturday, 9:00 AM to 8:00 PM"
    site_content.address = "Natural Medical Clinic, Main Shahrah-e-Faisal, Karachi, Pakistan"
    site_content.save()

    if Product.objects.exists():
        return

    products = [
        {
            "name": "Herbal Immunity Syrup",
            "slug": "herbal-immunity-syrup",
            "category": "Immunity",
            "short_description": "Daily herbal tonic for seasonal support and recovery.",
            "description": "A warming herbal syrup selected by the clinic to support immunity, energy, and recovery during changing weather.",
            "price": "850.00",
            "stock": 24,
            "image_url": "https://images.unsplash.com/photo-1514996937319-344454492b37?auto=format&fit=crop&w=900&q=80",
            "is_featured": True,
        },
        {
            "name": "Digestive Relief Powder",
            "slug": "digestive-relief-powder",
            "category": "Digestive Care",
            "short_description": "Natural support for bloating, heaviness, and stomach discomfort.",
            "description": "A traditional digestive blend made for post-meal comfort and balanced gut wellness.",
            "price": "620.00",
            "stock": 18,
            "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80",
            "is_featured": True,
        },
        {
            "name": "Joint Ease Massage Oil",
            "slug": "joint-ease-massage-oil",
            "category": "Pain Relief",
            "short_description": "A clinic-preferred massage oil for stiffness and body fatigue.",
            "description": "Used for light massage on sore joints and muscles, this oil is designed to support movement and relaxation.",
            "price": "990.00",
            "stock": 15,
            "image_url": "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=900&q=80",
            "is_featured": True,
        },
        {
            "name": "Skin Calm Herbal Cream",
            "slug": "skin-calm-herbal-cream",
            "category": "Skin Care",
            "short_description": "Soothing external care for dry, irritated, and sensitive skin.",
            "description": "A gentle cream chosen for daily support where calm hydration and herbal skin comfort are needed.",
            "price": "740.00",
            "stock": 20,
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=900&q=80",
            "is_featured": False,
        },
        {
            "name": "Women's Wellness Tonic",
            "slug": "womens-wellness-tonic",
            "category": "Women's Wellness",
            "short_description": "Balanced herbal support for energy, routine care, and wellbeing.",
            "description": "Prepared for women seeking daily strength, restorative care, and clinic-guided support.",
            "price": "1100.00",
            "stock": 12,
            "image_url": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=900&q=80",
            "is_featured": False,
        },
        {
            "name": "Herbal Sleep Support Drops",
            "slug": "herbal-sleep-support-drops",
            "category": "Wellness",
            "short_description": "Mild natural drops prepared for evening calm and better rest.",
            "description": "Recommended for bedtime routines when gentle calming support is preferred.",
            "price": "680.00",
            "stock": 16,
            "image_url": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=900&q=80",
            "is_featured": False,
        },
    ]

    for product in products:
        Product.objects.create(**product)


class Migration(migrations.Migration):
    dependencies = [
        ("todolist", "0005_sitecontent"),
    ]

    operations = [
        migrations.RunPython(seed_clinic_content, migrations.RunPython.noop),
    ]
