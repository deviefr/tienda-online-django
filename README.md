# tienda-online-django
***30-11-2025***

Proyecto Django para venta de productos personalizados (poleras, polerones, tazones, productos 3D).

Resumen de cambios integrados:
- Front-end reorganizado: plantillas y `static` (CSS/JS) añadidos; tema azul.
- Plantillas mejoradas y responsive: `catalogo`, `detalle_producto`, `crear_pedido`, `seguimiento`.
- `Producto.imagen_principal` para mostrar imagenes de forma correcta (anteriormente se rompían las imagenes)
- Formulario de pedidos (`PedidoForm`) funcional con subida múltiple de imágenes, vista `crear_pedido` implementada y adaptada.
- Barra de filtrado por categorías fuera del navbar y "★ TOP" para productos destacados.
  
***01-12-2025***

 - Buscador en el catálogo (por nombre), que preserva filtro de categoría.
 - Flujo de pedido mejorado: al crear un pedido se genera un token de seguimiento que se muestra en pantalla.
 - En `crear_pedido` el precio se autocompleta en la UI según el `producto` seleccionado y hay opción "Pagar" que marca el pedido como pagado.
 - En `seguimiento` se puede marcar un pedido como pagado (botón `PAGAR`) y la vista recarga manteniendo el token.

***14-12-2025***

- Implementación de **Django REST Framework**
- API de Insumos: CRUD completo (listar, crear, editar, eliminar)
- API de Pedidos: Creación vía json y actualización mediante token (sin listar ni eliminar)
- API de Filtrado: Endpoint avanzado para filtrar por rango de fechas, estados y limitación de resultados.

---

### Archivos principales añadidos/modificados:
- `templates/` : `base.html`, `catalogo.html`, `detalle_producto.html`, `crear_pedido.html`, `seguimiento.html`, `pedido_creado.html`
- `static/css/style.css`, `static/js/main.js`
- `mainApp/models.py`, `mainApp/forms.py`, `mainApp/views.py`, `mainApp/urls.py`, `mainApp/serializers.py`

---

### Cómo clonar este repositorio (branch `probando-hola`) y ejecutar:

1) Clonar el repo y cambiar al branch:
```
git clone https://github.com/deviefr/tienda-online-django.git
cd tienda-online-django
git checkout probando-hola
```

2) Crear y activar un entorno virtual (opcional):
```
python -m venv .venv
.\.venv\Scripts\Activate
```

3) Instalar dependencias mínimas (Django, Pillow para manejo de imágenes y Django Rest Framework para las APIs):
```
pip install --upgrade pip
pip install Django Pillow djangorestframework
```

4) Aplicar migraciones y crear superusuario:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5) Cargar datos de ejemplo (seed)
```
python manage.py seed
```
Este comando crea categorías, productos, insumos y pedidos con fechas de JUNIO 2024 para pruebas.

5) Ejecutar servidor de desarrollo:
```
python manage.py runserver
```

6) Acceder en el navegador:
- Catálogo: `http://127.0.0.1:8000/catalogo/`
- Admin (subir imágenes / gestionar productos): `http://127.0.0.1:8000/admin/`

### Uso y configuración de APIs

El proyecto incluye 3 APIs construidas con django rest framework.
Se incluyó una configuración para evitar errores con los formatos de fecha al editar pedidos en `settings.py`

***Rutas y ejemplos de uso***
1) API de INSUMOS (gestión del stock): permite ver, crear, editar y eliminar insumos.
- Listar/Crear: `http://127.0.0.1:8000/api/insumos/`
- Detalle/Editar/Eliminar: `http://127.0.0.1:8000/api/insumos/<id>/`

2) API de PEDIDOS (creación y edición):
- Crear pedido (json): `http://127.0.0.1:8000/api/pedidos/`
- Editar pedido: `http://127.0.0.1:8000/api/pedidos/<token>` (se usa el token, no el id)

3) API de FILTRADO (reportes): ruta principal: `http://127.0.0.1:8000/api/pedidos/filtrar/`
Esta API permite filtrar pedidos usando parámetros en la URL (?param=valor)

Parámetros permitidos por rúbrica:
- `fecha_inicio`: YYYY-MM-DD
- `fecha_fin`: YYYY-MM-DD
- `estados`: se puede repetir para filtrar varios (solicitado, pagado, etc)
- `max_resultados`: número entero para filtrar por un máximo de apariciones

Ejemplos para probar en la plataforma:
1. Filtrar por fechas (ej. pedidos de Junio 2024): `http://127.0.0.1:8000/api/pedidos/filtrar/?fecha_inicio=2024-06-01&fecha_fin=2024-06-30`
2. Filtrar por Estado: `http://127.0.0.1:8000/api/pedidos/filtrar/?estados=solicitado`
3. Filtrar Múltiples Estados + Límite: `http://127.0.0.1:8000/api/pedidos/filtrar/?estados=pagado&estados=pendiente&max_resultados=5`


### Notas adicionales
- Token de seguimiento: es un código único que se genera automáticamente, pero en el seed existen unos pre-definidos.
- Media: no existe carpeta `media/` en el repo, las imágenes subidas se guardan localmente mientras exista la carpeta creada al subir archivos.
