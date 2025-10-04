from django.contrib import admin
from web.models import User, Categoria, Producto, Comentarios, Orden, OrdenItem

# Register your models here.
admin.site.register(User)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Comentarios)
admin.site.register(Orden)
admin.site.register(OrdenItem)