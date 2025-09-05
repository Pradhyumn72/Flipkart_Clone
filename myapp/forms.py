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

class Registerform(forms.Form):
    email=forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder':"Enter Email ID"})
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'})
    )
    
    contact=forms.CharField(
        
        required=True,
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder':"Enter Contact Number"})
        )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )
    cpassword=forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder":"Enter your confirm Password"})
    )

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email ID'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )
    

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number', '')
        digits_only = ''.join(ch for ch in contact_number if ch.isdigit())
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise forms.ValidationError("Enter a valid contact number")
        return digits_only

