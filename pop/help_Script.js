document.addEventListener('DOMContentLoaded', () => {
    
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const arrow = item.querySelector('.arrow');

        // Estado inicial
        let isOpen = false;

        question.addEventListener('click', () => {
            
            // Opcional: Cerrar otros items si solo quieres uno abierto a la vez
            // closeAllOtherItems(item); 

            if (!isOpen) {
                // ANIMACIÓN DE APERTURA
                
                // 1. Animar la altura del contenedor de respuesta
                anime({
                    targets: answer,
                    height: [0, answer.scrollHeight + 'px'], // De 0 a la altura real del contenido
                    opacity: [0, 1],
                    duration: 400,
                    easing: 'easeOutQuad'
                });

                // 2. Animar la flecha girando 180 grados
                anime({
                    targets: arrow,
                    rotate: 180,
                    duration: 300,
                    easing: 'easeOutQuad'
                });

                // 3. Cambiar color del texto para indicar activo
                anime({
                    targets: question,
                    color: '#6c5ce7', // primary-purple
                    duration: 300
                });

                isOpen = true;

            } else {
                // ANIMACIÓN DE CIERRE

                // 1. Colapsar altura
                anime({
                    targets: answer,
                    height: 0,
                    opacity: [1, 0],
                    duration: 300,
                    easing: 'easeInQuad'
                });

                // 2. Regresar flecha
                anime({
                    targets: arrow,
                    rotate: 0,
                    duration: 300,
                    easing: 'easeInQuad'
                });

                // 3. Regresar color original
                anime({
                    targets: question,
                    color: '#4834d4', // dark-purple
                    duration: 300
                });

                isOpen = false;
            }
        });
    });

    // Función opcional si quisieras comportamiento de acordeón estricto
    /*
    function closeAllOtherItems(currentItem) {
        faqItems.forEach(otherItem => {
            if (otherItem !== currentItem) {
                // Lógica para cerrar otros (copiando la animación de cierre)
                // Esto requiere manejar el estado 'isOpen' globalmente o consultar clases.
            }
        });
    }
    */
});