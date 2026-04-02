from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from fpdf import FPDF
from openpyxl import Workbook
from .models import Producto
from .forms import ProductoForm

# Create your views here.

class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/listar_producto.html'
    context_object_name = 'productos'
    paginate_by = 10
    ordering = ['productoId']


@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})


@login_required
def ver_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/ver_producto.html', {'producto': producto})


@login_required
def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/actualizar_producto.html', {'form': form, 'producto': producto})


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})


@login_required
def exportar_productos_pdf(request):
    def limpiar(texto):
        reemplazos = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ñ':'n',
                      'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ñ':'N'}
        for k, v in reemplazos.items():
            texto = texto.replace(k, v)
        return texto

    productos = Producto.objects.all()
    pdf = FPDF()
    pdf.add_page()
    ancho = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(ancho, 10, 'Reporte de Productos', ln=True)
    pdf.set_font('Arial', '', 10)
    for producto in productos:
        linea = limpiar(
            f"ID: {producto.productoId} | Nombre: {producto.nombre_producto} "
            f"| Precio: {producto.precio} | Stock: {producto.unidades_stock}"
        )
        pdf.multi_cell(ancho, 8, linea)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productos.pdf"'
    response.write(bytes(pdf.output(dest='S')))
    return response


@login_required
def exportar_productos_excel(request):
    productos = Producto.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.title = 'Productos'
    ws.append(['ID', 'Nombre', 'Precio', 'Stock'])
    for producto in productos:
        ws.append([
            producto.productoId,
            producto.nombre_producto,
            float(producto.precio),
            producto.unidades_stock,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'
    wb.save(response)
    return response
