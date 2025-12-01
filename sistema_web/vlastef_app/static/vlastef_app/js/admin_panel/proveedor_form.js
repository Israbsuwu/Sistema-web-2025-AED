document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('proveedor-form');
    const nombre = document.getElementById('id_nombre');
    const telefono = document.getElementById('id_telefono');
    if (!form || !nombre) 
        return;

    // Auto-dismiss de mensajes del servidor (3s)
    const serverAlerts = document.querySelectorAll('.messages .alert');
    if (serverAlerts.length) {
        setTimeout(function(){
            serverAlerts.forEach(function(alert){
                alert.style.transition = 'opacity 0.5s ease, top 0.5s ease';
                alert.style.opacity = '0';
                alert.style.top = '-100px';
                setTimeout(function(){ alert.remove(); }, 500);
            });
        }, 3000);
    }

    function showInlineAlert(text, type) {
        let container = document.querySelector('.messages');
        if (!container) {
            container = document.createElement('div');
            container.className = 'messages';
            const panel = document.querySelector('.form-card');
            if (panel) 
                panel.prepend(container);
        }
        const alert = document.createElement('div');
        alert.className = 'alert ' + (type || 'error');
        alert.textContent = text;
        container.innerHTML = '';
        container.appendChild(alert);

        setTimeout(function(){
            alert.style.transition = 'opacity 0.5s ease, top 0.5s ease';
            alert.style.opacity = '0';
            alert.style.top = '-100px';
            setTimeout(function(){ alert.remove(); }, 500);
        }, 3000);
    }

    // Optimiza campo teléfono: solo dígitos y teclado numérico
    if (telefono) {
        telefono.setAttribute('inputmode', 'numeric');
        telefono.addEventListener('input', function () {
        const cleaned = this.value.replace(/\D+/g, '').slice(0,8);
        if (cleaned !== this.value) 
            this.value = cleaned;
        });
    }

    form.addEventListener('submit', function (e) {
        const nombreVal = (nombre.value || '').trim();
        if (!nombreVal) {
            e.preventDefault();
            showInlineAlert('El nombre del proveedor es obligatorio', 'error');
            nombre.focus();
            return;
        }

        if (telefono) {
            const telVal = (telefono.value || '').trim();
            if (telVal) {
                const patternOk = /^[578]\d{7}$/.test(telVal); 
                if (!patternOk) {
                e.preventDefault();
                showInlineAlert('Ingrese un número de teléfono válido.', 'error');
                telefono.focus();
                return;
                }
            }
        }
    });
});
