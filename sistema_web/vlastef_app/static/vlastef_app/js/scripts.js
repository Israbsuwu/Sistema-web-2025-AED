// Pequeñas utilidades compartidas para la demo
(function(){
  window.alx = window.alx || {};

  // Fallback para openCart si no existe
  window.openCart = window.openCart || function(){
    const cart = JSON.parse(sessionStorage.getItem('alx_cart')||'[]');
    alert('Carrito (demo): ' + cart.reduce((s,i)=>s+i.qty,0) + ' artículos');
  };

  // Formato simple
  window.formatCurrency = function(v){ return '$' + (Number(v)||0).toFixed(2); };

  // Búsqueda simple: filtra por título almacenado en products y recarga Menu_Principal
  window.doSearch = function(q){
    try{
      const prods = JSON.parse(sessionStorage.getItem('alx_products')||'[]');
      const results = prods.filter(p=>p.title.toLowerCase().includes(q.toLowerCase()));
      sessionStorage.setItem('alx_search_results', JSON.stringify(results));
      // redirigir al listado
      window.location.href = 'pagina_principal/Menu_Principal.html';
    }catch(e){ window.location.href = 'pagina_principal/Menu_Principal.html'; }
  };

  // Helper seguro para mostrar perfil (si no existe perfil script)
  window.safeShowProfile = function(){
    const panel = document.getElementById('profilePanel'); if(panel) panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
  };
})();
