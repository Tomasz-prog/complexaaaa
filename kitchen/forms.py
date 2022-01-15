from django import forms

class ShoppingItems(forms.Form):

    product1 = forms.CharField(label='Produkt nr.1', max_length=100, required=False)
    product2 = forms.CharField(label='Produkt nr.2', max_length=100, required=False)
    product3 = forms.CharField(label='Produkt nr.3', max_length=100,required=False)
    product4 = forms.CharField(label='Produkt nr.4', max_length=100, required=False)
    product5 = forms.CharField(label='Produkt nr.5', max_length=100,required=False)
    product6 = forms.CharField(label='Produkt nr.6', max_length=100,required=False)
    product7 = forms.CharField(label='Produkt nr.7', max_length=100,required=False)
    product8 = forms.CharField(label='Produkt nr.8', max_length=100,required=False)
    product9 = forms.CharField(label='Produkt nr.9', max_length=100,required=False)
    product10 = forms.CharField(label='Produkt nr.10', max_length=100,required=False)
