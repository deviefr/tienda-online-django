from django.db import models
import uuid
from django.core.exceptions import ValidationError

PLATAFORMAS = [
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('whatsapp', 'WhatsApp'),
    ('presencial', 'Presencial'),
    ('web', 'Sitio Web'),
    ('otra', 'Otra'),
    ]

ESTADOS_PEDIDO = [
    ('solicitado', 'Solicitado'),
    ('aprobado', 'Aprobado'),
    ('en_proceso', 'En Proceso'),
    ('realizada', 'Realizada'),
    ('finalizada', 'Finalizada'),
    ('cancelada', 'Cancelada'),
    ]

ESTADOS_PAGO = [
    ('pendiente', 'Pendiente'), 
    ('parcial', 'Parcial'),
    ('pagado', 'Pagado'),
    ]

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    destacado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    precio_base = models.IntegerField(max_digits=10)
    destacado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')
    orden = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return f"Imagen de {self.producto.nombre} (Orden: {self.orden})"
    
    class Meta:
        ordering = ['orden']
        
class Insumo(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    unidad = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
def generar_token():
    return uuid.uuid4().hex

class Pedido(models.Model):
    token = models.CharField(max_length=32, unique=True, default=generar_token, editable=False)
    cliente_nombre = models.CharField(max_length=200)
    cliente_contacto = models.CharField(max_length=200, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    descripcion = models.TextField(blank=True)
    plataforma = models.CharField(max_length=20, choices=PLATAFORMAS, default='web')
    fecha_solicitud = models.DateTimeField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='en_proceso')
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')
    total = models.IntegerField(default=0)

    def clean(self):
        if self.estado == 'finalizada' and self.estado_pago != 'pagado':
            raise ValidationError("El pedido no puede ser finalizado si el pago no está completo.")
        
    def __str__(self):
        return f"Pedido {self.token} - {self.cliente_nombre}"
    
class PedidoImagen(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='pedidos/')
    orden = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return f"Imagen de Pedido {self.pedido.token} (Orden: {self.orden})"
    
    class Meta:
        ordering = ['orden']

        
        
        