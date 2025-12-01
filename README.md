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

Archivos principales añadidos/modificados:
- `templates/` : `base.html`, `catalogo.html`, `detalle_producto.html`, `crear_pedido.html`, `seguimiento.html`, `pedido_creado.html`
- `static/css/style.css`, `static/js/main.js`
- `mainApp/models.py`, `mainApp/forms.py`, `mainApp/views.py`, `mainApp/urls.py`

Cómo clonar este repositorio (branch `probando-hola`) y ejecutar:

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

3) Instalar dependencias mínimas (Django, Pillow para manejo de imágenes):
```
pip install --upgrade pip
pip install Django Pillow
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
Este comando crea categorías, productos de ejemplo, insumos y pedidos de muestra. Al crear productos desde `seed`, el script también prepara datos básicos (productos con slug, categoría y precio_base).

5) Ejecutar servidor de desarrollo:
```
python manage.py runserver
```

6) Acceder en el navegador:
- Catálogo: `http://127.0.0.1:8000/catalogo/`
- Admin (subir imágenes / gestionar productos): `http://127.0.0.1:8000/admin/`

Notas y recomendaciones rápidas:
- En desarrollo, `MEDIA_URL` ya está configurado en `tiendaOnline/settings.py`; las rutas se sirven automáticamente cuando `DEBUG=True`.

Información adicional y buenas prácticas

- Token de seguimiento: cuando se crea un pedido válido, la página de confirmación muestra el `token` y un botón para ir a `Seguimiento`. Esa vista permite ver detalles y simular el pago.
- Pago (simulación): el proyecto implementa una opción de pago simulado (no hay integración con pasarela). Marcar "Pagar" en la creación o pulsar `PAGAR` en seguimiento cambia `estado_pago` a `pagado`.
- No existe carpeta `media/`, por lo que las fotos no quedan guardadas ni registradas, pero la lógica del proyecto la integra, por lo que es posible agregar, modificar o eliminar fotos mientras EXISTA la carpeta.

Estado actual: plataforma funcional, con necesidad de cambios mínimos.
