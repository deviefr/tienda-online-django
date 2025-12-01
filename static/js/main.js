// Archivo JS principal: pequeño comportamiento UX
document.addEventListener('DOMContentLoaded', function(){
    // ejemplo: cerrar alertas automáticamente
    // Solo cerramos automáticamente las alertas que NO tengan el atributo `data-persist`
    document.querySelectorAll('.alert').forEach(function(a){
        if (a.hasAttribute('data-persist')) return; // mantener alertas marcadas como persistentes
        setTimeout(function(){ a.classList.add('fade'); a.style.transition='opacity 0.5s'; a.style.opacity=0; setTimeout(()=>a.remove(),600); }, 5000);
    });
});
