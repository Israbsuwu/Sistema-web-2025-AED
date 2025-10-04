from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Categoria(models.Model):
    nombre = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Comentarios(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="comentario")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comentario")
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.producto.nombre}"

class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordenes")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    compra_finalizada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Orden {self.id} de {self.usuario.username}"

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Orden {self.orden.id})"

    def subtotal(self):
        return self.cantidad * self.producto.precio