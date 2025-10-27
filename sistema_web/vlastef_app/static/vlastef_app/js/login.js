(function () {
  const btnEye = document.querySelector(".toggle-pass");
  const input = document.getElementById("password");
  if (btnEye && input) {
    btnEye.addEventListener("click", () => {
      const showing = input.type === "text";
      input.type = showing ? "password" : "text";
      btnEye.setAttribute(
        "aria-label",
        showing ? "Mostrar contraseña" : "Ocultar contraseña"
      );
      btnEye.title = showing ? "Mostrar contraseña" : "Ocultar contraseña";
      btnEye.classList.toggle("show", !showing);
    });
  }

  // Client-side validation only. Submission and auth should be handled by Django views.
  const form = document.getElementById("loginForm");
  const email = document.getElementById("email");
  const errors = document.getElementById("loginErrors");

  if (form) {
    form.addEventListener("submit", function (e) {
      // Clear previous client-side errors
      if (errors) {
        errors.style.display = "none";
        errors.textContent = "";
      }

      const emailVal = ((email && email.value) || "").trim();
      const passVal = ((input && input.value) || "").trim();
      const msgs = [];
      if (!emailVal || !emailVal.includes("@"))
        msgs.push('Introduce un correo válido que contenga "@".');
      if (!passVal) msgs.push("La contraseña no puede estar vacía.");

      if (msgs.length) {
        e.preventDefault();
        if (errors) {
          errors.innerHTML = msgs.join("<br>");
          errors.style.display = "block";
        }
      }
      // Otherwise allow form to be submitted to server
    });
  }
})();
