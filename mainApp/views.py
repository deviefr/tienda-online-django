from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Producto, Categoria, Pedido, PedidoImagen
from .forms import PedidoForm


def catalogo(request):
    q = request.GET.get('q')
    cat = request.GET.get('categoria')
    productos = Producto.objects.all().select_related('categoria').prefetch_related('imagenes')
    
    if cat:
        productos = productos.filter(categoria__slug=cat)
    if q:
        productos = productos.filter(nombre__icontains=q)
    
    categorias = Categoria.objects.all()
    categoria_actual = None
    if cat:
        categoria_actual = Categoria.objects.filter(slug=cat).first()

    return render(request, 'catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': categoria_actual,
        'q': q,
    })


def detalle_producto(request, slug):
    producto = Producto.objects.filter(slug=slug).prefetch_related('imagenes').first()
    return render(request, 'detalle_producto.html', {'producto': producto})


def crear_pedido(request, slug=None):
    initial = {}
    if slug:
        producto = Producto.objects.filter(slug=slug).first()
        if producto:
            initial['producto'] = producto

    productos = Producto.objects.all()

    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            try:
                pedido.total = pedido.producto.precio_base
            except Exception:
                pedido.total = 0
            pedido.save()

            if request.FILES:
                imagenes_files = request.FILES.getlist('imagenes')
                for f in imagenes_files:
                    PedidoImagen.objects.create(pedido=pedido, imagen=f)

            try:
                pagar_ahora = form.cleaned_data.get('pagar_ahora')
            except Exception:
                pagar_ahora = False
            if pagar_ahora:
                pedido.estado_pago = 'pagado'
                pedido.save()

            return render(request, 'pedido_creado.html', {
                'token': pedido.token,
                'pedido': pedido,
            })
    else:
        form = PedidoForm(initial=initial)

    return render(request, 'crear_pedido.html', {
        'form': form,
        'productos': productos,
        'initial_producto': initial.get('producto') if initial else None,
    })


def marcar_pago(request, token):
    pedido = Pedido.objects.filter(token=token).first()
    if not pedido:
        return redirect('mainApp:seguimiento')

    pedido.estado_pago = 'pagado'
    pedido.save()
    
    return redirect(reverse('mainApp:seguimiento') + f'?token={pedido.token}')


def seguimiento(request):
    token = request.GET.get('token')
    pedido = None

    if token:
        pedido = Pedido.objects.prefetch_related('imagenes').filter(token=token).first()

    return render(request, 'seguimiento.html', {
        'pedido': pedido,
        'token': token
    })



from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, F, Q
from django.utils import timezone
from datetime import datetime

def staff_required(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(staff_required)
def reporte_dashboard(request):
    """
    Reporte del sistema:
    - Cantidad de pedidos por estado
    - Productos más solicitados
    - Pedidos por plataforma
    - Filtrado por fechas / plataforma
    """
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    plataforma = request.GET.get('plataforma', 'all')
    top_n = int(request.GET.get('top_n', 10))

    now = timezone.now()

    try:
        fecha_fin_dt = datetime.fromisoformat(fecha_fin) if fecha_fin else now
    except:
        fecha_fin_dt = now

    try:
        fecha_inicio_dt = datetime.fromisoformat(fecha_inicio) if fecha_inicio else fecha_fin_dt - timezone.timedelta(days=30)
    except:
        fecha_inicio_dt = fecha_fin_dt - timezone.timedelta(days=30)

    pedidos = Pedido.objects.all()

    if plataforma != "all":
        pedidos = pedidos.filter(plataforma=plataforma)

    pedidos = pedidos.filter(
        Q(fecha_solicitud__date__gte=fecha_inicio_dt.date(), fecha_solicitud__date__lte=fecha_fin_dt.date()) |
        Q(fecha_solicitud__isnull=True, creado__date__gte=fecha_inicio_dt.date(), creado__date__lte=fecha_fin_dt.date())
    )

    pedidos_por_estado = pedidos.values("estado").annotate(total=Count("id")).order_by("-total")

    productos_mas = pedidos.values(
        producto_id=F("producto"),
        producto_nombre=F("producto__nombre")
    ).annotate(
        cantidad=Count("id"),
        total_vendido=Sum("total")
    ).order_by("-cantidad")[:top_n]

    pedidos_por_plataforma = pedidos.values("plataforma").annotate(total=Count("id")).order_by("-total")

    pedidos_lista = pedidos.select_related("producto").order_by("-creado")[:500]

    context = {
        'fecha_inicio': fecha_inicio_dt.date().isoformat(),
        'fecha_fin': fecha_fin_dt.date().isoformat(),
        'plataforma_seleccionada': plataforma,
        'top_n': top_n,

        'pedidos_por_estado': list(pedidos_por_estado),
        'productos_mas': list(productos_mas),
        'pedidos_por_plataforma': list(pedidos_por_plataforma),
        'pedidos_lista': pedidos_lista,

        'estados_labels': [i['estado'] for i in pedidos_por_estado],
        'estados_values': [i['total'] for i in pedidos_por_estado],

        'productos_labels': [i['producto_nombre'] for i in productos_mas],
        'productos_values': [i['cantidad'] for i in productos_mas],

        'plataformas_labels': [i['plataforma'] for i in pedidos_por_plataforma],
        'plataformas_values': [i['total'] for i in pedidos_por_plataforma],
    }

    return render(request, 'reporte_dashboard.html', context)

def reporte_sistema(request):
    return render(request, "reporte.html")



