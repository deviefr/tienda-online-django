// Archivo JS principal: pequeño comportamiento UX
document.addEventListener('DOMContentLoaded', function(){
    // ejemplo: cerrar alertas automáticamente
    document.querySelectorAll('.alert').forEach(function(a){
        setTimeout(function(){ a.classList.add('fade'); a.style.transition='opacity 0.5s'; a.style.opacity=0; setTimeout(()=>a.remove(),600); }, 5000);
    });
});
