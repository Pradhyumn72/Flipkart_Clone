from django import forms 
from django.core.exceptions import ValidationError

class Product(forms.Form):
    Item_Name=forms.CharField(max_length=60)
    Price=forms.IntegerField()
    Category=forms.MultipleChoiceField()
    Stock_Capacity=forms.IntegerField()
    Current_Stock=forms.IntegerField()
    Description=forms.CharField(max_length=100)
    Image=forms.ImageField()


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username != "admin" or password != "ad@1234":
            raise forms.ValidationError("Invalid username or password")
        return cleaned_data

