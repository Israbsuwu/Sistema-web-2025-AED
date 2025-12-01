function openProvModal(url, nombre) {
    const backdrop = document.getElementById('modal-backdrop-prov');
    const nombreSpan = document.getElementById('modal-nombre-prov');
    const confirmBtn = document.getElementById('modal-confirm-btn-prov');

    nombreSpan.textContent = nombre;
    confirmBtn.href = url;
    
    backdrop.style.display = 'flex';
}

function closeProvModal() {
    const backdrop = document.getElementById('modal-backdrop-prov');
    backdrop.style.display = 'none';
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const backdrop = document.getElementById('modal-backdrop-prov');
    if (event.target == backdrop) {
        closeProvModal();
    }
}

// Desaparecer alertas automáticamente después de 3 segundos
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(function() {
            alerts.forEach(function(alert) {
                alert.style.transition = 'opacity 0.5s ease, top 0.5s ease';
                alert.style.opacity = '0';
                alert.style.top = '-100px';
                setTimeout(function() { alert.remove(); }, 500);
            });
        }, 3000);
    }

    // Resaltar proveedor
    const params = new URLSearchParams(window.location.search);
    const highlightId = params.get('highlight');
    if (highlightId) {
        const row = document.getElementById('proveedor-row-' + highlightId);
        if (row) {
            row.classList.add('proveedor-highlight');
            row.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(function(){ row.classList.remove('proveedor-highlight'); }, 3200);
        }
    }
});
