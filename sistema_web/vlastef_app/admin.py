from django.contrib import admin
from .models import Cliente, Categoria, Producto, Proveedor, Venta, DetalleVenta, Comentario, Carrito, CarritoDetalle, Stock

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Comentario)
admin.site.register(Carrito)
admin.site.register(CarritoDetalle)
admin.site.register(Stock)