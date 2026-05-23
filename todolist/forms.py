from django import forms


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Full name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"})
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "+92 300 1234567"}),
    )
    city = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "Karachi"}),
    )
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "House, street, area, and nearby landmark"}
        )
    )
    payment_method = forms.ChoiceField(
        choices=[
            ("cod", "Cash on delivery"),
            ("bank", "Bank transfer"),
        ],
        widget=forms.Select(),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Share any consultation note, delivery timing, or special instruction",
            }
        ),
    )
