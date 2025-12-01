document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.categoria-form');
    const nombre = document.getElementById('nombre');
    if (!form || !nombre) 
        return;

    // Mostrar mensajes del servidor
    var alerts = [];
    var source = document.getElementById('categoria-form-alerts-source');
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

    function showInlineAlert(text, type) {
            // Busca contenedor de mensajes y agrega un alert similar al framework
            let container = document.querySelector('.messages');
            if (!container) {
                container = document.createElement('div');
                container.className = 'messages';
                const panel = document.body;
                if (panel) panel.prepend(container);
            }
            const alert = document.createElement('div');
            alert.className = 'alert ' + (type || 'error');
            alert.textContent = text;
            container.innerHTML = '';
            container.appendChild(alert);

        // Desaparecer 
        setTimeout(function(){
            alert.style.transition = 'opacity 0.5s ease, top 0.5s ease';
            alert.style.opacity = '0';
            alert.style.top = '-100px';
            setTimeout(function(){ alert.remove(); }, 500);
        }, 3000);
    }

    form.addEventListener('submit', function (e) {
        const value = (nombre.value || '').trim();
        if (!value) {
            e.preventDefault();
            // Mostrar mensaje obligatorio con estilo de alerta
            showInlineAlert('El nombre de la categoría es obligatorio', 'error');
            nombre.focus();
        }
    });
});
