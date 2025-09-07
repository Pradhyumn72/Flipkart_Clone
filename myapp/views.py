from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdminLoginForm, UserLoginForm, Registerform, ProductForm
from .models import Product, AdminUser
from django.contrib import messages



# Create your views here.
def _product_catalog():
    return [
        {"id": 1, "title": "Apple iPhone 14 Pro (128GB)", "label": "iPhone 14 Pro", "price": 129900},
        {"id": 2, "title": "Dell XPS 13 (i7, 16GB)", "label": "Dell XPS 13", "price": 115990},
        {"id": 3, "title": "Nike Air Max 270 React", "label": "Nike Air Max", "price": 12795},
        {"id": 4, "title": "Samsung 55\" 4K Ultra HD TV", "label": "Samsung TV", "price": 52990},
        {"id": 5, "title": "Adidas Originals Track Jacket", "label": "Adidas Jacket", "price": 4999},
        {"id": 6, "title": "Sony PlayStation 5 Console", "label": "PlayStation 5", "price": 49990},
    ]


def index(req):
    return render(req,'index.html', {"products": _product_catalog()})

def adhome(req):
    return render(req,'adhome.html')

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
    else:
        fm=Registerform()
        return render(req,'register.html',{'x':fm})

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

    return render(req, 'cart.html', {'items': items, 'subtotal': subtotal})


# Admin Views
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                admin = AdminUser.objects.get(username=username, is_active=True)
                if check_password(password, admin.password_hash):
                    request.session['is_admin'] = True
                    request.session['admin_name'] = admin.username
                    messages.success(request, "Welcome, Admin!")
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, "Invalid password")
            except AdminUser.DoesNotExist:
                messages.error(request, "User not found")
    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'form': form})


def admin_logout(request):
    request.session.flush()  # clears all session data
    messages.success(request, "Logged out successfully")
    return redirect('admin_login')


# --- SIMPLE DASHBOARD ---
def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    products = Product.objects.all()
    return render(request, 'admin_dashboard.html', {
        'products': products,
        'total_products': products.count(),
        'admin_name': request.session.get('admin_name')
    })


# ---  LIST ---
def product_list(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    products = Product.objects.all().order_by('-created_at')
    return render(request, 'product_list.html', {'products': products})


# ---  CREATE ---
def product_create(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added!")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'title': 'Add Product'})


# ---  UPDATE ---
def product_edit(request, pk):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'title': 'Edit Product'})


# ---  DELETE ---
def product_delete(request, pk):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted!")
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})