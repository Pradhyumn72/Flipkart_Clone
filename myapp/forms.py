from django import forms 
from .models import Register,User,Product
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'label', 'price', 'image', 'image_url', 'description', 'category', 'stock', 'is_active']


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

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Email does not exist, kindly register")

            # plain-text password check
            if user.password != password:
                raise forms.ValidationError("Email and password do not match")

            # attach user object for view usage
            cleaned_data["user"] = user

        return cleaned_data
    








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

