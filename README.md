# tienda-online-django

------------------------------------------------------------------------------------------------------------------------------------------------------------
30-11-2025
Proyecto Django para venta de productos personalizados (poleras, polerones, tazones, productos 3D).

Resumen de cambios integrados:
- Front-end reorganizado: plantillas y `static` (CSS/JS) añadidos; tema azul.
- Plantillas mejoradas y responsive: `catalogo`, `detalle_producto`, `crear_pedido`, `seguimiento`.
- `Producto.imagen_principal` para mostrar imagenes de forma correcta (anteriormente se rompían las imagenes)
- Formulario de pedidos (`PedidoForm`) funcional con subida múltiple de imágenes, vista `crear_pedido` implementada y adaptada.
- Barra de filtrado por categorías fuera del navbar y "★ TOP" para productos destacados.

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

5) Ejecutar servidor de desarrollo:
```
python manage.py runserver
```

6) Acceder en el navegador:
- Catálogo: `http://127.0.0.1:8000/catalogo/`
- Admin (subir imágenes / gestionar productos): `http://127.0.0.1:8000/admin/`

Notas y recomendaciones rápidas:
- En desarrollo, `MEDIA_URL` ya está configurado en `tiendaOnline/settings.py`; las rutas se sirven automáticamente cuando `DEBUG=True`.

Estado actual: plataforma funcional, con necesidad de cambios mínimos.
