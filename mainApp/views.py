from django.shortcuts import render
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
    return render(request, 'catalogo.html', {'productos': productos, 'categorias': categorias})

def detalle_producto(request, slug):
    producto = Producto.objects.filter(slug=slug).prefetch_related('imagenes').first()
    return render(request, 'detalle_producto.html', {'producto': producto})

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'crear_pedido.html')
    else:
        form = PedidoForm()
    return render(request, 'crear_pedido.html', {'form': form})

def seguimiento(request):
    token = request.GET.get('token')
    pedido = None
    if token:
        pedido = Pedido.objects.filter(token=token).first()
    return render(request, 'seguimiento.html', {'pedido': pedido})
