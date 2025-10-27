from django.db import models
from django.contrib.auth.models import User

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ])
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Comentario(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='comentarios')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    calificacion = models.IntegerField(default=0) 

    def __str__(self):
        return f"Comentario de {self.cliente} en {self.producto}"


class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='carritos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True) 

    def __str__(self):
        return f"Carrito de {self.cliente} ({'Activo' if self.activo else 'Cerrado'})"


class CarritoDetalle(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


class Stock(models.Model):
    MOVIMIENTO_TIPO = [
        ('E', 'Entrada'),
        ('S', 'Salida'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos_stock')
    tipo = models.CharField(max_length=1, choices=MOVIMIENTO_TIPO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.producto.nombre} ({self.cantidad})"
