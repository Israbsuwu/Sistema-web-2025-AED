function openModal(url, nombre) {
    const backdrop = document.getElementById('modal-backdrop');
    const nombreSpan = document.getElementById('modal-nombre-categoria');
    const confirmBtn = document.getElementById('modal-confirm-btn');

    nombreSpan.textContent = nombre;
    confirmBtn.href = url;
    
    backdrop.style.display = 'flex';
}

function closeModal() {
    const backdrop = document.getElementById('modal-backdrop');
    backdrop.style.display = 'none';
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const backdrop = document.getElementById('modal-backdrop');
    if (event.target == backdrop) {
        closeModal();
    }
}

// Desaparecer alertas automáticamente después de 3 segundos
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar mensajes del servidor
    var alerts = [];
    var source = document.getElementById('categorias-alerts-source');
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
            var panel = document.querySelector('.categorias-panel');
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

    // Resaltar categoría
    const params = new URLSearchParams(window.location.search);
    const highlightId = params.get('highlight');
    if (highlightId) {
        const row = document.getElementById('categoria-row-' + highlightId);
        if (row) {
            row.classList.add('categoria-highlight');
            row.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(function(){ row.classList.remove('categoria-highlight'); }, 3200);
        }
    }
});
