# Sistema-web-2025-AED

## Instalación

1. Creas una carpeta en tu pc y la abres con VSCode.
2. Usando git abres la ubicación de la carpeta y clonas el repositorio:

```bash
git clone https://github.com/Israbsuwu/Sistema-web-2025-AED.git
```

3. Accedes a la ubicación de la carpeta:

```bash
cd SISTEMA-WEB-2025-AED
```

4. Coloca en la terminal lo siguiente para instalar las dependencias:

```bash
pip install -r requirements.txt
```

5. Luego a la carpeta del proyecto Django:

```bash
cd sistema_web
```

6. En PostgreSQL crea una base de datos con el nombre de:

```bash
bd_web
```
Tanto el USER como el PASSWORD de su PostgreSQL debe de ser el mismo que está puesto en el "settings.py" del proyecto.
Si no es el mismo entonces modifica el settings.py poniendo tu USER y PASSWORD igualito al que tienes en postgres.
Eso se encuentra a partir de la línea 82 y 83 de settings.py, después guarda los cambios y procede con los siguientes pasos.

7. Ahora volviendo al proyecto realiza las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

8. Una vez completado ve a la base de datos (postgres) para verificar si se realizaron las migraciones correctamente.
9. Regresa al proyecto y crea un superusuario para poder acceder:

```bash
python manage.py createsuperuser
```

10. Te pedirá ingresar un nombre de usuario, correo y contraseña (no lo olvides).
11. Una vez creado es momento de ejecutar el proyecto:

```bash
python manage.py runserver
```

12. En la terminal encontrarás un enlace donde al presionar 'control + clic' te llevará a la página web.
\
Estando en la página tienes la opción de iniciar sesión o registrar una cuenta.\
Puedes iniciar sesión con el superusuario creado poniéndolo en el login junto con su contraseña.
