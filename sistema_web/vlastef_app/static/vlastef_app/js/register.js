// Mostrar/ocultar contraseña (guardado por si el elemento no existe)
const togglePwd = document.getElementById("togglePwd");
if (togglePwd) {
  togglePwd.addEventListener("change", function () {
    const pwd = document.getElementById("contrasena");
    if (pwd) pwd.type = this.checked ? "text" : "password";
  });
}

// Manejar envío: validación cliente y permitir envío al servidor
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", function (e) {
    // simple client validation
    const form = e.target;
    const correo = (form.correo.value || '').trim();
  const username = (form.username ? form.username.value || '' : '').trim();
    const contrasena = form.contrasena.value || '';
  const contrasena2 = form.contrasena2 ? form.contrasena2.value || '' : '';
    const nombres = (form.nombres.value || '').trim();
    const apellidos = (form.apellidos.value || '').trim();

    if (!correo || !/^\S+@\S+\.\S+$/.test(correo)) {
      e.preventDefault();
      alert('Ingrese un correo válido.');
      return;
    }
    if (!contrasena || contrasena.length < 6) {
      e.preventDefault();
      alert('La contraseña debe tener mínimo 6 caracteres.');
      return;
    }
    if (!username) { e.preventDefault(); alert('Ingrese un nombre de usuario.'); return; }
    if (contrasena !== contrasena2) {
      e.preventDefault();
      alert('Las contraseñas no coinciden.');
      return;
    }
    if (!nombres || !apellidos) {
      e.preventDefault();
      alert('Complete nombres y apellidos.');
      return;
    }
    // new required fields
    const fecha_nac = form.fecha_nac ? form.fecha_nac.value || '' : '';
  const sexo = form.sexo ? (form.sexo.value || '') : '';
    const direccion = form.direccion ? form.direccion.value.trim() : '';
    if (!fecha_nac) { e.preventDefault(); alert('Ingrese su fecha de nacimiento.'); return; }
    if (!sexo) { e.preventDefault(); alert('Seleccione su sexo.'); return; }
    if (!direccion) { e.preventDefault(); alert('Ingrese su dirección.'); return; }
    // allow server to handle creating the user
  });
}
