from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Cliente, Producto, Categoria, Proveedor
import re

# Formulario de registro de usuarios
class RegisterForm(forms.Form):
    correo = forms.EmailField(
        label='Correo',
        max_length=254,
        widget=forms.EmailInput(attrs={'id':'correo','placeholder':'ejemplo@dominio.com','class':'input'}),
        error_messages={
            'required': 'Debes ingresar tu correo.',
            'invalid': 'Ingrese un correo válido.'
        },
        validators=[EmailValidator(message='Ingrese un correo válido.')]
    )
    username = forms.CharField(label='Usuario', max_length=150, widget=forms.TextInput(attrs={'id':'username','placeholder':'quevedin','class':'input'}), error_messages={'required': 'Debes ingresar tu usuario.'})
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'id':'contrasena','class':'input'}), min_length=8, error_messages={'required': 'Debes ingresar tu contraseña.', 'min_length': 'La contraseña debe tener al menos 8 caracteres.'})
    contrasena2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'id':'contrasena2','class':'input'}), min_length=8, error_messages={'required': 'Debes confirmar tu contraseña.', 'min_length': 'La contraseña debe tener al menos 8 caracteres.'})
    nombres = forms.CharField(label='Nombres', max_length=100, widget=forms.TextInput(attrs={'id':'nombres','placeholder':'Jhonny Antony','class':'input'}), error_messages={'required': 'Debes ingresar tus nombres.'})
    apellidos = forms.CharField(label='Apellidos', max_length=100, widget=forms.TextInput(attrs={'id':'apellidos','placeholder':'Garay Cisnero','class':'input'}), error_messages={'required': 'Debes ingresar tus apellidos.'})
    telefono = forms.CharField(label='Teléfono', max_length=8, min_length=8, widget=forms.TextInput(attrs={'id':'telefono','placeholder':'Teléfono','class':'input'}), error_messages={'required': 'Debes ingresar tu teléfono.', 'min_length': 'El teléfono debe tener 8 dígitos.', 'max_length': 'El teléfono debe tener 8 dígitos.', 'invalid': 'Ingrese un número de teléfono válido.'})
    fecha_nac = forms.DateField(
        label='Fecha de nacimiento',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date','id':'fecha_nac','class':'input'}),
        error_messages={
            'required': 'Debes ingresar tu fecha de nacimiento.',
            'invalid': 'Ingresa una fecha válida.'
        }
    )
    sexo = forms.ChoiceField(label='Sexo', choices=(('', 'Seleccione su sexo'), ('F', 'Femenino'), ('M', 'Masculino')), required=True, widget=forms.Select(attrs={'id':'sexo','class':'input'}), error_messages={'required': 'Debes seleccionar tu sexo.'})
    direccion = forms.CharField(label='Dirección', widget=forms.Textarea(attrs={'id':'direccion','class':'input','rows':'3','placeholder':'Calle, número, ciudad...'}), required=True, error_messages={'required': 'Debes ingresar tu dirección.'})

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError('Ya existe una cuenta con ese correo.')
        return correo

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso.')
        if not re.match(r'^[a-z0-9._-]+$', username):
            raise forms.ValidationError('El usuario solo puede contener minúsculas, números y estos caracteres: . _ -')
        if any(c.isupper() for c in username):
            raise forms.ValidationError('No se permiten mayúsculas en el usuario.')
        return username

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit() or len(telefono) != 8:
            raise forms.ValidationError('El teléfono debe tener 8 dígitos.')
        if telefono[0] not in ['5', '7', '8']:
            raise forms.ValidationError('Ingrese un número de teléfono válido.')
        if Cliente.objects.filter(telefono=telefono).exists():
            raise forms.ValidationError('Ya existe una cuenta con ese número de teléfono.')
        return telefono

    def clean(self):
        cleaned = super().clean()
        if self.errors.get('correo') and len(self.errors['correo']) > 1:
            self.errors['correo'] = [self.errors['correo'][0]]
        p1 = cleaned.get('contrasena')
        p2 = cleaned.get('contrasena2')
        if p1 and p2 and p1 != p2:
            self.add_error('contrasena2', 'Las contraseñas no coinciden.')
        sexo = cleaned.get('sexo')
        if not sexo or sexo == '':
            if not self.errors.get('sexo'):
                self.add_error('sexo', 'Debes seleccionar tu sexo.')
        if not cleaned.get('fecha_nac'):
            if not self.errors.get('fecha_nac'):
                self.add_error('fecha_nac', 'Debes ingresar tu fecha de nacimiento.')
        if not cleaned.get('direccion'):
            if not self.errors.get('direccion'):
                self.add_error('direccion', 'Debes ingresar tu dirección.')
        return cleaned

    def save(self):
        correo = self.cleaned_data['correo']
        username = self.cleaned_data.get('username')
        contrasena = self.cleaned_data['contrasena']
        nombres = self.cleaned_data.get('nombres', '')
        apellidos = self.cleaned_data.get('apellidos', '')
        fecha_nac = self.cleaned_data.get('fecha_nac')
        direccion = self.cleaned_data.get('direccion', '')
        sexo = self.cleaned_data.get('sexo', '')
        telefono = self.cleaned_data.get('telefono', '')
        user = User.objects.create_user(username=username or correo, email=correo, password=contrasena, first_name=nombres, last_name=apellidos)
        cliente = None
        if not user.is_staff and not user.is_superuser:
            cliente = Cliente.objects.create(
                usuario=user,
                nombres=nombres,
                apellidos=apellidos,
                fecha_nacimiento=fecha_nac,
                direccion=direccion,
                sexo=sexo,
                telefono=telefono,
            )
        return user, cliente

