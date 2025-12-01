from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Cliente, Categoria, Producto, Proveedor, Venta, DetalleVenta, Comentario, Carrito, CarritoDetalle, Stock
from .forms import LoginForm, RegisterForm, ProductoForm, ProveedorForm, CategoriaForm, StockForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Cliente, Producto
from django.db.models import Q, Sum

# Create your views here.
# INICIO DE SESIÓN
def index_view(request):
    error = None
    initial = {} if request.method != 'POST' else request.POST
    form = LoginForm(initial if request.method == 'POST' else None)
    if request.method == 'POST':
        if form.is_valid():
            user_auth = form.cleaned_data['user_auth']
            from django.contrib.auth import login
            login(request, user_auth)
            # Funcionalidad de 'Recuérdame'
            if request.POST.get('remember'):
                request.session.set_expiry(1209600)  # 2 semanas
            else:
                request.session.set_expiry(0)  # hasta cerrar navegador
            if user_auth.is_staff or user_auth.is_superuser:
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            error_list = [e for e in form.errors.values()]
            error = error_list[0][0] if error_list and isinstance(error_list[0], list) else str(form.errors)
    else:
        # Limpiar campos y mensajes al volver al login
        form = LoginForm()
        error = None
    return render(request, 'vlastef_app/index.html', {'form': form, 'error': error})

# REGISTRO
def register_view(request):
    error = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user, cliente = form.save()
            from django.contrib import messages
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión con tu usuario y contraseña.')
            return redirect('index')
        else:
            # Mostrar solo el primer error general o de campo
            error_list = [e for e in form.errors.values()]
            error = error_list[0][0] if error_list and isinstance(error_list[0], list) else str(form.errors)
    else:
        form = RegisterForm()
        error = None
    return render(request, 'vlastef_app/register.html', {'form': form, 'error': error})

# HOME
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


# CERRAR SESIÓN
def logout_view(request):
    auth_logout(request)
    return redirect('index')


# VERIFICA SI ES STAFF O SUPERUSUARIO
def staff_required(user):
    return user.is_active and (user.is_staff or user.is_superuser)


# PANEL DE ADMINISTRACIÓN
# DASHBOARD
@user_passes_test(staff_required, login_url='index')
def admin_dashboard_view(request):
    ultimas_ventas = []
    productos_mas_vendidos = []
    productos_recientes = []
    return render(request, 'vlastef_app/admin_panel/dashboard.html', {
        'user': request.user,
        'ultimas_ventas': ultimas_ventas,
        'productos_mas_vendidos': productos_mas_vendidos,
        'productos_recientes': productos_recientes,
    })


# CLIENTES
@user_passes_test(staff_required, login_url='index')
def admin_clientes_view(request):
    q = request.GET.get('q', '').strip()
    clientes_qs = Cliente.objects.select_related('usuario').order_by('-fecha_registro')
    if q:
        clientes_qs = clientes_qs.filter(
            Q(usuario__username__icontains=q) |
            Q(usuario__email__icontains=q) |
            Q(nombres__icontains=q) |
            Q(apellidos__icontains=q) |
            Q(telefono__icontains=q)
        )
    
    total_clientes = clientes_qs.count()
    
    return render(request, 'vlastef_app/admin_panel/clientes.html', {
        'clientes': clientes_qs,
        'query': q,
        'total_clientes': total_clientes,
    })

# Detalles del cliente
@user_passes_test(staff_required, login_url='index')
def admin_cliente_detalle_view(request, user_id):
    cliente = get_object_or_404(Cliente, usuario_id=user_id)
    return render(request, 'vlastef_app/admin_panel/cliente_detalle.html', {'cliente': cliente})

