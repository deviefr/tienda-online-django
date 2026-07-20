# Tienda Online Django

Aplicación web desarrollada en equipo utilizando Django para la gestión de una tienda de productos personalizados.

> Proyecto académico desarrollado como parte de la formación en Analista Programador.

---

# Descripción

Tienda Online Django es una aplicación web orientada a la administración y venta de productos personalizados, permitiendo a los usuarios explorar un catálogo, realizar pedidos y hacer seguimiento del estado de sus compras.

El proyecto fue desarrollado colaborativamente utilizando Django y Django REST Framework, integrando funcionalidades de administración, carga de imágenes, seguimiento de pedidos y una API REST para distintas operaciones.

---

# Características

- Catálogo de productos.
- Filtro por categorías.
- Buscador de productos.
- Detalle de productos.
- Creación de pedidos.
- Seguimiento mediante token.
- Gestión de imágenes.
- Panel administrativo con Django Admin.
- API REST.
- Diseño responsive.

---

# Tecnologías utilizadas

## Backend

- Python
- Django
- Django REST Framework

## Frontend

- HTML5
- CSS3
- JavaScript

## Base de datos

- SQLite

## Herramientas

- Git
- GitHub
- Visual Studio Code

---

# Arquitectura

```
Usuario
    │
    ▼
Interfaz Web
    │
    ▼
Django
(Modelos • Vistas • Formularios • API REST)
    │
    ▼
SQLite
```

---

# Funcionalidades principales

## Gestión de productos

- Crear productos.
- Editar productos.
- Visualizar catálogo.
- Filtrar por categorías.
- Buscar por nombre.

---

## Gestión de pedidos

- Crear pedidos personalizados.
- Cargar imágenes de referencia.
- Generación automática de token.
- Seguimiento del estado del pedido.

---

## API REST

El proyecto incorpora una API desarrollada con Django REST Framework para la gestión de información desde aplicaciones externas.

Incluye operaciones CRUD para distintos recursos del sistema.

---

# Instalación

```bash
git clone https://github.com/deviefr/tienda-online-django.git

cd tienda-online-django

python -m venv venv
```

Activar entorno virtual

Windows

```bash
venv\Scripts\activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Migraciones

```bash
python manage.py migrate
```

Ejecutar servidor

```bash
python manage.py runserver
```

---

# Mi participación

Este fue un proyecto desarrollado en equipo.

Mi participación incluyó el desarrollo e integración de funcionalidades backend y frontend utilizando Django, así como la implementación y mejora de distintas características del sistema en conjunto con el resto del equipo.

---

# Competencias desarrolladas

Durante este proyecto se fortalecieron conocimientos relacionados con:

- Desarrollo web con Django.
- Desarrollo de API REST.
- Arquitectura MVT.
- Gestión de formularios.
- Bases de datos relacionales.
- Trabajo colaborativo utilizando Git.
- Desarrollo de interfaces web.
- Resolución de problemas.

---

# Estado del proyecto

Proyecto académico finalizado.

La aplicación fue desarrollada con fines educativos y el código fuente permanece disponible para revisión.

---

# Autor

Proyecto desarrollado en equipo.

Repositorio publicado por:

**Javiera Sepúlveda**

GitHub:
https://github.com/deviefr
