// home.js - cleaned and wrapped to avoid HTML fragments and early DOM access
// Exposes a few global helpers: addToCart, buyNow, openCart, changeQty, removeFromCart

(function(){
  'use strict';

  const PATH_PERFIL = '../perfil_Usuario/perfil-usuario-app/src/views/Perfil_Usuario_Cliente.html';
  const PATH_LOGIN = '../Loggin/index.html';

  function getParam(name){ try{ const url = new URL(location.href); return url.searchParams.get(name); }catch(e){ return null; } }

  function safeGet(id){ return document.getElementById(id) || null; }

  // All UI wiring runs after DOM is ready
  window.addEventListener('DOMContentLoaded', () => {

    function populateProfileFromSession(){
      try{
        const raw = sessionStorage.getItem('alx_user');
        if(!raw) return false;
        const user = JSON.parse(raw);
        const profileImg = user.foto || 'https://via.placeholder.com/80';
        const elProfile = safeGet('profileImg'); if(elProfile) elProfile.src = profileImg;
        const mini = safeGet('profileImgMini'); if(mini) mini.src = user.foto || 'https://via.placeholder.com/40';
        const nameEl = safeGet('profileName'); if(nameEl) nameEl.textContent = user.nombre || 'Usuario';
        const emailEl = safeGet('profileEmail'); if(emailEl) emailEl.textContent = user.correo || '';
        const toggle = safeGet('profileToggle'); if(toggle) toggle.style.display = 'flex';
        return true;
      }catch(e){ return false; }
    }

    function showAfterLogin(){
      const overlay = safeGet('lockedOverlay'); if(overlay) overlay.style.display = 'none';
      const main = safeGet('mainContent'); if(main) main.setAttribute('aria-hidden','false');
      sessionStorage.setItem('alx_logged','1');
      populateProfileFromSession();
    }

    // profile toggle: delegate click handling
    document.addEventListener('click', function(e){
      const panel = safeGet('profilePanel');
      const toggle = safeGet('profileToggle');
      if(toggle && (toggle.contains(e.target) || toggle === e.target)){
        if(panel) panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
        return;
      }
      if(panel && !panel.contains(e.target) && !(toggle && toggle.contains(e.target))) panel.style.display = 'none';
    });

    // navigation helper
    window.navigateTo = function(section){
      const panel = safeGet('profilePanel'); if(panel) panel.style.display = 'none';
      switch(section){
        case 'registrarse': window.location.href = '../Registro/index.html'; break;
        default: console.log('Navigate to', section); break;
      }
    };

    // profile photo modal functions
    window.openPhotoModal = function(){ const modal = safeGet('photoModal'); if(modal) modal.style.display = 'flex'; const preview = safeGet('photoPreview'); if(preview) preview.style.display = 'none'; };
    window.closePhotoModal = function(){ const modal = safeGet('photoModal'); if(modal) modal.style.display = 'none'; const input = safeGet('photoInput'); if(input) input.value = ''; };
    window.savePhoto = function(){
      const input = safeGet('photoInput'); if(!input || !input.files || !input.files[0]){ alert('Por favor, selecciona una foto primero'); return; }
      const newPhotoUrl = URL.createObjectURL(input.files[0]);
      const p = safeGet('profileImg'); if(p) p.src = newPhotoUrl; const pm = safeGet('profileImgMini'); if(pm) pm.src = newPhotoUrl;
      try{ const userData = JSON.parse(sessionStorage.getItem('alx_user')||'{}'); userData.foto = newPhotoUrl; sessionStorage.setItem('alx_user', JSON.stringify(userData)); }catch(e){ console.error(e); }
      window.closePhotoModal(); alert('Foto de perfil actualizada correctamente');
    };

    const photoInputEl = safeGet('photoInput');
    if(photoInputEl){
      photoInputEl.addEventListener('change', function(e){
        const file = e.target.files[0]; if(!file) return; const reader = new FileReader();
        reader.onload = function(ev){ const preview = safeGet('photoPreview'); if(preview){ preview.src = ev.target.result; preview.style.display = 'block'; } };
        reader.readAsDataURL(file);
      });
    }

    // startup: check session
    const hasSession = getParam('logged') === '1' || sessionStorage.getItem('alx_logged') === '1';
    if(!hasSession || !populateProfileFromSession()){
      const lock = safeGet('lockedOverlay'); if(lock) lock.style.display = 'flex';
    } else showAfterLogin();

    // search helper
    const searchBtn = safeGet('searchBtn');
    if(searchBtn){ searchBtn.addEventListener('click', () => { const input = safeGet('searchInput'); if(!input || !input.value.trim()){ return alert('Escribe algo para buscar.'); } alert('Buscar: ' + input.value.trim()); }); }

    // product markup is rendered server-side in the template. Wire up small client interactions below.
    const productGrid = safeGet('productGrid');
    const resultsCount = safeGet('resultsCount');
    const sortSelect = safeGet('sortSelect');
    const categories = safeGet('categories');

    // if there are server-rendered product cards, wire delegated clicks for add/buy
    if(productGrid){
      productGrid.addEventListener('click', function(ev){
        const addBtn = ev.target.closest('.add-to-cart');
        const buyBtn = ev.target.closest('.buy-now');
        if(addBtn){ const card = addBtn.closest('.product-card'); if(card){ const id = card.dataset.id; const price = Number(card.dataset.price||0); const title = card.dataset.title||''; const img = card.dataset.img||''; window.addToCart && window.addToCart(id, { title, price, img }); } }
        if(buyBtn){ const card = buyBtn.closest('.product-card'); if(card){ const id = card.dataset.id; window.buyNow && window.buyNow(id); } }
      });
    }

    // cart in sessionStorage
    function getCart(){ try{ return JSON.parse(sessionStorage.getItem('alx_cart')||'[]'); }catch(e){ return []; } }
    function saveCart(c){ sessionStorage.setItem('alx_cart', JSON.stringify(c)); updateCartIndicator(); }

    window.addToCart = function(id){ const prod = sampleProducts.find(p=>p.id===id); if(!prod) return; const cart = getCart(); const existing = cart.find(i=>i.id===id); if(existing) existing.qty += 1; else cart.push({ id:prod.id, title:prod.title, price:prod.price, qty:1, img:prod.img }); saveCart(cart); alert('Añadido al carrito: ' + prod.title); };
    window.buyNow = function(id){ window.addToCart && window.addToCart(id); window.openCart && window.openCart(); };

    const cartCountEl = safeGet('cart-count');
    const cartButton = safeGet('cart-button'); if(cartButton) cartButton.addEventListener('click', () => window.openCart && window.openCart());

    function updateCartIndicator(){ if(!cartCountEl) return; const cart = getCart(); const count = cart.reduce((s,i)=>s+i.qty,0); cartCountEl.textContent = `Carrito (${count})`; }

    const cartModal = safeGet('cartModal');
    const cartList = safeGet('cartList');
    const cartEmpty = safeGet('cartEmpty');
    const subtotalEl = safeGet('subtotal');
    const ivaEl = safeGet('iva');
    const discountEl = safeGet('discount');
    const totalEl = safeGet('total');
    const clearCartBtn = safeGet('clearCart');
    const buyBtn = safeGet('buyBtn');
    const closeCartBtn = safeGet('closeCart');
    const selectAll = safeGet('selectAll');

    window.openCart = function(){ if(cartModal){ renderCart(); cartModal.style.display = 'flex'; cartModal.setAttribute('aria-hidden','false'); } };
    if(closeCartBtn) closeCartBtn.addEventListener('click', () => { if(cartModal){ cartModal.style.display='none'; cartModal.setAttribute('aria-hidden','true'); } });

    function renderCart(){
      const cart = getCart();
      if(!cartList) return;
      cartList.innerHTML = '';
      if(!cart || cart.length===0){ if(cartEmpty) cartEmpty.style.display = 'block'; cartList.style.display = 'none'; if(subtotalEl) subtotalEl.textContent = '$0.00'; if(ivaEl) ivaEl.textContent = '$0.00'; if(discountEl) discountEl.textContent = '-$0.00'; if(totalEl) totalEl.textContent = '$0.00'; updateCartIndicator(); return; }
      if(cartEmpty) cartEmpty.style.display = 'none'; cartList.style.display = 'flex';
      cart.forEach(item=>{
        const row = document.createElement('div');
        row.style.display='flex';row.style.gap='8px';row.style.alignItems='center';row.style.borderBottom='1px solid #f6f6f6';row.style.padding='8px 0';
        row.innerHTML = `
          <input type="checkbox" data-id="${item.id}" style="width:18px;height:18px">
          <img src="${item.img}" style="width:60px;height:60px;border-radius:6px;object-fit:cover">
          <div style="flex:1">
            <div style="font-size:14px">${escapeHtml(item.title)}</div>
            <div style="font-size:13px;color:var(--muted)">$${item.price.toFixed(2)} x ${item.qty}</div>
          </div>
          <div style="display:flex;flex-direction:column;gap:6px;align-items:flex-end">
            <div style="display:flex;gap:6px">
              <button class="small-btn" data-change="-1">-</button>
              <div style="min-width:24px;text-align:center">${item.qty}</div>
              <button class="small-btn" data-change="1">+</button>
            </div>
            <button class="small-btn" style="background:#fff;border:1px solid #f0f0f0" data-remove>Eliminar</button>
          </div>
        `;
        // delegate within row
        row.addEventListener('click', (ev) => {
          const ch = ev.target.closest('[data-change]'); if(ch){ const delta = Number(ch.dataset.change||0); window.changeQty && window.changeQty(item.id, delta); }
          if(ev.target.closest('[data-remove]')) window.removeFromCart && window.removeFromCart(item.id);
        });
        cartList.appendChild(row);
      });
      calculateTotals(); updateCartIndicator();
    }

    function calculateTotals(){
      const cart = getCart(); const subtotal = cart.reduce((s,i)=>s + i.price * i.qty,0); const iva = subtotal * 0.12; const discount = 0; const total = subtotal + iva - discount; if(subtotalEl) subtotalEl.textContent = `$${subtotal.toFixed(2)}`; if(ivaEl) ivaEl.textContent = `$${iva.toFixed(2)}`; if(discountEl) discountEl.textContent = `-$${discount.toFixed(2)}`; if(totalEl) totalEl.textContent = `$${total.toFixed(2)}`; }

    window.changeQty = function(id, delta){ const cart = getCart(); const it = cart.find(i=>i.id===id); if(!it) return; it.qty = Math.max(0, it.qty + delta); const filtered = cart.filter(i=>i.qty>0); saveCart(filtered); renderCart(); };
    window.removeFromCart = function(id){ const cart = getCart().filter(i=>i.id!==id); saveCart(cart); renderCart(); };

    if(clearCartBtn) clearCartBtn.addEventListener('click', () => { if(confirm('Vaciar carrito?')){ saveCart([]); renderCart(); } });
    if(buyBtn) buyBtn.addEventListener('click', () => { const cart = getCart(); if(!cart || cart.length===0) return alert('El carrito está vacío'); alert('Compra simulada. Total: ' + (totalEl ? totalEl.textContent : '')); saveCart([]); renderCart(); if(cartModal) cartModal.style.display='none'; });
    if(selectAll) selectAll.addEventListener('change', function(){ if(!cartList) return; const checks = cartList.querySelectorAll('input[type="checkbox"]'); checks.forEach(c => c.checked = selectAll.checked); });

    // initialize product list and cart indicator
    applyFilters(); updateCartIndicator();

  }); // DOMContentLoaded

})();