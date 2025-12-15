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
                }
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
                }
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
            categoria = categoria_objs.get(categoria_nombre)
            if not categoria:
                self.stdout.write(self.style.WARNING(f"Categoría '{categoria_nombre}' no encontrada"))
                continue

            obj, _ = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "slug": slugify(nombre),
                    "categoria": categoria,
                    "precio_base": precio,
                    "destacado": False,
                }
            )
            producto_objs[nombre] = obj
        

        pedidos = [
            ("pcp3001", "Juan Pérez", "Polerón personalizado impresión frontal", "2024-06-01 10:00"),
            ("pcp3002", "María Gómez", "Taza personalizada sublimada", "2024-06-02 14:30"),
            ("pcp3003", "Carlos Ruiz", "Figura 3D personalizada", "2024-06-03 09:15"),
            ("pcp3004", "Ana Torres", "Sticker vinilo personalizado", "2024-06-04 16:45"),
            ("pcp3005", "Luis Fernández", "Polera personalizada full color", "2024-06-05 11:20"),
        ]
        
        for token, cliente, producto_nombre, fecha_str in pedidos:
            producto = producto_objs.get(producto_nombre)

            if not producto:
                self.stdout.write(
                    self.style.WARNING(f"Producto '{producto_nombre}' no encontrado, pedido omitido")
                )
                continue

            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")

            Pedido.objects.get_or_create(
                token=token,
                defaults={
                    "cliente_nombre": cliente,
                    "producto": producto,
                    "fecha_solicitud": fecha,
                    "plataforma": "web",
                    "descripcion": f"Pedido de {producto.nombre} por {cliente}.",
                    "estado": "solicitado",
                    "estado_pago": "pendiente",
                    "total": producto.precio_base,
                }
            )
        
        self.stdout.write(self.style.SUCCESS("Carga de datos completada exitosamente."))
