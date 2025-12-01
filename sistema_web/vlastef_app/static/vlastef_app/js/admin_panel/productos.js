function openProductoModal(url, nombre) {
    const backdrop = document.getElementById('modal-backdrop-producto');
    const nombreSpan = document.getElementById('modal-nombre-producto');
    const confirmBtn = document.getElementById('modal-confirm-btn-producto');

    nombreSpan.textContent = nombre;
    confirmBtn.href = url;
    
    backdrop.style.display = 'flex';
}

function closeProductoModal() {
    const backdrop = document.getElementById('modal-backdrop-producto');
    backdrop.style.display = 'none';
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const backdrop = document.getElementById('modal-backdrop-producto');
    if (event.target == backdrop) {
        closeProductoModal();
    }
}

// Desaparecer alertas automáticamente después de 3 segundos
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
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

    // Resaltar un producto si viene ?highlight=ID (desde detalle de categoría)
    const params = new URLSearchParams(window.location.search);
    const highlightId = params.get('highlight');
    if (highlightId) {
        const row = document.getElementById('producto-row-' + highlightId);
        if (row) {
            row.classList.add('producto-highlight');
            row.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(function(){ row.classList.remove('producto-highlight'); }, 3200);
        }
    }

    // Ampliar imagen al hacer clic en miniatura
    const thumbnails = document.querySelectorAll('.producto-miniatura');
    const viewerBackdrop = document.getElementById('image-viewer-backdrop');
    const viewerImg = document.getElementById('image-viewer-img');

    function openImageViewer(src, altText) {
        if (!viewerBackdrop || !viewerImg) return;
        viewerImg.src = src;
        viewerImg.alt = altText || 'Imagen producto ampliada';
        viewerBackdrop.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    function closeImageViewer() {
        if (!viewerBackdrop) return;
        viewerBackdrop.style.display = 'none';
        viewerImg.src = '';
        document.body.style.overflow = '';
    }

    thumbnails.forEach(function(img){
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', function(){
            openImageViewer(img.src, img.alt);
        });
    });

    if (viewerBackdrop) {
        viewerBackdrop.addEventListener('click', function(e){
            if (e.target === viewerBackdrop) {
                closeImageViewer();
            }
        });
        // Cerrar con ESC
        document.addEventListener('keyup', function(e){
            if (e.key === 'Escape' && viewerBackdrop.style.display === 'flex') {
                closeImageViewer();
            }
        });
    }
});