# Editar campos del cliente
@user_passes_test(staff_required, login_url='index')
def admin_cliente_editar_view(request, user_id):
    cliente = get_object_or_404(Cliente, usuario_id=user_id)
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        
        # Validar email único
        if email:
            if User.objects.filter(email=email).exclude(id=user_id).exists():
                messages.error(request, 'Ya existe una cuenta con ese correo.')
                return render(request, 'vlastef_app/admin_panel/cliente_editar.html', {'cliente': cliente})
        
        # Validar teléfono único
        if telefono:
            if Cliente.objects.filter(telefono=telefono).exclude(id=cliente.id).exists():
                messages.error(request, 'Ya existe una cuenta con ese número de teléfono.')
                return render(request, 'vlastef_app/admin_panel/cliente_editar.html', {'cliente': cliente})
        
        # Actualizar datos de User
        user = cliente.usuario
        user.email = email
        user.first_name = request.POST.get('nombres') # Opcional si se usa nombres de Cliente
        user.last_name = request.POST.get('apellidos') # Opcional
        
        # Actualizar staff status
        is_staff = request.POST.get('is_staff') == 'on'
        user.is_staff = is_staff
        
        user.save()
        
        # Actualizar datos de Cliente
        cliente.nombres = request.POST.get('nombres')
        cliente.apellidos = request.POST.get('apellidos')
        cliente.telefono = telefono
        cliente.direccion = request.POST.get('direccion')
        cliente.save()
        
        messages.success(request, 'Cliente actualizado correctamente.')
        return redirect('admin_clientes')
    
    return render(request, 'vlastef_app/admin_panel/cliente_editar.html', {'cliente': cliente})

# Activar cliente
@user_passes_test(staff_required, login_url='index')
def admin_cliente_activar_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'Usuario {user.username} activado.')
    return redirect('admin_clientes')

# Desactivar cliente
@user_passes_test(staff_required, login_url='index')
def admin_cliente_desactivar_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'Usuario {user.username} desactivado.')
    return redirect('admin_clientes')

# Eliminar cliente
@user_passes_test(staff_required, login_url='index')
def admin_cliente_eliminar_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete() # Esto eliminará también al Cliente por el on_delete=CASCADE
    messages.success(request, 'Cliente eliminado correctamente.')
    return redirect('admin_clientes')

# Restablecer contraseña del cliente
@user_passes_test(staff_required, login_url='index')
def admin_cliente_reset_password_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        if not new_password or len(new_password.strip()) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('admin_cliente_editar', user_id=user.id)
        user.set_password(new_password)
        user.save()
        messages.success(request, f'Contraseña restablecida para {user.username}.')
        return redirect('admin_clientes')
    return redirect('admin_cliente_editar', user_id=user.id)


# CATEGORÍAS
@user_passes_test(staff_required, login_url='index')
def admin_categorias_view(request):
    q = request.GET.get('q', '').strip()
    categorias_qs = Categoria.objects.all().order_by('nombre')
    if q:
        categorias_qs = categorias_qs.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q)
        )
    
    total_categorias = categorias_qs.count()
    
    return render(request, 'vlastef_app/admin_panel/categorias.html', {
        'categorias': categorias_qs,
        'query': q,
        'total_categorias': total_categorias,
    })

