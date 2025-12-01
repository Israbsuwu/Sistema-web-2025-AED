function togglePasswordReset() {
    var area = document.getElementById('password-reset-area');
    if (area.style.display === 'none') {
        area.style.display = 'block';
    } else {
        area.style.display = 'none';
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
});

// Modal y validación para cambio de contraseña 
document.addEventListener('DOMContentLoaded', function() {
    var btnOpenModal = document.getElementById('btn-open-reset-modal');
    var modalBackdrop = document.getElementById('modal-backdrop-reset');
    var btnCancelModal = document.getElementById('btn-cancel-reset-modal');
    var btnConfirmModal = document.getElementById('btn-confirm-reset-modal');
    var newPasswordInput = document.getElementById('new_password');
    var passwordForm = newPasswordInput ? newPasswordInput.closest('form') : null;

    if (!btnOpenModal || !modalBackdrop || !btnConfirmModal || !newPasswordInput || !passwordForm) {
        return;
    }

    btnOpenModal.addEventListener('click', function() {
        var pwd = (newPasswordInput.value || '').trim();
        if (pwd.length < 8) {
            showAlert('La contraseña debe tener al menos 8 caracteres.', 'error');
            newPasswordInput.focus();
            return;
        }
        modalBackdrop.style.display = 'flex';
    });

    if (btnCancelModal) {
        btnCancelModal.addEventListener('click', function() {
            modalBackdrop.style.display = 'none';
        });
    }

    btnConfirmModal.addEventListener('click', function() {
        var url = btnConfirmModal.getAttribute('data-reset-url');
        if (url) {
            passwordForm.setAttribute('action', url);
        }
        passwordForm.submit();
    });

    // Cerrar modal al hacer clic fuera
    modalBackdrop.addEventListener('click', function(e) {
        if (e.target === modalBackdrop) {
            modalBackdrop.style.display = 'none';
        }
    });
});

function showAlert(msg, type) {
    var alertDiv = document.createElement('div');
    alertDiv.className = 'alert ' + (type || '');
    alertDiv.textContent = msg;
    document.body.appendChild(alertDiv);
    setTimeout(function() {
        alertDiv.style.transition = 'opacity 0.5s ease, top 0.5s ease';
        alertDiv.style.opacity = '0';
        alertDiv.style.top = '-100px';
        setTimeout(function() { alertDiv.remove(); }, 500);
    }, 3000);
}

// Validación del formulario de edición
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.editar-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const nombres = document.getElementById('nombres').value.trim();
            const apellidos = document.getElementById('apellidos').value.trim();
            const email = document.getElementById('email').value.trim();
            const telefono = document.getElementById('telefono').value.trim();

            if (!nombres) {
                e.preventDefault();
                showAlert('El nombre es obligatorio.', 'error');
                document.getElementById('nombres').focus();
                return;
            }

            if (!apellidos) {
                e.preventDefault();
                showAlert('Los apellidos son obligatorios.', 'error');
                document.getElementById('apellidos').focus();
                return;
            }

            if (!email) {
                e.preventDefault();
                showAlert('El email es obligatorio.', 'error');
                document.getElementById('email').focus();
                return;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                e.preventDefault();
                showAlert('Ingresa un email válido.', 'error');
                document.getElementById('email').focus();
                return;
            }

            if (!telefono) {
                e.preventDefault();
                showAlert('El teléfono es obligatorio.', 'error');
                document.getElementById('telefono').focus();
                return;
            }

            if (!/^[578]\d{7}$/.test(telefono)) {
                e.preventDefault();
                showAlert('Ingrese un número de teléfono válido.', 'error');
                document.getElementById('telefono').focus();
                return;
            }
        });
    }
});
