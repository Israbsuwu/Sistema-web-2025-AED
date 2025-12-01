document.addEventListener('DOMContentLoaded', function() {
    var DURATION = 3000;

    function showAlert(message, type) {
        var alertDiv = document.createElement('div');
        alertDiv.className = 'alert ' + (type || '');
        alertDiv.textContent = message;
        document.body.appendChild(alertDiv);
        setTimeout(function() {
            alertDiv.style.transition = 'opacity 0.5s ease, top 0.5s ease';
            alertDiv.style.opacity = '0';
            alertDiv.style.top = '-100px';
            setTimeout(function() { alertDiv.remove(); }, 500);
        }, 3000);
    }

    var alerts = [];
    var source = document.getElementById('stock-alerts-source');
    if (source) {
        var items = source.querySelectorAll('.alert-item');
        items.forEach(function(el){
            alerts.push({ text: el.textContent || '', type: el.getAttribute('data-type') || 'error' });
        });
    }

    if (alerts.length) {
        var hasErrors = alerts.some(function(a){ return (a.type || 'error').indexOf('error') !== -1; });
        if (hasErrors) {
            showAlert('Por favor, complete los campos obligatorios.', 'error');
        } else {
            var combinedInfo = alerts.map(function(a){ return a.text; }).join('\n');
            showAlert(combinedInfo, 'info');
        }
    }

    // Prevenir ingreso de signo menos en cantidad
    const cantidadInput = document.getElementById('id_cantidad');
    if (cantidadInput) {
        cantidadInput.addEventListener('keydown', function(e) {
            if (e.key === '-') {
                e.preventDefault();
            }
        });
    }

    const form = document.querySelector('.stock-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const producto = document.getElementById('id_producto');
            const tipo = document.getElementById('id_tipo');
            const cantidad = document.getElementById('id_cantidad');
            const prodVal = producto ? (producto.value || '').trim() : '';
            const tipoVal = tipo ? tipo.value : '';
            const cantVal = cantidad ? (cantidad.value || '').trim() : '';
            let hasSomeFilled = prodVal || tipoVal || cantVal;
            let message = '';
            let missing = [];
            if (!prodVal) missing.push('Producto');
            if (!tipoVal) missing.push('Tipo de movimiento');
            if (!cantVal) missing.push('Cantidad');
            else {
                const cantNum = parseInt(cantVal);
                if (isNaN(cantNum) || cantNum < 1) {
                    message = 'La cantidad de entrada o salida no debe de ser 0.';
                    e.preventDefault();
                    showAlert(message, 'error');
                    cantidad.focus();
                    return;
                }
            }
            if (missing.length > 0) {
                e.preventDefault();
                if (!hasSomeFilled) {
                    message = 'Complete los campos obligatorios';
                } else {
                    message = 'Complete: ' + missing.join(', ');
                }
                showAlert(message, 'error');
                if (!prodVal) producto.focus();
                else if (!tipoVal) tipo.focus();
                else if (!cantVal) cantidad.focus();
                return;
            }
        });
    }

    // Mostrar mensajes del servidor para stock.html
    var alerts = [];
    var source = document.getElementById('stock-alerts-source');
    if (source) {
        var items = source.querySelectorAll('.alert-item');
        items.forEach(function(el){
            alerts.push({ text: el.textContent || '', type: el.getAttribute('data-type') || 'success' });
        });
    }

    if (alerts.length) {
        alerts.forEach(function(alertData){
            showAlert(alertData.text, alertData.type || 'success');
        });
    }

    // Resaltar producto
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
});