# Crear categoría
@user_passes_test(staff_required, login_url='index')
def admin_categoria_crear_view(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('admin_categorias')
        else:
            nombre_errors = form.errors.get('nombre')
            if nombre_errors and any('Ya existe una categoría con ese nombre.' in str(e) for e in nombre_errors):
                messages.error(request, 'Ya existe una categoría con ese nombre.')
            else:
                messages.error(request, 'Corrige los errores en el formulario.')
            # Mantener valores ingresados en el template actual
            categoria = Categoria(nombre=request.POST.get('nombre', ''), descripcion=request.POST.get('descripcion', ''))
            return render(request, 'vlastef_app/admin_panel/categoria_form.html', {'titulo': 'Nueva Categoría', 'categoria': categoria})
    return render(request, 'vlastef_app/admin_panel/categoria_form.html', {'titulo': 'Nueva Categoría'})

# Editar categoría
@user_passes_test(staff_required, login_url='index')
def admin_categoria_editar_view(request, cat_id):
    categoria = get_object_or_404(Categoria, id=cat_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('admin_categorias')
        else:
            nombre_errors = form.errors.get('nombre')
            if nombre_errors and any('Ya existe otra categoría con ese nombre.' in str(e) for e in nombre_errors):
                messages.error(request, 'Ya existe otra categoría con ese nombre.')
            else:
                messages.error(request, 'Corrige los errores en el formulario.')
    return render(request, 'vlastef_app/admin_panel/categoria_form.html', {'categoria': categoria, 'titulo': 'Editar Categoría'})

# Eliminar categoría
@user_passes_test(staff_required, login_url='index')
def admin_categoria_eliminar_view(request, cat_id):
    categoria = get_object_or_404(Categoria, id=cat_id)
    categoria.delete()
    messages.success(request, 'Categoría eliminada exitosamente.')
    return redirect('admin_categorias')

# Detalles de la categoría
@user_passes_test(staff_required, login_url='index')
def admin_categoria_detalle_view(request, cat_id):
    categoria = get_object_or_404(Categoria.objects.prefetch_related('productos'), id=cat_id)
    productos = categoria.productos.all().select_related('categoria', 'proveedor')
    total_productos = productos.count()
    return render(request, 'vlastef_app/admin_panel/categoria_detalle.html', {
        'categoria': categoria,
        'productos': productos,
        'total_productos': total_productos,
    })


# PRODUCTOS
@user_passes_test(staff_required, login_url='index')
def admin_productos_view(request):
    q = request.GET.get('q', '').strip()
    productos_qs = Producto.objects.select_related('categoria', 'proveedor').order_by('-id')
    if q:
        productos_qs = productos_qs.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(categoria__nombre__icontains=q) |
            Q(proveedor__nombre__icontains=q)
        )
    return render(request, 'vlastef_app/admin_panel/productos.html', {
        'productos': productos_qs,
        'query': q,
    })

# Crear producto
@user_passes_test(staff_required, login_url='index')
def admin_producto_crear_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            # Reubicar imagen principal en carpeta por id
            if producto.imagen and producto.imagen.name:
                from django.conf import settings
                import os, shutil
                orig_rel = producto.imagen.name.replace('\\','/')
                if orig_rel.startswith('productos/') and not orig_rel.startswith(f'productos/{producto.id}/'):
                    orig_abs = os.path.join(settings.MEDIA_ROOT, orig_rel)
                    target_dir = os.path.join(settings.MEDIA_ROOT, 'productos', str(producto.id))
                    os.makedirs(target_dir, exist_ok=True)
                    new_name = os.path.basename(orig_abs)
                    try:
                        target_princ = os.path.join(target_dir, new_name)
                        if os.path.exists(target_princ):
                            try:
                                os.remove(target_princ)
                            except Exception:
                                pass
                        shutil.move(orig_abs, target_princ)
                        producto.imagen.name = f"productos/{producto.id}/{new_name}"
                        producto.save(update_fields=['imagen'])
                    except Exception:
                        pass
            # Guardar imágenes adicionales
            extra_files = request.FILES.getlist('extra_imagenes')
            if extra_files:
                import os
                from django.conf import settings
                base_dir = os.path.join(settings.MEDIA_ROOT, 'productos', 'extra', str(producto.id))
                os.makedirs(base_dir, exist_ok=True)
                for f in extra_files:
                    safe_name = f.name
                    dest_path = os.path.join(base_dir, safe_name)
                    if os.path.exists(dest_path):
                        try:
                            os.remove(dest_path)
                        except Exception:
                            pass
                    with open(dest_path, 'wb+') as dest:
                        for chunk in f.chunks():
                            dest.write(chunk)
            # Registrar movimiento de stock inicial si hay cantidad
            if producto.cantidad_disponible > 0:
                Stock.objects.create(
                    producto=producto,
                    tipo='E',
                    cantidad=producto.cantidad_disponible,
                    descripcion='Stock inicial al crear producto'
                )
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('admin_productos')
        else:
            messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = ProductoForm()
    return render(request, 'vlastef_app/admin_panel/producto_form.html', {'form': form, 'titulo': 'Nuevo Producto'})

# Editar producto
@user_passes_test(staff_required, login_url='index')
def admin_producto_editar_view(request, prod_id):
    producto = get_object_or_404(Producto, id=prod_id)
    cantidad_anterior = producto.cantidad_disponible
    # Marcar borrado de principal dentro del guardado normal
    if request.method == 'POST' and request.POST.get('delete_principal'):
        from django.conf import settings
        import os
        # Eliminar archivo físico si existe
        if producto.imagen and producto.imagen.name:
            abs_path = os.path.join(settings.MEDIA_ROOT, producto.imagen.name)
            if os.path.exists(abs_path):
                try:
                    os.remove(abs_path)
                except Exception:
                    pass
        producto.imagen = None
        producto.save(update_fields=['imagen'])
    # Borrado de imagen extra
    if request.method == 'POST' and request.POST.get('delete_extra'):
        del_name = request.POST.get('file_name')
        if del_name:
            from django.conf import settings
            import os
            rel = del_name.replace('\\','/')
            extra_prefix = f"productos/extra/{producto.id}/"
            # No borrar si es la principal
            if producto.imagen and producto.imagen.name.replace('\\','/') == rel:
                messages.error(request, 'No puedes eliminar la imagen principal desde este botón.')
            else:
                if rel.startswith(extra_prefix):
                    abs_path = os.path.join(settings.MEDIA_ROOT, rel)
                    if os.path.exists(abs_path):
                        try:
                            os.remove(abs_path)
                            messages.success(request, 'Imagen adicional eliminada.')
                        except Exception:
                            messages.error(request, 'No se pudo eliminar la imagen adicional.')
            return redirect('admin_producto_editar', prod_id=producto.id)
    # Procesar cambio de principal mediante POST separado
    if request.method == 'POST' and request.POST.get('set_principal'):
        filename = request.POST.get('file_name')
        if filename:
            from django.conf import settings
            import os, shutil
            rel = filename.replace('\\','/')
            # Esperamos ruta completa relativa dentro de MEDIA_ROOT
            extra_dir = f"productos/extra/{producto.id}/"
            principal_dir = f"productos/{producto.id}/"
            if rel.startswith(extra_dir):
                select_abs = os.path.join(settings.MEDIA_ROOT, rel)
                if os.path.exists(select_abs):
                    # Mover actual principal a extras si existe
                    current = producto.imagen.name.replace('\\','/') if producto.imagen else None
                    if current and current.startswith(principal_dir):
                        curr_abs = os.path.join(settings.MEDIA_ROOT, current)
                        if os.path.exists(curr_abs):
                            os.makedirs(os.path.join(settings.MEDIA_ROOT, extra_dir), exist_ok=True)
                            try:
                                target_extra = os.path.join(settings.MEDIA_ROOT, extra_dir, os.path.basename(curr_abs))
                                if os.path.exists(target_extra):
                                    try:
                                        os.remove(target_extra)
                                    except Exception:
                                        pass
                                shutil.move(curr_abs, target_extra)
                            except Exception:
                                pass
                    # Mover seleccionada a principal
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, principal_dir), exist_ok=True)
                    new_princ_name = os.path.basename(select_abs)
                    try:
                        target_princ = os.path.join(settings.MEDIA_ROOT, principal_dir, new_princ_name)
                        if os.path.exists(target_princ):
                            try:
                                os.remove(target_princ)
                            except Exception:
                                pass
                        shutil.move(select_abs, target_princ)
                        producto.imagen.name = f"{principal_dir}{new_princ_name}"
                        producto.save(update_fields=['imagen'])
                        messages.success(request, 'Imagen principal actualizada.')
                    except Exception:
                        messages.error(request, 'No se pudo cambiar la imagen principal.')
                    return redirect('admin_producto_editar', prod_id=producto.id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            # Reubicar nueva principal si se subió  
            if producto.imagen and producto.imagen.name:
                from django.conf import settings
                import os, shutil
                rel_main = producto.imagen.name.replace('\\','/')
                target_dir = os.path.join(settings.MEDIA_ROOT, 'productos', str(producto.id))
                if rel_main.startswith('productos/') and not rel_main.startswith(f'productos/{producto.id}/'):
                    abs_main = os.path.join(settings.MEDIA_ROOT, rel_main)
                    os.makedirs(target_dir, exist_ok=True)
                    new_name = os.path.basename(abs_main)
                    try:
                        target_princ = os.path.join(target_dir, new_name)
                        if os.path.exists(target_princ):
                            try:
                                os.remove(target_princ)
                            except Exception:
                                pass
                        shutil.move(abs_main, target_princ)
                        producto.imagen.name = f"productos/{producto.id}/{new_name}"
                        producto.save(update_fields=['imagen'])
                    except Exception:
                        pass
            # Guardar nuevas imágenes adicionales
            extra_files = request.FILES.getlist('extra_imagenes')
            if extra_files:
                import os
                from django.conf import settings
                base_dir = os.path.join(settings.MEDIA_ROOT, 'productos', 'extra', str(producto.id))
                os.makedirs(base_dir, exist_ok=True)
                for f in extra_files:
                    safe_name = f.name
                    dest_path = os.path.join(base_dir, safe_name)
                    if os.path.exists(dest_path):
                        try:
                            os.remove(dest_path)
                        except Exception:
                            pass
                    with open(dest_path, 'wb+') as dest:
                        for chunk in f.chunks():
                            dest.write(chunk)
            # Registrar aumento de stock si corresponde
            diferencia = producto.cantidad_disponible - cantidad_anterior
            if diferencia > 0:
                Stock.objects.create(
                    producto=producto,
                    tipo='E',
                    cantidad=diferencia,
                    descripcion='Aumento de stock al editar producto'
                )
            elif diferencia < 0:
                Stock.objects.create(
                    producto=producto,
                    tipo='S',
                    cantidad=abs(diferencia),
                    descripcion='Reducción de stock al editar producto'
                )
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('admin_productos')
        else:
            messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'vlastef_app/admin_panel/producto_form.html', {'form': form, 'titulo': 'Editar Producto', 'producto': producto})

