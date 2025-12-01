document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('producto-form');
    const precioReal = document.getElementById('id_precio_real');
    const precioVenta = document.getElementById('id_precio_venta');
    const cantidad = document.getElementById('id_cantidad_disponible');
    const imagenInput = document.getElementById('id_imagen');
    const preview = document.getElementById('imagen-preview');
    const alertContainer = document.getElementById('alert-container');

    // Función para mostrar alertas
    function showAlert(message, type = 'error') {
        const alert = document.createElement('div');
        alert.className = `alert ${type}`;
        alert.textContent = message;
        alertContainer.appendChild(alert);

        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, top 0.5s ease';
            alert.style.opacity = '0';
            alert.style.top = '-100px';
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    }

    // Auto-dismiss para alertas existentes (del backend)
    const existingAlerts = document.querySelectorAll('.alert');
    if (existingAlerts.length > 0) {
        setTimeout(() => {
            existingAlerts.forEach(alert => {
                alert.style.transition = 'opacity 0.5s ease, top 0.5s ease';
                alert.style.opacity = '0';
                alert.style.top = '-100px';
                setTimeout(() => alert.remove(), 500);
            });
        }, 3000);
    }

    // Prevenir entrada de caracteres no numéricos (excepto punto decimal)
    function preventNonNumeric(e) {
        // Permitir: backspace, delete, tab, escape, enter, punto
        if ([46, 8, 9, 27, 13, 110, 190].indexOf(e.keyCode) !== -1 ||
            // Permitir: Ctrl+A, Command+A
            (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
            // Permitir: home, end, left, right, down, up
            (e.keyCode >= 35 && e.keyCode <= 40)) {
            return;
        }
        // Asegurar que sea un número
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    }

    // Prevenir entrada de caracteres no numéricos (excepto números enteros)
    function preventNonInteger(e) {
        if ([8, 9, 27, 13].indexOf(e.keyCode) !== -1 ||
            (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
            (e.keyCode >= 35 && e.keyCode <= 40)) {
            return;
        }
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    }

    if (precioReal) precioReal.addEventListener('keydown', preventNonNumeric);
    if (precioVenta) precioVenta.addEventListener('keydown', preventNonNumeric);
    if (cantidad) cantidad.addEventListener('keydown', preventNonInteger);

    // Validación al enviar el formulario
    if (form) {
        form.addEventListener('submit', function(e) {
            let hasError = false;
            alertContainer.innerHTML = ''; // Limpiar alertas anteriores

            // Validar campos requeridos
            const requiredFields = form.querySelectorAll('[required]');
            const missing = [];
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    missing.push(field);
                    field.classList.add('input-error');
                } else {
                    field.classList.remove('input-error');
                }
            });

            if (missing.length === requiredFields.length) {
                // Todos vacíos: mensaje único genérico
                showAlert('Por favor, complete los campos obligatorios.');
                hasError = true;
            } else if (missing.length > 0) {
                // Algunos faltan: un solo mensaje listándolos
                const labels = missing.map(f => {
                    const label = document.querySelector(`label[for="${f.id}"]`);
                    return label ? label.textContent.replace('*', '').trim() : (f.name || 'campo');
                });
                showAlert('Faltan los siguientes campos: ' + labels.join(', ') + '.');
                hasError = true;
            }

            // Validar valores numéricos solo si NO hay campos faltantes
            if (missing.length === 0) {
                const pr = parseFloat(precioReal.value);
                const pv = parseFloat(precioVenta.value);
                const cant = parseInt(cantidad.value);

                if (precioReal.value && pr <= 0) {
                    showAlert('El Costo Unitario debe ser mayor a 0.');
                    hasError = true;
                }
                if (precioVenta.value && pv <= 0) {
                    showAlert('El Costo de Venta debe ser mayor a 0.');
                    hasError = true;
                }
                if (cantidad.value && cant < 0) {
                    showAlert('La cantidad no puede ser negativa.');
                    hasError = true;
                }
                
                if (precioReal.value && precioVenta.value && pv < pr) {
                    showAlert('El Costo de Venta debe ser mayor o igual al Costo Unitario.');
                    hasError = true;
                }
            }

            if (hasError) {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }

    // Vista previa de imagen
    if (imagenInput && preview) {
        imagenInput.addEventListener('change', function(e) {
            const file = e.target.files && e.target.files[0];
            if (file) {
                const url = URL.createObjectURL(file);
                preview.src = url;
                preview.style.display = 'inline-block';
                const currentImg = document.getElementById('imagen-actual');
                if(currentImg) currentImg.style.display = 'none';
            }
        });
    }
});
