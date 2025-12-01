document.addEventListener('DOMContentLoaded', function(){
    // Mostrar mensajes del servidor
    var alerts = [];
    var source = document.getElementById('venta-detalle-alerts-source');
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