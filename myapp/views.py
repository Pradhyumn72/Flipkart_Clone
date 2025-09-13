from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdminLoginForm, UserLoginForm, RegisterForm, ProductForm
from .models import Product, AdminUser,Register
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Admin
from .forms import ProductForm, AdminLoginForm


# Create your views here.
def index(req):
    products = Product.objects.filter(is_active=True)
    return render(req, "index.html", {"products": products})

def adhome(req):
    return render(req,'adhome.html')


def dashboard(req):
    products = Product.objects.order_by('-created_at') 
    total_products = products.count()
    active_products = products.filter(is_active=True).count()

    return render(req, 'admin_dashboard.html', {
        'admin_username': req.session.get('admin_username', 'Admin'),
        'total_products': total_products,
        'active_products': active_products,
        'products': products
    })
 







def register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            # Extract cleaned data from form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            password = form.cleaned_data['password']

            # Save using objects.create
            Register.objects.create(
                name=name,
                email=email,
                contact=contact,
                password=password    
            )

            return render(req, 'userlogin.html', {'x': form})
        else:
            print(form.errors)  # Debugging
            return render(req, 'register.html', {'x': form})
    else:
        form = RegisterForm()
        return render(req, 'register.html', {'x': form})





def userlogin(req):
    if req.method == 'POST':
        form = UserLoginForm(req.POST)
        if form.is_valid():
            req.session['user'] = {
                'id': form.cleaned_data['user'].id,
                'email': form.cleaned_data['email'],
            }
            messages.success(req, "User login successful!")
            return redirect('index')  
        else:
            messages.error(req, "Please correct the errors below")
    else:
        form = UserLoginForm()
    return render(req, 'userlogin.html', {'form': form})






def _get_cart_nested(session):
    # ensure cart dict exists
    cart = session.get('cart')
    if not isinstance(cart, dict):
        cart = {}

    # ensure sub-keys exist
    if 'cartt' not in cart or not isinstance(cart.get('cartt'), dict):
        cart['cartt'] = {}
    if 'carttt' not in cart['cartt'] or not isinstance(cart['cartt'].get('carttt'), list):
        cart['cartt']['carttt'] = []

    # set user id (fall back to None if not logged in)
    user = session.get('user')
    if user:
        user_id = user.get('email')  # from your login session structure
    else:
        user_id = None

    # assign user_id into cart
    cart['user_id'] = user_id
    cart['cartt']['user_id'] = user_id

    # save back into session
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

    # total quantity per product id
    qty_by_id = {}
    for pid in product_ids:
        qty_by_id[pid] = qty_by_id.get(pid, 0) + 1

    # fetch products from DB
    products = Product.objects.filter(id__in=product_ids)
    catalog = {p.id: p for p in products}

    items = []
    subtotal = 0
    for pid, qty in qty_by_id.items():
        if pid in catalog:
            info = catalog[pid]
            line_total = info.price * qty
            subtotal += line_total
            items.append({
                'id': pid,
                'title': info.title,
                'price': info.price,
                'qty': qty,
                'line_total': line_total,
            })

    return render(req, 'cart.html', {'items': items, 'subtotal': subtotal})



# Admin Views

# def adminlogin(req):
#     if req.method == 'POST':
#         form = AdminLoginForm(req.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             if username == "admin" and password == "ad@1234":
#                 messages.success(req, "Admin login successful!")
#                 return redirect('admin_dashboard')   
#             else:
#                 messages.error(req, "Invalid credentials")
#     else:
#         form = AdminLoginForm()

#     return render(req, 'adhome.html', {'form': form})






# # --- SIMPLE DASHBOARD ---
# def admin_dashboard(request):
#     if not request.session.get('is_admin'):
#         return redirect('admin_login')

#     products = Product.objects.all()
#     return render(request, 'admin_dashboard.html', {
#         'products': products,
#         'total_products': products.count(),
#         'admin_name': request.session.get('admin_name')
#     })


# def product_catalog(req):
#     if req.method == "POST":
#         form = ProductForm(req.POST, req.FILES)
#         if form.is_valid():
#             form.save()   
#             return redirect('dashboard')  
#     else:
#         form = ProductForm()
#     return render(req, 'admin_product_create.html', {'form': form})


# # ---  LIST ---
# def product_list(request):
#     if not request.session.get('is_admin'):
#         return redirect('admin_login')

#     products = Product.objects.all().order_by('-created_at')
#     return render(request, 'product_list.html', {'products': products})


# # ---  CREATE ---
# def product_create(request):
#     if not request.session.get('is_admin'):
#         return redirect('admin_login')

#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Product added!")
#             return redirect('product_list')
#     else:
#         form = ProductForm()
#     return render(request, 'product_form.html', {'form': form, 'title': 'Add Product'})


# # ---  UPDATE ---
# def product_edit(request, pk):
#     if not request.session.get('is_admin'):
#         return redirect('admin_login')

#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, instance=product)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Product updated!")
#             return redirect('product_list')
#     else:
#         form = ProductForm(instance=product)
#     return render(request, 'product_form.html', {'form': form, 'title': 'Edit Product'})


# # ---  DELETE ---
# def product_delete(request, pk):
#     if not request.session.get('is_admin'):
#         return redirect('admin_login')

#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         product.delete()
#         messages.success(request, "Product deleted!")
#         return redirect('product_list')
#     return render(request, 'product_confirm_delete.html', {'product': product})def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                admin = Admin.objects.get(name=username, password=password)
                request.session["admin_id"] = admin.id
                return redirect("admin_dashboard")
            except Admin.DoesNotExist:
                messages.error(request, "Invalid credentials")
    else:
        form = AdminLoginForm()

    return render(request, "admin_login.html", {"form": form})


# -------------------
# Admin Dashboard
# -------------------

def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if username == "admin" and password == "ad@1234":
                request.session["is_admin"] = True
                return render(request,'admin_dashboard.html')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = AdminLoginForm()

    return render(request, "admin_login.html", {"form": form})



def admin_dashboard(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    products = Product.objects.all()
    return render(request, "admin_dashboard.html", {"products": products})


# -------------------
# Add Product
# -------------------
def add_product(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("admin_dashboard")
    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})


# -------------------
# Edit Product
# -------------------
def edit_product(request, pk):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("admin_dashboard")
    else:
        form = ProductForm(instance=product)

    return render(request, "edit_product.html", {"form": form})


# -------------------
# Delete Product
# -------------------
def delete_product(request, pk):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("admin_dashboard")


# -------------------
# Show products in index.html
# -------------------
def indexx(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "index.html", {"products": products})





def admin_logout(request):
    request.session.flush()  # clears all session data
    messages.success(request, "Logged out successfully")
    return redirect('admin_login')
