from django import forms
from django_countries.fields import CountryField

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)
class CheckoutForm(forms.Form):
    add1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'street number '
    }) )
    add2 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Apartment number '
    }) )
    country = CountryField(blank_label='(select country)').formfield()
    zip = forms.CharField(max_length=10)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

