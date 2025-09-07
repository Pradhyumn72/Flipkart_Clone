from django import forms 
from .models import Register
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

class RegisterForm(forms.ModelForm):
    cpassword = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    class Meta:
        model = Register
        fields = ['name', 'email', 'contact', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
            'contact': forms.NumberInput(attrs={'placeholder': 'Enter Contact'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        }

    # validate password match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        cpassword = cleaned_data.get("cpassword")

        if password and cpassword and password != cpassword:
            self.add_error("cpassword", "Passwords do not match")

        return cleaned_data

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


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Admin Username', 'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'label', 'price', 'image_url', 'description', 'category', 'stock', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Title'}),
            'label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Label'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Image URL'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product Description', 'rows': 3}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Quantity'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

