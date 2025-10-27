from django import forms
from django.contrib.auth.models import User
from .models import Cliente

class RegisterForm(forms.Form):
    correo = forms.EmailField(label='Correo', max_length=254, widget=forms.EmailInput(attrs={'id':'correo','placeholder':'ejemplo@dominio.com','class':'input'}))
    username = forms.CharField(label='Usuario', max_length=150, widget=forms.TextInput(attrs={'id':'username','placeholder':'usuario','class':'input'}))
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'id':'contrasena','class':'input'}), min_length=6)
    contrasena2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'id':'contrasena2','class':'input'}), min_length=6)
    nombres = forms.CharField(label='Nombres', max_length=100, widget=forms.TextInput(attrs={'id':'nombres','class':'input'}))
    apellidos = forms.CharField(label='Apellidos', max_length=100, widget=forms.TextInput(attrs={'id':'apellidos','class':'input'}))
    fecha_nac = forms.DateField(label='Fecha de nacimiento', required=True, widget=forms.DateInput(attrs={'type': 'date','id':'fecha_nac','class':'input'}))
    sexo = forms.ChoiceField(label='Sexo', choices=(('F', 'Femenino'), ('M', 'Masculino')), required=True, widget=forms.Select(attrs={'id':'sexo','class':'input'}))
    direccion = forms.CharField(label='Dirección', widget=forms.Textarea(attrs={'id':'direccion','class':'input','rows':'3','placeholder':'Calle, número, ciudad...'}), required=True)

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError('Ya existe una cuenta con ese correo.')
        return correo

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('contrasena')
        p2 = cleaned.get('contrasena2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned

    def save(self):
        # Create User and Cliente
        correo = self.cleaned_data['correo']
        username = self.cleaned_data.get('username')
        contrasena = self.cleaned_data['contrasena']
        nombres = self.cleaned_data.get('nombres', '')
        apellidos = self.cleaned_data.get('apellidos', '')
        fecha_nac = self.cleaned_data.get('fecha_nac')
        direccion = self.cleaned_data.get('direccion', '')
        sexo = self.cleaned_data.get('sexo', '')
        # create the User and fill first/last name
        user = User.objects.create_user(username=username or correo, email=correo, password=contrasena, first_name=nombres, last_name=apellidos)

        # create Cliente only for non-staff/non-superuser accounts (owner/admin shouldn't be a Cliente)
        cliente = None
        if not user.is_staff and not user.is_superuser:
            cliente = Cliente.objects.create(
                usuario=user,
                nombres=nombres,
                apellidos=apellidos,
                fecha_nacimiento=fecha_nac,
                direccion=direccion,
                sexo=sexo,
            )

        return user, cliente