# Eliminar producto
@user_passes_test(staff_required, login_url='index')
def admin_producto_eliminar_view(request, prod_id):
    producto = get_object_or_404(Producto, id=prod_id)
    # Conservar movimientos de stock de productos eliminados
    Stock.objects.filter(producto=producto).update(producto=None)
    producto.delete()
    messages.success(request, 'Producto eliminado exitosamente.')
    return redirect('admin_productos')


# PROVEEDORES
@user_passes_test(staff_required, login_url='index')
def admin_proveedores_view(request):
    q = request.GET.get('q', '').strip()
    proveedores_qs = Proveedor.objects.all().order_by('nombre')
    if q:
        proveedores_qs = proveedores_qs.filter(
            Q(nombre__icontains=q) |
            Q(correo__icontains=q) |
            Q(telefono__icontains=q) |
            Q(direccion__icontains=q)
        )
    total_proveedores = proveedores_qs.count()
    return render(request, 'vlastef_app/admin_panel/proveedores.html', {
        'proveedores': proveedores_qs,
        'query': q,
        'total_proveedores': total_proveedores,
    })

# Detalles del proveedor
@user_passes_test(staff_required, login_url='index')
def admin_proveedor_detalle_view(request, prov_id):
    proveedor = get_object_or_404(Proveedor.objects.prefetch_related('productos'), id=prov_id)
    productos = proveedor.productos.all().select_related('categoria', 'proveedor')
    total_productos = productos.count()
    return render(request, 'vlastef_app/admin_panel/proveedor_detalle.html', {
        'proveedor': proveedor,
        'productos': productos,
        'total_productos': total_productos,
    })

