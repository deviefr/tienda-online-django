# formularios para pedidos

from django import forms
from .models import Pedido, PedidoImagen

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class PedidoForm(forms.ModelForm):
    imagenes = forms.FileField(widget=MultipleFileInput(attrs={'multiple': True}), required=False)
    pagar_ahora = forms.BooleanField(required=False, label='Pagar ahora (simulación)')
    
    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'cliente_contacto', 'producto', 'descripcion', 'plataforma', 'fecha_solicitud']
        widgets = {
            'fecha_solicitud': forms.DateTimeInput(attrs={'type': 'datetime-local'}),}
        
    def save(self, commit=True):
        pedido = super().save(commit=commit)
        if self.files:
            imagenes_files = self.files.getlist('imagenes')
            for f in imagenes_files:
                PedidoImagen.objects.create(pedido=pedido, imagen=f)
        return pedido