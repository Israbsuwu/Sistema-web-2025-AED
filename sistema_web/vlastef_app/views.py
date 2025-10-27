from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Cliente, Categoria, Producto, Proveedor, Venta, DetalleVenta, Comentario, Carrito, CarritoDetalle, Stock
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Cliente, Producto
from django.db.models import Q

# Create your views here.
def index_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or '@' not in email:
            error = 'Introduce un correo válido.'
        elif not password:
            error = 'La contraseña no puede estar vacía.'
        else:
            try:
                user = User.objects.get(email=email)
                user_auth = authenticate(request, username=user.username, password=password)
                if user_auth is not None:
                    login(request, user_auth)
                    # If staff or superuser, redirect to admin panel dashboard
                    if user_auth.is_staff or user_auth.is_superuser:
                        return redirect('admin_dashboard')
                    return redirect('home')
                else:
                    error = "Correo o contraseña incorrectos."
            except User.DoesNotExist:
                error = "Correo no registrado."

    return render(request, 'vlastef_app/index.html', {'error': error})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user, cliente = form.save()
            # Don't auto-login: show success message and let the user log in manually
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión con tu correo y contraseña.')
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'vlastef_app/register.html', {'form': form})


@login_required
def home_view(request):
    user = request.user
    # sample products passed from server-side (will replace with real Producto queryset later)
    sample_products = [
        { 'id': 'p1', 'title': 'Vestido floral Primavera', 'price': 29.99, 'oldPrice': 45.00, 'img': 'https://images.unsplash.com/photo-1520975698515-1f8c7eea3f9c?q=80&w=800&auto=format&fit=crop', 'category':'mujer'},
        { 'id': 'p2', 'title': 'Zapatillas deportivas', 'price': 49.5, 'oldPrice': 69.99, 'img': 'https://images.unsplash.com/photo-1600180758890-1787632f0b27?q=80&w=800&auto=format&fit=crop', 'category':'calzado'},
        { 'id': 'p3', 'title': 'Bolso clásico cuero', 'price': 85.00, 'oldPrice': None, 'img': 'https://images.unsplash.com/photo-1543165796-3f4c7a6d69f6?q=80&w=800&auto=format&fit=crop', 'category':'accesorios'},
        { 'id': 'p4', 'title': 'Camisa formal hombre', 'price': 22.00, 'oldPrice': 35.00, 'img': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=800&auto=format&fit=crop', 'category':'hombre'},
        { 'id': 'p5', 'title': 'Pantalones cargo', 'price': 39.99, 'oldPrice': 59.99, 'img': 'https://images.unsplash.com/photo-1520975698515-1f8c7eea3f9c?q=80&w=800&auto=format&fit=crop', 'category':'hombre'},
        { 'id': 'p6', 'title': 'Collar elegante', 'price': 12.5, 'oldPrice': 19.99, 'img': 'https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?q=80&w=800&auto=format&fit=crop', 'category':'accesorios'},
        { 'id': 'p7', 'title': 'Sudadera con capucha', 'price': 34.00, 'oldPrice': None, 'img': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=800&auto=format&fit=crop', 'category':'mujer'},
        { 'id': 'p8', 'title': 'Gafas de sol', 'price': 16.99, 'oldPrice': 24.99, 'img': 'https://images.unsplash.com/photo-1504198453319-5ce911bafcde?q=80&w=800&auto=format&fit=crop', 'category':'accesorios'},
    ]

    return render(request, 'vlastef_app/home.html', {'user': user, 'products': sample_products})


def logout_view(request):
    auth_logout(request)
    return redirect('index')


# Helper to test staff/superuser
def staff_required(user):
    return user.is_active and (user.is_staff or user.is_superuser)


@user_passes_test(staff_required, login_url='index')
def admin_dashboard_view(request):
    users_count = User.objects.count()
    clients_count = Cliente.objects.count()
    products_count = Producto.objects.count()
    categories_count = Categoria.objects.count()
    suppliers_count = Proveedor.objects.count()
    comments_count = Comentario.objects.count()
    stock_movements_count = Stock.objects.count()
    return render(request, 'vlastef_app/admin_panel/dashboard.html', {
        'users_count': users_count,
        'clients_count': clients_count,
        'products_count': products_count,
        'categories_count': categories_count,
        'suppliers_count': suppliers_count,
        'comments_count': comments_count,
        'stock_movements_count': stock_movements_count,
    })


@user_passes_test(staff_required, login_url='index')
def admin_users_view(request):
    q = request.GET.get('q', '').strip()
    users_qs = User.objects.all().order_by('-date_joined')
    if q:
        users_qs = users_qs.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
    # prefetch cliente relation
    users = users_qs.select_related()
    # list of user ids that have a Cliente
    client_user_ids = list(Cliente.objects.filter(usuario_id__in=[u.id for u in users_qs]).values_list('usuario_id', flat=True))
    return render(request, 'vlastef_app/admin_panel/users.html', {'users': users, 'client_user_ids': client_user_ids, 'query': q})


def csrf_failure(request, reason=""):
    """Custom CSRF failure handler: show a friendly message and redirect to login/index."""
    try:
        messages.error(request, 'Error de seguridad (CSRF). Por favor recarga la página e inicia sesión de nuevo.')
    except Exception:
        # messages may fail if middleware not loaded; ignore
        pass
    return redirect('index')