from django.core.management.base import BaseCommand
from mainApp.models import Producto, Categoria, Insumo, Pedido
from django.utils.text import slugify
from datetime import datetime


class Command(BaseCommand):
    help = "Carga datos iniciales (categorías, productos, insumos y pedidos) en la base de datos."

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando la carga de datos...")

        categorias = [
            ("Polerones Personalizados", True),
            ("Poleras Personalizadas", True),
            ("Tazas Personalizadas", True),
            ("Impresiones 3D", True),
            ("Stickers y Vinilos", True),
        ]

        categoria_objs = {}
        for nombre, destacado in categorias:
            obj, _ = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "slug": slugify(nombre),
                    "destacado": destacado,
                },
            )
            categoria_objs[nombre] = obj

        insumos = [
            ("Vinilo textil premium", "Material", 50, "metros", "Siser", "Negro"),
            ("Filamento PLA 1kg", "Material 3D", 10, "kg", "Esun", "Blanco"),
            ("Taza sublimable 11oz", "Base", 100, "unidades", "Generic", "Blanco"),
            ("Polerón algodón", "Base ropa", 20, "unidades", "Fruit of the Loom", "Gris"),
            ("Resina UV 500ml", "Material 3D", 5, "litros", "Anycubic", "Transparente"),
        ]

        for nombre, tipo, cantidad, unidad, marca, color in insumos:
            Insumo.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "tipo": tipo,
                    "cantidad": cantidad,
                    "unidad": unidad,
                    "marca": marca,
                    "color": color,
                },
            )


        productos = [
            ("Polerón personalizado impresión frontal", "Polerones Personalizados", 25000),
            ("Polera personalizada full color", "Poleras Personalizadas", 15000),
            ("Taza personalizada sublimada", "Tazas Personalizadas", 12000),
            ("Figura 3D personalizada", "Impresiones 3D", 50000),
            ("Sticker vinilo personalizado", "Stickers y Vinilos", 3000),
        ]

        producto_objs = {}
        for nombre, categoria_nombre, precio in productos:
            slug = slugify(nombre)
            obj, _ = Producto.objects.get_or_create(
                slug=slug,
                defaults={
                    "nombre": nombre,
                    "categoria": categoria_objs[categoria_nombre],
                    "precio_base": precio,
                    "destacado": False,
                },
            )
            producto_objs[slug] = obj


        pedidos = [
            ("pcp3001", "Juan Pérez", "poleron-personalizado-impresion-frontal", "2024-06-01 10:00"),
            ("pcp3002", "María Gómez", "taza-personalizada-sublimada", "2024-06-02 14:30"),
            ("pcp3003", "Carlos Ruiz", "figura-3d-personalizada", "2024-06-03 09:15"),
            ("pcp3004", "Ana Torres", "sticker-vinilo-personalizado", "2024-06-04 16:45"),
            ("pcp3005", "Luis Fernández", "polera-personalizada-full-color", "2024-06-05 11:20"),
        ]

        for token, cliente, producto_slug, fecha_str in pedidos:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
            Pedido.objects.get_or_create(
                token=token,
                defaults={
                    "cliente_nombre": cliente,
                    "producto": producto_objs[producto_slug],
                    "fecha_solicitud": fecha,
                    "plataforma": "web",
                    "descripcion": f"Pedido de {producto_objs[producto_slug].nombre} por {cliente}.",
                    "estado": "solicitado",
                    "estado_pago": "pendiente",
                    "total": producto_objs[producto_slug].precio_base,
                },
            )

        self.stdout.write(self.style.SUCCESS("Carga de datos completada exitosamente."))
