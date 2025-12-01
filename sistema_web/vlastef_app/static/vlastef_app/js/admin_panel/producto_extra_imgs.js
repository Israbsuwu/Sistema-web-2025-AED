document.addEventListener('DOMContentLoaded', function(){
    const backdrop = document.getElementById('modal-backdrop-imagen');
    const confirmBtn = document.getElementById('modal-img-confirm');
    const cancelBtn = document.getElementById('modal-img-cancel');
    const modalText = document.getElementById('modal-img-text');
    const extraText = document.getElementById('modal-img-extra-text');
    let pendingAction = null; 
    let pendingFile = null;

    function openModal(action, fileName){
        pendingAction = action;
        pendingFile = fileName;
        if(action === 'delete-extra') {
            modalText.textContent = '¿Eliminar esta imagen adicional?';
            extraText.textContent = 'La miniatura se eliminará del almacenamiento.';
        } else if(action === 'delete-principal') {
            modalText.textContent = '¿Eliminar la imagen principal del producto?';
            extraText.textContent = 'El producto quedará sin imagen al guardar.';
        } else if(action === 'set-principal') {
            modalText.textContent = '¿Establecer esta imagen como principal?';
            extraText.textContent = 'La imagen actual pasará a la galería de adicionales.';
        }
        backdrop.style.display = 'flex';
    }
    function closeModal(){
        backdrop.style.display = 'none';
        pendingAction = null; pendingFile = null;
    }
    cancelBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', function(e){ if(e.target === backdrop) closeModal(); });

    confirmBtn.addEventListener('click', function(){
        if(!pendingAction) return;
        const csrf = document.querySelector('input[name=csrfmiddlewaretoken]');
        if(pendingAction === 'delete-extra') {
            const form = document.createElement('form');
            form.method='POST'; form.action=window.location.pathname;
            if(csrf){ const c=document.createElement('input'); c.type='hidden'; c.name='csrfmiddlewaretoken'; c.value=csrf.value; form.appendChild(c); }
            const flag=document.createElement('input'); flag.type='hidden'; flag.name='delete_extra'; flag.value='1'; form.appendChild(flag);
            const fname=document.createElement('input'); fname.type='hidden'; fname.name='file_name'; fname.value=pendingFile; form.appendChild(fname);
            document.body.appendChild(form); form.submit();
        } else if(pendingAction === 'set-principal') {
            const form = document.createElement('form');
            form.method='POST'; form.action=window.location.pathname;
            if(csrf){ const c=document.createElement('input'); c.type='hidden'; c.name='csrfmiddlewaretoken'; c.value=csrf.value; form.appendChild(c); }
            const flag=document.createElement('input'); flag.type='hidden'; flag.name='set_principal'; flag.value='1'; form.appendChild(flag);
            const fname=document.createElement('input'); fname.type='hidden'; fname.name='file_name'; fname.value=pendingFile; form.appendChild(fname);
            document.body.appendChild(form); form.submit();
        } else if(pendingAction === 'delete-principal') {
            // Agregar hidden al formulario principal y retirar vista previa
            const mainForm = document.getElementById('producto-form');
            if(mainForm){
                let hidden = mainForm.querySelector('input[name=delete_principal]');
                if(!hidden){
                    hidden = document.createElement('input');
                    hidden.type='hidden'; hidden.name='delete_principal'; hidden.value='1';
                    mainForm.appendChild(hidden);
                }
                // Limpiar input file y preview
                const fileInput = document.getElementById('id_imagen');
                if(fileInput){ fileInput.value=''; }
                const preview = document.getElementById('imagen-actual');
                if(preview){ preview.parentElement.remove(); }
            }
        }
        closeModal();
    });

    // Principal delete button
    const principalDeleteBtn = document.querySelector('.btn-delete-principal');
    if(principalDeleteBtn){ principalDeleteBtn.addEventListener('click', ()=> openModal('delete-principal', 'principal')); }

    // Viewer: abrir al hacer clic en principal o extra, evitando botones
    const viewerBackdrop = document.getElementById('image-viewer-backdrop');
    const viewerImg = document.getElementById('image-viewer-img');
    function openViewer(src, alt){ if(!viewerBackdrop||!viewerImg) return; viewerImg.src = src; viewerImg.alt = alt||'Imagen ampliada'; viewerBackdrop.style.display='flex'; document.body.style.overflow='hidden'; }
    function closeViewer(){ if(!viewerBackdrop||!viewerImg) return; viewerBackdrop.style.display='none'; viewerImg.src=''; document.body.style.overflow=''; }
    if(viewerBackdrop){ viewerBackdrop.addEventListener('click', function(e){ if(e.target===viewerBackdrop){ closeViewer(); } }); document.addEventListener('keyup', function(e){ if(e.key==='Escape' && viewerBackdrop.style.display==='flex'){ closeViewer(); } }); }

    const principalImg = document.getElementById('imagen-actual');
    if(principalImg){ principalImg.style.cursor='zoom-in'; principalImg.addEventListener('click', function(e){ if(e.target.closest('.btn-delete-principal')) return; openViewer(principalImg.src, principalImg.alt); }); }
    document.querySelectorAll('.extra-thumb').forEach(img => {
        img.style.cursor='zoom-in';
        img.addEventListener('click', function(e){
            if(e.target.closest('.btn-delete-extra') || e.target.closest('.btn-set-principal')) return;
            openViewer(img.src, img.alt);
        });
    });

    // Set principal buttons (acción directa sin modal)
    document.querySelectorAll('.btn-set-principal').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const fileName = btn.getAttribute('data-file');
            if(!fileName) return;
            const csrf = document.querySelector('input[name=csrfmiddlewaretoken]');
            const form = document.createElement('form');
            form.method='POST'; form.action=window.location.pathname;
            if(csrf){ const c=document.createElement('input'); c.type='hidden'; c.name='csrfmiddlewaretoken'; c.value=csrf.value; form.appendChild(c); }
            const flag=document.createElement('input'); flag.type='hidden'; flag.name='set_principal'; flag.value='1'; form.appendChild(flag);
            const fname=document.createElement('input'); fname.type='hidden'; fname.name='file_name'; fname.value=fileName; form.appendChild(fname);
            document.body.appendChild(form); form.submit();
        });
    });

    // Delete extra buttons
    document.querySelectorAll('.btn-delete-extra').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const fileName = btn.getAttribute('data-delete-file');
            if(!fileName) return; openModal('delete-extra', fileName);
        });
    });
});
