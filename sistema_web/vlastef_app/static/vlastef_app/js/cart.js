/* Lógica del carrito para la página Carrito.html */
(function(){
  function getCart(){ try{ return JSON.parse(sessionStorage.getItem('alx_cart')||'[]'); }catch(e){ return []; } }
  function saveCart(cart){ sessionStorage.setItem('alx_cart', JSON.stringify(cart)); }

  function format(v){ try{ if(typeof formatCurrency==='function') return formatCurrency(v); }catch(e){} return '$' + (Number(v)||0).toFixed(2); }

  function render(){
    const list = getCart();
    const container = document.getElementById('cartItems');
    const empty = document.getElementById('cartEmpty');
    const summaryEl = document.getElementById('cartSummary');
    if(!container) return;
    container.innerHTML = '';
    if(!list || list.length === 0){ if(empty) empty.style.display = 'block'; if(summaryEl) summaryEl.style.display = 'none'; return; }
    if(empty) empty.style.display = 'none'; if(summaryEl) summaryEl.style.display = 'block';

    list.forEach((item, idx) => {
      const row = document.createElement('div');
      row.className = 'item-row';
      row.dataset.index = idx;

      // Checkbox
      const cbWrap = document.createElement('div');
      const cb = document.createElement('input');
      cb.type = 'checkbox'; cb.className = 'sel-item'; cb.dataset.index = idx; cb.setAttribute('aria-label', 'Seleccionar ' + (item.title || ''));
      cbWrap.appendChild(cb);
      row.appendChild(cbWrap);

      // Thumb
      const thumb = document.createElement('div'); thumb.className = 'item-thumb';
      const img = document.createElement('img'); img.src = item.img || '../assets/favicon.svg'; img.alt = item.title || '';
      thumb.appendChild(img);
      row.appendChild(thumb);

      // Info
      const info = document.createElement('div'); info.className = 'item-info';
      const title = document.createElement('div'); title.className = 'item-title'; title.textContent = item.title || '';
      const meta = document.createElement('div'); meta.className = 'item-meta';
      meta.textContent = (item.size ? ('Talla: ' + item.size + ' • ') : '') + (item.color ? ('Color: ' + item.color) : '');

      const controls = document.createElement('div'); controls.className = 'item-controls';
      const qtyControl = document.createElement('div'); qtyControl.className = 'qty-control';
      const btnDec = document.createElement('button'); btnDec.type = 'button'; btnDec.className = 'qty-dec'; btnDec.dataset.idx = idx; btnDec.textContent = '-';
      const inputQty = document.createElement('input'); inputQty.type = 'number'; inputQty.min = 1; inputQty.value = item.qty || 1; inputQty.className = 'qty-input'; inputQty.dataset.idx = idx;
      const btnInc = document.createElement('button'); btnInc.type = 'button'; btnInc.className = 'qty-inc'; btnInc.dataset.idx = idx; btnInc.textContent = '+';
      qtyControl.appendChild(btnDec); qtyControl.appendChild(inputQty); qtyControl.appendChild(btnInc);
      const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'remove-btn'; remove.dataset.idx = idx; remove.textContent = 'Eliminar';
      controls.appendChild(qtyControl); controls.appendChild(remove);

      info.appendChild(title); info.appendChild(meta); info.appendChild(controls);
      row.appendChild(info);

      // Price
      const priceDiv = document.createElement('div'); priceDiv.className = 'price';
      priceDiv.textContent = format(item.price);
      const qtySmall = document.createElement('div'); qtySmall.style.fontSize = '12px'; qtySmall.style.color = 'var(--muted)'; qtySmall.textContent = 'x ' + (item.qty || 1);
      priceDiv.appendChild(qtySmall);
      row.appendChild(priceDiv);

      container.appendChild(row);
    });

    attachHandlers();
    updateTotals();
  }

  function escapeHtml(s){ return String(s||'').replace(/[&<>'"]/g, function(m){ return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m]; }); }

  function attachHandlers(){
    document.querySelectorAll('.qty-inc').forEach(b=> b.onclick = function(){ changeQty(parseInt(this.dataset.idx,10), 1); });
    document.querySelectorAll('.qty-dec').forEach(b=> b.onclick = function(){ changeQty(parseInt(this.dataset.idx,10), -1); });
    document.querySelectorAll('.qty-input').forEach(i=> i.onchange = function(){ setQty(parseInt(this.dataset.idx,10), Math.max(1,parseInt(this.value||1,10))); });
    document.querySelectorAll('.remove-btn').forEach(b=> b.onclick = function(){ removeItem(parseInt(this.dataset.idx,10)); });
    document.getElementById('selectAll') && (document.getElementById('selectAll').onchange = function(){ document.querySelectorAll('.sel-item').forEach(cb=> cb.checked = this.checked); });
    document.getElementById('deleteSelected') && (document.getElementById('deleteSelected').onclick = deleteSelected);
    document.getElementById('checkoutBtn') && (document.getElementById('checkoutBtn').onclick = checkout);
    document.getElementById('clearCart') && (document.getElementById('clearCart').onclick = clearCart);
  }

  function changeQty(idx, delta){ const cart = getCart(); if(!cart[idx]) return; cart[idx].qty = Math.max(1, (cart[idx].qty||1)+delta); saveCart(cart); render(); }
  function setQty(idx, qty){ const cart = getCart(); if(!cart[idx]) return; cart[idx].qty = Math.max(1, qty||1); saveCart(cart); render(); }
  function removeItem(idx){ const cart = getCart(); if(!cart[idx]) return; if(!confirm('Eliminar este producto?')) return; cart.splice(idx,1); saveCart(cart); render(); }

  function deleteSelected(){ const checks = Array.from(document.querySelectorAll('.sel-item')).filter(c=>c.checked).map(c=>parseInt(c.dataset.index,10)); if(!checks.length) return alert('No hay productos seleccionados.'); if(!confirm('Eliminar los productos seleccionados?')) return; let cart = getCart(); cart = cart.filter((_,i)=> !checks.includes(i)); saveCart(cart); render(); }

  function clearCart(){ if(!confirm('Vaciar todo el carrito?')) return; saveCart([]); render(); }

  function updateTotals(){ const cart = getCart(); const subtotal = cart.reduce((s,i)=>s + (Number(i.price)||0) * (Number(i.qty)||0), 0); const iva = subtotal * 0.12; const discount = 0; const total = subtotal + iva - discount; document.getElementById('subtotal').textContent = format(subtotal); document.getElementById('iva').textContent = format(iva); document.getElementById('discount').textContent = '-'+format(discount); document.getElementById('total').textContent = format(total); }

  function checkout(){ const checks = Array.from(document.querySelectorAll('.sel-item')).filter(c=>c.checked).map(c=>parseInt(c.dataset.index,10)); const cart = getCart(); if(cart.length===0) return alert('El carrito está vacío'); let toBuy = cart; if(checks.length) toBuy = cart.filter((_,i)=>checks.includes(i)); const summary = toBuy.map(i=> i.title + ' x' + i.qty).join('\n'); if(!confirm('Confirmar compra de:\n' + summary)) return; // Simulación
    // Aquí podrías enviar al servidor
    // Remover items comprados
    if(checks.length){ let newCart = cart.filter((_,i)=> !checks.includes(i)); saveCart(newCart); } else { saveCart([]); }
    alert('Compra simulada. Gracias!'); render();
  }

  // Inicializar
  document.addEventListener('DOMContentLoaded', function(){
    render();
  });

  // Exponer utilidades (opcional)
  window.cartRender = render;
  window.cartGet = getCart;
})();
