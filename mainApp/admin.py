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



def marcar_solicitado(modeladmin, request, queryset):
    queryset.update(estado='solicitado')
marcar_solicitado.short_description = "Marcar como SOLICITADO"

def marcar_aprobado(modeladmin, request, queryset):
    queryset.update(estado='aprobado')
marcar_aprobado.short_description = "Marcar como APROBADO"

def marcar_en_proceso(modeladmin, request, queryset):
    queryset.update(estado='en_proceso')
marcar_en_proceso.short_description = "Marcar como EN PROCESO"

def marcar_realizada(modeladmin, request, queryset):
    queryset.update(estado='realizada')
marcar_realizada.short_description = "Marcar como REALIZADA"

def marcar_entregada(modeladmin, request, queryset):
    queryset.update(estado='entregada')
marcar_entregada.short_description = "Marcar como ENTREGADA"

def marcar_finalizada(modeladmin, request, queryset):
    queryset.update(estado='finalizada')
marcar_finalizada.short_description = "Marcar como FINALIZADA"

def marcar_cancelada(modeladmin, request, queryset):
    queryset.update(estado='cancelada')
marcar_cancelada.short_description = "Marcar como CANCELADA"


def pago_pendiente(modeladmin, request, queryset):
    queryset.update(estado_pago='pendiente')
pago_pendiente.short_description = "Marcar pago como PENDIENTE"

def pago_parcial(modeladmin, request, queryset):
    queryset.update(estado_pago='parcial')
pago_parcial.short_description = "Marcar pago como PARCIAL"

def pago_pagado(modeladmin, request, queryset):
    queryset.update(estado_pago='pagado')
pago_pagado.short_description = "Marcar pago como PAGADO"


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'token',
        'cliente_nombre',
        'producto',
        'estado',
        'estado_pago',
        'creado',
        'fecha_solicitud'
    )
    list_filter = ('plataforma', 'estado', 'estado_pago', 'creado')
    search_fields = ('token', 'cliente_nombre', 'cliente_contacto', 'producto_nombre')
    inlines = [PedidoImagenInline]
    readonly_fields = ('token', 'creado')

    actions = [
        marcar_solicitado,
        marcar_aprobado,
        marcar_en_proceso,
        marcar_realizada,
        marcar_entregada,
        marcar_finalizada,
        marcar_cancelada,
        pago_pendiente,
        pago_parcial,
        pago_pagado
    ]

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
        except ValidationError as e:
            from django.contrib import messages
            messages.error(request, e)
            return
        super().save_model(request, obj, form, change)
