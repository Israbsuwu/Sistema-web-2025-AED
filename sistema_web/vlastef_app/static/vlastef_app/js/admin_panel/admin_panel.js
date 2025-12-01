// Minimizar/expandir al hacer clic en el área del logo-panel
document.addEventListener('DOMContentLoaded', function() {
    var logoPanel = document.querySelector('.logo-panel');
    var sidebar = document.querySelector('.sidebar');
    if (logoPanel && sidebar) {
        logoPanel.style.cursor = 'pointer';
        logoPanel.addEventListener('click', function() {
            sidebar.classList.toggle('sidebar-collapsed');
        });
    }
});
