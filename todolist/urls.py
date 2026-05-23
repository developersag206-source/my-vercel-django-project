from django.urls import path

from . import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("treatments/", views.treatments, name="treatments"),
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
