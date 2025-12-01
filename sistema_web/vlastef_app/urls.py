from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard Admin
    path('panel/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Clientes
    path('panel/clientes/', views.admin_clientes_view, name='admin_clientes'),
    path('panel/clientes/<int:user_id>/detalle/', views.admin_cliente_detalle_view, name='admin_cliente_detalle'),
    path('panel/clientes/<int:user_id>/editar/', views.admin_cliente_editar_view, name='admin_cliente_editar'),
    path('panel/clientes/<int:user_id>/activar/', views.admin_cliente_activar_view, name='admin_cliente_activar'),
    path('panel/clientes/<int:user_id>/desactivar/', views.admin_cliente_desactivar_view, name='admin_cliente_desactivar'),
    path('panel/clientes/<int:user_id>/eliminar/', views.admin_cliente_eliminar_view, name='admin_cliente_eliminar'),
    path('panel/clientes/<int:user_id>/reset-password/', views.admin_cliente_reset_password_view, name='admin_cliente_reset_password'),
    
    # Categorías
    path('panel/categorias/', views.admin_categorias_view, name='admin_categorias'),
    path('panel/categorias/crear/', views.admin_categoria_crear_view, name='admin_categoria_crear'),
    path('panel/categorias/<int:cat_id>/detalle/', views.admin_categoria_detalle_view, name='admin_categoria_detalle'),
    path('panel/categorias/<int:cat_id>/editar/', views.admin_categoria_editar_view, name='admin_categoria_editar'),
    path('panel/categorias/<int:cat_id>/eliminar/', views.admin_categoria_eliminar_view, name='admin_categoria_eliminar'),

    # Productos
    path('panel/productos/', views.admin_productos_view, name='admin_productos'),
    path('panel/productos/crear/', views.admin_producto_crear_view, name='admin_producto_crear'),
    path('panel/productos/<int:prod_id>/editar/', views.admin_producto_editar_view, name='admin_producto_editar'),
    path('panel/productos/<int:prod_id>/eliminar/', views.admin_producto_eliminar_view, name='admin_producto_eliminar'),
    path('panel/productos/<int:prod_id>/set-principal/', views.admin_producto_editar_view, name='admin_producto_set_principal'),

    # Proveedores
    path('panel/proveedores/', views.admin_proveedores_view, name='admin_proveedores'),
    path('panel/proveedores/<int:prov_id>/detalle/', views.admin_proveedor_detalle_view, name='admin_proveedor_detalle'),
    path('panel/proveedores/crear/', views.admin_proveedor_crear_view, name='admin_proveedor_crear'),
    path('panel/proveedores/<int:prov_id>/editar/', views.admin_proveedor_editar_view, name='admin_proveedor_editar'),
    path('panel/proveedores/<int:prov_id>/eliminar/', views.admin_proveedor_eliminar_view, name='admin_proveedor_eliminar'),

    # Comentarios
    path('panel/comentarios/', views.admin_comentarios_view, name='admin_comentarios'),
    path('panel/comentarios/<int:com_id>/eliminar/', views.admin_comentario_eliminar_view, name='admin_comentario_eliminar'),

    # Ventas
    path('panel/ventas/', views.admin_ventas_view, name='admin_ventas'),
    path('panel/ventas/<int:venta_id>/detalle/', views.admin_venta_detalle_view, name='admin_venta_detalle'),

    # Carritos
    path('panel/carritos/', views.admin_carritos_view, name='admin_carritos'),
    path('panel/carritos/<int:carrito_id>/detalle/', views.admin_carrito_detalle_view, name='admin_carrito_detalle'),

    # Stock
    path('panel/stock/', views.admin_stock_view, name='admin_stock'),
    path('panel/stock/crear/', views.admin_stock_crear_view, name='admin_stock_crear'),
]
