from django.contrib import admin

from .models import CustomerOrder, OrderItem, Product, SiteContent


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "unit_price")


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Branding",
            {"fields": ("site_name", "site_tagline", "footer_text")},
        ),
        (
            "About Page",
            {
                "fields": (
                    "about_badge",
                    "about_heading",
                    "about_description",
                    "vision_title",
                    "vision_text",
                    "offerings_title",
                    "offerings_text",
                    "focus_title",
                    "focus_text",
                )
            },
        ),
        (
            "Contact Page",
            {
                "fields": (
                    "contact_badge",
                    "contact_heading",
                    "contact_description",
                    "phone_number",
                    "secondary_phone",
                    "whatsapp_number",
                    "contact_email",
                    "business_hours",
                    "address",
                    "facebook_url",
                    "instagram_url",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        if SiteContent.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_featured", "is_active")
    list_filter = ("category", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "category", "short_description")


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "phone", "city", "payment_method", "created_at")
    search_fields = ("customer_name", "phone", "email", "city")
    inlines = [OrderItemInline]
