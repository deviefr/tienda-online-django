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
