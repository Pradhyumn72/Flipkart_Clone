from django.shortcuts import render, redirect
from django import *
from .forms import AdminLoginForm,UserLoginForm,Registerform
from .models import Product
from django.contrib import messages



# Create your views here.
def register(req):
    pass
def _product_catalog():
    # Pull from DB; if empty, show nothing (admin can add via Django admin)
    return list(Product.objects.all().values('id', 'title', 'label', 'price', 'image_url'))


def index(req):
    return render(req,'index.html', {"products": _product_catalog()})

def adhome(req):
    return render(req,'adhome.html')
from django.contrib import messages

def adminlogin(req):
    if req.method == 'POST':
        form = AdminLoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if username == "admin" and password == "ad@1234":
                messages.success(req, "Admin login successful!")
                return redirect('index')   
            else:
                messages.error(req, "Invalid credentials")
    else:
        form = AdminLoginForm()

    return render(req, 'adhome.html', {'form': form})



def register(req):
    print(req.method)
    if req.method=='POST':
        form=Registerform(req.POST)
     
        if form.is_valid():
            form.save()
            fm=Registerform()
            return render(req,'userlogin.html',{'x':form})
        else:
            fm=Registerform()
            return render(req,'register.html',{'x':fm})
    return render(req,'register.html')

def userlogin(req):
    if req.method == 'POST':
        form = UserLoginForm(req.POST)
        if form.is_valid():
            req.session['user'] = {
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['username'],
                'contact_number': form.cleaned_data['contact_number'],
            }
            messages.success(req, "User login successful!")
            return redirect('index')
        else:
            messages.error(req, "Please correct the errors below")
    else:
        form = UserLoginForm()
    return render(req, 'userlogin.html', {'form': form})

def _get_cart_nested(session):
    #  it ensures all keys exist
    cart = session.get('cart')
    if not isinstance(cart, dict):
        cart = {}
    if 'cartt' not in cart or not isinstance(cart.get('cartt'), dict):
        cart['cartt'] = {}
    if 'carttt' not in cart['cartt'] or not isinstance(cart['cartt'].get('carttt'), list):
        cart['cartt']['carttt'] = []

    # set user id from session user if present, else default will be run
    user_id = 1
    user = session.get('user')
    if user:
        user_id = 1  # placeholder; in real app map to DB user id
    cart['user_id'] = user_id
    cart['cartt']['user_id'] = user_id

    session['cart'] = cart
    session.modified = True
    return cart

def add_to_cart(req, product_id):
    if req.method == 'POST':
        cart = _get_cart_nested(req.session)
        # append product id to nested list
        cart['cartt']['carttt'].append(product_id)
        req.session['cart'] = cart
        messages.success(req, f"Added to cart: #{product_id}")
    return redirect('index')

def view_cart(req):
    cart = _get_cart_nested(req.session)
    product_ids = cart['cartt']['carttt']
    # total quantity quantity per product id
    qty_by_id = {}
    for pid in product_ids:
        qty_by_id[pid] = qty_by_id.get(pid, 0) + 1
    # build items with details
    catalog = {p['id']: p for p in _product_catalog()}
    items = []
    subtotal = 0
    for pid, qty in qty_by_id.items():
        if pid in catalog:
            info = catalog[pid]
            line_total = info['price'] * qty
            subtotal += line_total
            items.append({
                'id': pid,
                'title': info['title'],
                'price': info['price'],
                'qty': qty,
                'line_total': line_total,
            })

            '''
            '''
    return render(req, 'cart.html', {'items': items, 'subtotal': subtotal})