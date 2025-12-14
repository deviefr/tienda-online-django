from django.urls import path
from . import views

app_name = 'mainApp'

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("producto/<slug:slug>/", views.detalle_producto, name="detalle_producto"),
    path("producto/<slug:slug>/solicitar/", views.crear_pedido, name="crear_pedido"),
    path("crear-pedido/", views.crear_pedido, name="crear_pedido_simple"),
    path("pago/<str:token>/", views.marcar_pago, name="marcar_pago"),
    path("seguimiento/", views.seguimiento, name="seguimiento"),
    path("reporte/", views.reporte_dashboard, name="reporte"),
    path('api/insumos/', views.InsumoListCreateView.as_view()),
    path('api/insumos/<int:pk>/', views.InsumoDetailView.as_view()),
    path('api/pedidos/', views.PedidoCreateView.as_view()),
    path('api/pedidos/filtrar/', views.PedidoFiltrarView.as_view(), name='pedidos-filtrar'),
    path('api/pedidos/<str:token>/', views.PedidoUpdateView.as_view()),
]