# Formulario de login
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={'id':'username','placeholder':'Usuario','class':'input'}),
        error_messages={'required': 'Debes ingresar tu usuario.'}
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'id':'password','placeholder':'Contraseña','class':'input'}),
        error_messages={'required': 'Debes ingresar tu contraseña.'}
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username:
            raise forms.ValidationError('Debes ingresar tu usuario.')
        if not password:
            raise forms.ValidationError('Debes ingresar tu contraseña.')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('El usuario no existe.')
        user_auth = authenticate(username=username, password=password)
        if user_auth is None:
            raise forms.ValidationError('Usuario o contraseña incorrectos.')
        cleaned_data['user_auth'] = user_auth
        return cleaned_data


# Formulario para productos (admin)
class ProductoForm(forms.ModelForm):
    def clean_colores(self):
        colores = self.cleaned_data.get('colores', '')
        if colores:
            items = [c.strip() for c in colores.split(',') if c.strip()]
            for color in items:
                if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúÑñ ]+', color):
                    raise forms.ValidationError('Cada color debe contener solo letras y estar separado por comas. Ejemplo: rojo, azul, negro')
            return ', '.join(items)
        return colores

    def clean_tallas(self):
        tallas = self.cleaned_data.get('tallas', '')
        if tallas:
            items = [t.strip() for t in tallas.split(',') if t.strip()]
            for talla in items:
                # Permite letras (S, M, L, XL) o números con un decimal (35, 36.5)
                if not re.fullmatch(r'([A-Za-z]{1,3}|\d{1,2}(\.\d)?)', talla):
                    raise forms.ValidationError('Cada talla debe ser solo letras (S, M, XL) o números (35, 36.5), separados por comas.')
            return ', '.join(items)
        return tallas

    cantidad_disponible = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'step': '1', 'placeholder': '0', 'inputmode': 'numeric'}))

    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio_real', 'precio_venta', 'cantidad_disponible',
            'imagen', 'categoria', 'proveedor', 'colores', 'tallas', 'genero'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-input', 'placeholder': 'Describe el producto (opcional)'}),
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre del producto', 'maxlength': '100'}),
            'precio_real': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0', 'placeholder': '0.00', 'inputmode': 'decimal'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0', 'placeholder': '0.00', 'inputmode': 'decimal'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'step': '1', 'placeholder': '0', 'inputmode': 'numeric'}),
            'imagen': forms.FileInput(attrs={'class': 'form-input'}),
            'categoria': forms.Select(attrs={'class': 'form-input'}),
            'proveedor': forms.Select(attrs={'class': 'form-input'}),
            'colores': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Ejemplo: rojo, azul, negro'}),
            'tallas': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Ejemplo: S, M o 35, 36.5'}),
            'genero': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        qs = Producto.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe un producto con ese nombre.')
        return nombre

    def clean(self):
        cleaned = super().clean()
        precio_real = cleaned.get('precio_real')
        precio_venta = cleaned.get('precio_venta')
        cantidad = cleaned.get('cantidad_disponible')
        if cantidad in (None, ''):
            cleaned['cantidad_disponible'] = 0
            cantidad = 0

        # Validaciones numéricas
        if precio_real is not None and precio_real <= 0:
            self.add_error('precio_real', 'El costo unitario debe ser mayor a 0.')
        if precio_venta is not None and precio_venta <= 0:
            self.add_error('precio_venta', 'El costo de venta debe ser mayor a 0.')
        if cantidad is not None and cantidad < 0:
            self.add_error('cantidad_disponible', 'La cantidad no puede ser negativa.')
        
        if precio_real is not None and precio_venta is not None:
            if precio_venta < precio_real:
                self.add_error('precio_venta', 'El costo de venta debe ser mayor o igual al costo unitario.')
        
        return cleaned

# Formulario para categorías (admin)
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'maxlength': '100', 'placeholder': 'Nombre de la Categoría'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Descripción (opcional)'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        qs = Categoria.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            if self.instance and self.instance.pk:
                raise forms.ValidationError('Ya existe otra categoría con ese nombre.')
            raise forms.ValidationError('Ya existe una categoría con ese nombre.')
        return nombre

# Formulario para proveedores (admin)
class ProveedorForm(forms.ModelForm):
    correo = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'correo@dominio.com (opcional)'}), error_messages={'invalid': 'Ingresa un correo válido.'})
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'maxlength': '100', 'placeholder': 'Nombre del proveedor'}),
            'telefono': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Teléfono (opcional)'}),
            'direccion': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Dirección (opcional)'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        qs = Proveedor.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe un proveedor con ese nombre.')
        return nombre

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo:
            return None
            
        qs = Proveedor.objects.filter(correo__iexact=correo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe un proveedor con ese correo.')
        return correo

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            qs = Proveedor.objects.filter(telefono__iexact=telefono)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Ya existe un proveedor con ese teléfono.')
        return telefono

# Formulario para movimientos de stock
class StockForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Producto',
        error_messages={
            'required': 'Este campo es obligatorio.',
            'invalid_choice': 'Seleccione un producto válido.'
        }
    )
    tipo = forms.ChoiceField(
        choices=[('', '---------'), ('E', 'Entrada'), ('S', 'Salida')],
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Tipo de Movimiento',
        error_messages={
            'required': 'Seleccione el tipo de movimiento.'
        }
    )

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if not tipo:
            raise forms.ValidationError('Seleccione el tipo de movimiento.')
        return tipo
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Cantidad', 'min': '1'}),
        label='Cantidad',
        error_messages={
            'required': 'Este campo es obligatorio.',
            'invalid': 'Ingrese un número entero válido.',
            'min_value': 'La cantidad debe ser al menos 1.'
        }
    )
    descripcion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Motivo del movimiento (opcional)'}),
        label='Descripción'
    )
