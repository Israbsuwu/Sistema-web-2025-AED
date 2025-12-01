function openComentarioModal(url, cliente, producto) {
    const backdrop = document.getElementById('modal-backdrop-com');
    document.getElementById('modal-cliente-com').textContent = cliente;
    document.getElementById('modal-producto-com').textContent = producto;
    document.getElementById('modal-confirm-btn-com').href = url;
    backdrop.style.display = 'flex';
}

function closeComentarioModal() {
    const backdrop = document.getElementById('modal-backdrop-com');
    backdrop.style.display = 'none';
}

window.addEventListener('click', function(ev){
    const backdrop = document.getElementById('modal-backdrop-com');
    if (ev.target === backdrop) {
        closeComentarioModal();
    }
});

document.addEventListener('DOMContentLoaded', function(){
    // Mostrar mensajes del servidor
    var alerts = [];
    var source = document.getElementById('comentarios-alerts-source');
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
});
