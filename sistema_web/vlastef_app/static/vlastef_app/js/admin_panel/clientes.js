function openModal(type, url, username) {
    const backdrop = document.getElementById('modal-backdrop');
    const title = document.getElementById('modal-title');
    const message = document.getElementById('modal-message');
    const warning = document.getElementById('modal-warning');
    const confirmBtn = document.getElementById('modal-confirm-btn');

    backdrop.style.display = 'flex';
    confirmBtn.href = url;

    if (type === 'eliminar') {
        title.textContent = '¿Eliminar usuario?';
        message.textContent = `¿Estás seguro de que deseas eliminar al usuario "${username}"?`;
        warning.style.display = 'block';
        confirmBtn.className = 'btn-confirmar btn-danger';
        confirmBtn.textContent = 'Sí, eliminar permanentemente';
    } else if (type === 'desactivar') {
        title.textContent = '¿Desactivar usuario?';
        message.textContent = `¿Estás seguro de que deseas desactivar al usuario "${username}"? El usuario no podrá iniciar sesión.`;
        warning.style.display = 'none';
        confirmBtn.className = 'btn-confirmar btn-warning';
        confirmBtn.textContent = 'Sí, desactivar';
    } else if (type === 'activar') {
        title.textContent = '¿Activar usuario?';
        message.textContent = `¿Estás seguro de que deseas activar al usuario "${username}"?`;
        warning.style.display = 'none';
        confirmBtn.className = 'btn-confirmar btn-success';
        confirmBtn.textContent = 'Sí, activar';
    }
}

function closeModal() {
    document.getElementById('modal-backdrop').style.display = 'none';
}

// Cerrar modal al hacer clic fuera
document.addEventListener('DOMContentLoaded', function() {
    const backdrop = document.getElementById('modal-backdrop');
    if (backdrop) {
        backdrop.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
    }

    // Mostrar mensajes del servidor
    var alerts = [];
    var source = document.getElementById('clientes-alerts-source');
    if (source) {
        var items = source.querySelectorAll('.alert-item');
        items.forEach(function(el){
            alerts.push({ text: el.textContent || '', type: el.getAttribute('data-type') || 'success' });
        });
    }

    if (alerts.length) {
        // Crear contenedor de mensajes
        var container = document.querySelector('.messages');
        if (!container) {
            container = document.createElement('div');
            container.className = 'messages';
            var panel = document.body;
            if (panel) panel.prepend(container);
        }
        alerts.forEach(function(alertData){
            var alert = document.createElement('div');
            alert.className = 'alert ' + (alertData.type || 'success');
            alert.setAttribute('role', 'alert');
            alert.textContent = alertData.text;
            container.appendChild(alert);
        });

        // Auto-dismiss (3s)
        setTimeout(function(){
            var serverAlerts = document.querySelectorAll('.messages .alert');
            serverAlerts.forEach(function(alert){
                alert.style.transition = 'opacity 0.5s ease, top 0.5s ease';
                alert.style.opacity = '0';
                alert.style.top = '-100px';
                setTimeout(function(){ if (alert && alert.parentNode) alert.remove(); }, 500);
            });
        }, 3000);
    }

    // Desaparecer alertas automáticamente después de 3 segundos
    const alertsOld = document.querySelectorAll('.alert');
    if (alertsOld.length > 0) {
        setTimeout(function() {
            alerts.forEach(function(alert) {
                // Efecto de desvanecimiento y deslizamiento hacia arriba
                alert.style.transition = 'opacity 0.5s ease, top 0.5s ease';
                alert.style.opacity = '0';
                alert.style.top = '-100px'; // Mover hacia arriba fuera de la pantalla
                setTimeout(function() {
                    alert.remove();
                }, 500); // Esperar a que termine la transición para eliminar del DOM
            });
        }, 3000); // 3 segundos de espera
    }
});
