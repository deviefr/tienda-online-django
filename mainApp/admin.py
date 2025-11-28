from django.contrib import admin
from .models import *
from django.core.exceptions import ValidationError

class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    max_num = 3
    
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_base', 'destacado', 'creado')
    prepopulated_fields = {'slug': ['nombre']}
    list_filter = ('categoria', 'destacado', 'creado')
    search_fields = ('nombre', 'descripcion')
    inlines = [ProductoImagenInline]
    
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'destacado')
    prepopulated_fields = {'slug': ['nombre']}
    
@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'cantidad', 'unidad', 'marca', 'color')
    search_fields = ('nombre', 'tipo', 'marca')
    
class PedidoImagenInline(admin.TabularInline):
    model = PedidoImagen
    extra = 1
    
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('token', 'cliente_nombre', 'producto', 'estado', 'estado_pago', 'creado', 'fecha_solicitud')
    list_filter = ('plataforma', 'estado', 'estado_pago', 'creado')
    search_fields = ('token', 'cliente_nombre', 'cliente_contacto', 'producto_nombre')
    inlines = [PedidoImagenInline]
    readonly_fields = ('token', 'creado')
    
    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
        except ValidationError as e:
            from django.contrib import messages
            messages.error(request, e)
            return
        super().save_model(request, obj, form, change)
        