# Crear proveedor
@user_passes_test(staff_required, login_url='index')
def admin_proveedor_crear_view(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente.')
            return redirect('admin_proveedores')
        else:
            # Mensaje específico si el nombre ya existe y limpiar el campo
            nombre_errors = form.errors.get('nombre')
            if nombre_errors and any('Ya existe un proveedor con ese nombre.' in str(e) for e in nombre_errors):
                messages.error(request, 'Ya existe un proveedor con ese nombre.')
                mutable = request.POST.copy()
                mutable['nombre'] = ''
                form = ProveedorForm(mutable)
            else:
                correo_errors = form.errors.get('correo')
                if correo_errors and any('Ya existe un proveedor con ese correo.' in str(e) for e in correo_errors):
                    messages.error(request, 'Ya existe un proveedor con ese correo.')
                    mutable = request.POST.copy()
                    mutable['correo'] = ''
                    form = ProveedorForm(mutable)
                else:
                    telefono_errors = form.errors.get('telefono')
                    if telefono_errors and any('Ya existe un proveedor con ese teléfono.' in str(e) for e in telefono_errors):
                        messages.error(request, 'Ya existe un proveedor con ese teléfono.')
                        mutable = request.POST.copy()
                        mutable['telefono'] = ''
                        form = ProveedorForm(mutable)
                    elif form.errors.get('correo'):
                        messages.error(request, 'Ingresa un correo válido.')
                    else:
                        messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = ProveedorForm()
    return render(request, 'vlastef_app/admin_panel/proveedor_form.html', {'form': form, 'titulo': 'Nuevo Proveedor'})

# Editar proveedor
@user_passes_test(staff_required, login_url='index')
def admin_proveedor_editar_view(request, prov_id):
    proveedor = get_object_or_404(Proveedor, id=prov_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado exitosamente.')
            return redirect('admin_proveedores')
        else:
            nombre_errors = form.errors.get('nombre')
            if nombre_errors and any('Ya existe un proveedor con ese nombre.' in str(e) for e in nombre_errors):
                messages.error(request, 'Ya existe un proveedor con ese nombre.')
                mutable = request.POST.copy()
                mutable['nombre'] = ''
                form = ProveedorForm(mutable, instance=proveedor)
            else:
                correo_errors = form.errors.get('correo')
                if correo_errors and any('Ya existe un proveedor con ese correo.' in str(e) for e in correo_errors):
                    messages.error(request, 'Ya existe un proveedor con ese correo.')
                    mutable = request.POST.copy()
                    mutable['correo'] = ''
                    form = ProveedorForm(mutable, instance=proveedor)
                else:
                    telefono_errors = form.errors.get('telefono')
                    if telefono_errors and any('Ya existe un proveedor con ese teléfono.' in str(e) for e in telefono_errors):
                        messages.error(request, 'Ya existe un proveedor con ese teléfono.')
                        mutable = request.POST.copy()
                        mutable['telefono'] = ''
                        form = ProveedorForm(mutable, instance=proveedor)
                    elif form.errors.get('correo'):
                        messages.error(request, 'Ingresa un correo válido.')
                    else:
                        messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'vlastef_app/admin_panel/proveedor_form.html', {'form': form, 'titulo': 'Editar Proveedor', 'proveedor': proveedor})

# Eliminar proveedor
@user_passes_test(staff_required, login_url='index')
def admin_proveedor_eliminar_view(request, prov_id):
    proveedor = get_object_or_404(Proveedor, id=prov_id)
    proveedor.delete()
    messages.success(request, 'Proveedor eliminado exitosamente.')
    return redirect('admin_proveedores')


# COMENTARIOS
@user_passes_test(staff_required, login_url='index')
def admin_comentarios_view(request):
    q = request.GET.get('q', '').strip()
    comentarios_qs = Comentario.objects.select_related('cliente__usuario', 'producto').order_by('-fecha')
    if q:
        comentarios_qs = comentarios_qs.filter(
            Q(texto__icontains=q) |
            Q(cliente__usuario__username__icontains=q) |
            Q(producto__nombre__icontains=q)
        )
    total_comentarios = comentarios_qs.count()
    return render(request, 'vlastef_app/admin_panel/comentarios.html', {
        'comentarios': comentarios_qs,
        'query': q,
        'total_comentarios': total_comentarios,
    })

# Eliminar comentario
@user_passes_test(staff_required, login_url='index')
def admin_comentario_eliminar_view(request, com_id):
    comentario = get_object_or_404(Comentario, id=com_id)
    comentario.delete()
    messages.success(request, 'Comentario eliminado exitosamente.')
    return redirect('admin_comentarios')


# VENTAS
@user_passes_test(staff_required, login_url='index')
def admin_ventas_view(request):
    q = request.GET.get('q', '').strip()
    ventas_qs = Venta.objects.select_related('cliente__usuario').order_by('-fecha')
    
    if q:
        ventas_qs = ventas_qs.filter(
            Q(numero_factura__icontains=q) |
            Q(cliente__usuario__username__icontains=q) |
            Q(cliente__nombres__icontains=q) |
            Q(cliente__apellidos__icontains=q)
        )
    
    total_ventas = ventas_qs.count()
    return render(request, 'vlastef_app/admin_panel/ventas.html', {
        'ventas': ventas_qs,
        'query': q,
        'total_ventas': total_ventas,
    })

# Detalles de la venta
@user_passes_test(staff_required, login_url='index')
def admin_venta_detalle_view(request, venta_id):
    venta = get_object_or_404(Venta.objects.select_related('cliente__usuario'), id=venta_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Venta.ESTADO_CHOICES):
            # Si se marca como Pagada, validar stock y registrar salida
            if nuevo_estado == 'P':
                detalles = DetalleVenta.objects.filter(venta=venta).select_related('producto')
                # Validar stock suficiente para todos los productos
                insuficientes = []
                for d in detalles:
                    if d.producto.cantidad_disponible < d.cantidad:
                        insuficientes.append((d.producto.nombre, d.producto.cantidad_disponible, d.cantidad))
                if insuficientes:
                    # No cambiar estado si no hay stock
                    pass  # No message
                else:
                    # Descontar stock y registrar movimientos de salida
                    for d in detalles:
                        # Registrar movimiento en historial de Stock
                        Stock.objects.create(
                            producto=d.producto,
                            tipo='S',
                            cantidad=d.cantidad,
                            descripcion=f'Venta #{venta.id}'
                        )
                        # Actualizar cantidad disponible
                        d.producto.cantidad_disponible -= d.cantidad
                        d.producto.save()
                    venta.estado = nuevo_estado
                    venta.save()
                    messages.success(request, 'Estado de la venta actualizado correctamente.')
            else:
                venta.estado = nuevo_estado
                venta.save()
                messages.success(request, 'Estado de la venta actualizado correctamente.')
            return redirect('admin_venta_detalle', venta_id=venta.id)

    detalles = DetalleVenta.objects.filter(venta=venta).select_related('producto')
    total_calculado = detalles.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
    
    return render(request, 'vlastef_app/admin_panel/venta_detalle.html', {
        'venta': venta,
        'detalles': detalles,
        'total_calculado': total_calculado,
    })


# CARRITO
@user_passes_test(staff_required, login_url='index')
def admin_carritos_view(request):
    q = request.GET.get('q', '').strip()
    carritos_qs = Carrito.objects.select_related('cliente__usuario').order_by('-fecha_creacion')
    
    if q:
        carritos_qs = carritos_qs.filter(
            Q(cliente__usuario__username__icontains=q) |
            Q(cliente__nombres__icontains=q) |
            Q(cliente__apellidos__icontains=q)
        )
        
    total_carritos = carritos_qs.count()
    return render(request, 'vlastef_app/admin_panel/carritos.html', {
        'carritos': carritos_qs,
        'query': q,
        'total_carritos': total_carritos,
    })

# Detalles del carrito
@user_passes_test(staff_required, login_url='index')
def admin_carrito_detalle_view(request, carrito_id):
    carrito = get_object_or_404(Carrito.objects.select_related('cliente__usuario'), id=carrito_id)
    detalles = CarritoDetalle.objects.filter(carrito=carrito).select_related('producto')
    total_carrito = detalles.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
    return render(request, 'vlastef_app/admin_panel/carrito_detalle.html', {
        'carrito': carrito,
        'detalles': detalles,
        'total_carrito': total_carrito,
    })


# STOCK
@user_passes_test(staff_required, login_url='index')
def admin_stock_view(request):
    q = request.GET.get('q', '').strip()
    movimientos = Stock.objects.select_related('producto').order_by('-fecha')
    
    if q:
        movimientos = movimientos.filter(
            Q(producto__nombre__icontains=q) |
            Q(descripcion__icontains=q)
        )
    
    # Obtener resumen de stock actual por producto
    productos_stock = Producto.objects.all().order_by('nombre')
    
    return render(request, 'vlastef_app/admin_panel/stock.html', {
        'movimientos': movimientos,
        'productos_stock': productos_stock,
        'query': q,
    })

# Crear movimiento de stock
@user_passes_test(staff_required, login_url='index')
def admin_stock_crear_view(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            tipo = form.cleaned_data['tipo']
            cantidad = form.cleaned_data['cantidad']
            descripcion = form.cleaned_data['descripcion']
            
            # Validar stock suficiente para salidas
            if tipo == 'S' and producto.cantidad_disponible < cantidad:
                messages.error(request, f'No hay suficiente stock de {producto.nombre} para realizar esta salida. Disponible: {producto.cantidad_disponible}')
            else:
                # Crear registro de movimiento
                Stock.objects.create(
                    producto=producto,
                    tipo=tipo,
                    cantidad=cantidad,
                    descripcion=descripcion
                )
                
                # Actualizar stock del producto
                if tipo == 'E':
                    producto.cantidad_disponible += cantidad
                else:
                    producto.cantidad_disponible -= cantidad
                producto.save()
                
                messages.success(request, 'Movimiento de stock registrado exitosamente.')
                return redirect('admin_stock')
    else:
        form = StockForm()
    
    return render(request, 'vlastef_app/admin_panel/stock_form.html', {
        'form': form,
        'titulo': 'Registrar Movimiento de Stock'
    })


# CHECKOUT
@login_required
def checkout_view(request):
    cliente = request.user.cliente
    carrito = Carrito.objects.filter(cliente=cliente, procesado=False).first()
    if not carrito:
        messages.error(request, 'No tienes un carrito activo.')
        return redirect('home')
    
    detalles = CarritoDetalle.objects.filter(carrito=carrito).select_related('producto')
    if not detalles:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('home')
    
    # Verificar stock suficiente
    for d in detalles:
        if d.cantidad > d.producto.cantidad_disponible:
            messages.error(request, f'Stock insuficiente para {d.producto.nombre}. Disponible: {d.producto.cantidad_disponible}')
            return redirect('home')
    
    # Calcular total
    total = sum(d.cantidad * d.producto.precio_venta for d in detalles)
    
    # Crear Venta
    venta = Venta.objects.create(cliente=cliente, total=total)
    
    # Crear DetalleVenta, actualizar stock y crear movimientos
    for d in detalles:
        DetalleVenta.objects.create(
            venta=venta,
            producto=d.producto,
            cantidad=d.cantidad,
            precio_unitario=d.producto.precio_venta
        )
        
        # Actualizar stock del producto
        d.producto.cantidad_disponible -= d.cantidad
        d.producto.save()
        
        # Crear movimiento de stock
        Stock.objects.create(
            producto=d.producto,
            tipo='S',
            cantidad=d.cantidad,
            descripcion=f'Venta #{venta.id}'
        )
    
    # Marcar carrito como procesado
    carrito.procesado = True
    carrito.save()
    
    messages.success(request, f'Compra realizada exitosamente. Total: ${total:.2f}')
    return redirect('home')


# Manejo de errores CSRF
def csrf_failure(request, reason=""):
    try:
        messages.error(request, 'Error de seguridad (CSRF). Por favor recarga la página e inicia sesión de nuevo.')
    except Exception:
        pass
    return redirect('index')
