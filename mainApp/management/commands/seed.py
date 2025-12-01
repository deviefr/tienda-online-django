from django.core.management.base import BaseCommand
from mainApp.models import Producto, Categoria, Insumo, Pedido
from django.utils.text import slugify
from datetime import datetime

class Command(BaseCommand):
    help = "Carga datos iniciales (categorías, productos, insumos y pedidos) en la base de datos."
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando la carga de datos...")
        
        #Categorias personalizadas
        categorias = [
            ("Polerones Personalizados", True),
            ("Poleras Personalizadas", True),
            ("Tazas Personalizadas", True),
            ("Impresiones 3D", True),
            ("Stickers y Vinilos", True), 
        ]
        
        categoria_objs = {}
        for nombre, destacado in categorias:
            obj, created = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'slug': slugify(nombre),
                    'destacado': destacado},
            )
            categoria_objs[nombre] = obj
            
        
        #Insumos personalizados
        insumos = [
            ("Vinilo textil premium", "Material", 50, "metros", "Siser", "Negro"),
            ("Filamento PLA 1kg", "Material 3D", 10, "kg", "Esun", "Blanco"),
            ("Taza sublimable 11oz", "Base", 100, "unidades", "Generic", "Blanco"),
            ("Polerón algodón", "Base ropa", 20, "unidades", "Fruit of the Loom", "Gris"),
            ("Resina UV 500ml", "Material 3D", 5, "litros", "Anycubic", "Transparente"),
        ]
        
        for i in insumos:
            Insumo.objects.get_or_create(
                nombre=i[0],
                defaults={
                    'tipo': i[1],
                    'cantidad': i[2],
                    'unidad': i[3],
                    'marca': i[4],
                    'color': i[5],
                }
            )
            
        #Productos personalizados
        productos = [
            ("Polerón personalizado impresión frontal", categoria_objs["Polerones Personalizados"], 25000),
            ("Polera personalizada full color", categoria_objs["Poleras Personalizadas"], 15000),
            ("Taza personalizada sublimada", categoria_objs["Tazas Personalizadas"], 12000),
            ("Figura 3D personalizada", categoria_objs["Impresiones 3D"], 50000),
            ("Sticker vinilo personalizado", categoria_objs["Stickers y Vinilos"], 3000),
        ]
        
        producto_objs = {}
        for nombre, cat, precio in productos:
            obj, created = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'slug': slugify(nombre),
                    'categoria': cat,
                    'precio_base': precio,
                    'destacado': False,
                }
            )
            producto_objs[nombre] = obj
            
        #Pedidos de ejemplo
        pedidos = [
            ("pcp3001", "Juan Pérez", producto_objs["Polerón personalizado impresíon frontal"], "2024-06-01 10:00"),
            ("pcp3002", "María Gómez", producto_objs["Taza personalizada sublimada"], "2024-06-02 14:30"),
            ("pcp3003", "Carlos Ruiz", producto_objs["Figura 3D personalizada"], "2024-06-03 09:15"),
            ("pcp3004", "Ana Torres", producto_objs["Sticker vinilo personalizado"], "2024-06-04 16:45"),
            ("pcp3005", "Luis Fernández", producto_objs["Polera personalizada full color"], "2024-06-05 11:20"),
        ]
        
        for token, cliente, prod, fecha_str in pedidos:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
            Pedido.objects.get_or_create(
                token=token,
                defaults={
                    'cliente_nombre': cliente,
                    'producto': prod,
                    'fecha_solicitud': fecha,
                    'plataforma': "web",
                    'descripcion': f"Pedido de {prod.nombre} por {cliente}.",
                    'estado': "solicitado",
                    'estado_pago': "pendiente",
                    'total': prod.precio_base,
                }
            )
            
        self.stdout.write(self.style.SUCCESS("Carga de datos completada exitosamente."))