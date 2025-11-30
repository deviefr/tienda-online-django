from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Pedido
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
    })


def detalle_producto(request, slug):
    producto = Producto.objects.filter(slug=slug).prefetch_related('imagenes').first()
    return render(request, 'detalle_producto.html', {'producto': producto})


def crear_pedido(request, slug=None):
    """
    Crear un pedido. Si se pasa `slug`, preselecciona el producto en el formulario.
    """
    initial = {}
    if slug:
        producto = Producto.objects.filter(slug=slug).first()
        if producto:
            initial['producto'] = producto

    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'pedido_creado.html')
    else:
        form = PedidoForm(initial=initial)

    return render(request, 'crear_pedido.html', {'form': form})



def seguimiento(request):
    """
    Muestra la pantalla para ingresar un token
    y en caso de venir 'token' en GET, muestra el detalle.
    """
    token = request.GET.get('token')
    pedido = None

    if token:
        pedido = Pedido.objects.prefetch_related('imagenes').filter(token=token).first()

    return render(request, 'seguimiento.html', {
        'pedido': pedido,
        'token': token
    })
