from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from fpdf import FPDF
from openpyxl import Workbook
from .models import DetallePedido
from .forms import DetallePedidoForm
# Create your views here.
class DetallePedidoListView(LoginRequiredMixin, ListView):
    template_name = 'detalles_pedido/listar_detalles.html'
    context_object_name = 'detalles_pedidos'
    paginate_by = 10

    def get_queryset(self):
        return DetallePedido.objects.select_related('pedidoId', 'productoId').all().order_by('detallesId')

@login_required
def crear_detalle_pedido(request):
    if request.method == 'POST':
        form = DetallePedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_detalle_pedidos')
    else:
        form = DetallePedidoForm()
    return render(request, 'detalles_pedido/crear_detalles.html', {'form': form})


@login_required
def ver_detalle_pedido(request, pk):
    detalle_pedido = get_object_or_404(DetallePedido, pk=pk)
    return render(request, 'detalles_pedido/ver_detalles.html', {'detalle_pedido': detalle_pedido})


@login_required
def actualizar_detalle_pedido(request, pk):
    detalle_pedido = get_object_or_404(DetallePedido, pk=pk)
    if request.method == 'POST':
        form = DetallePedidoForm(request.POST, instance=detalle_pedido)
        if form.is_valid():
            form.save()
            return redirect('listar_detalle_pedidos')
    else:
        form = DetallePedidoForm(instance=detalle_pedido)
    return render(request, 'detalles_pedido/actualizar_detalles.html', {'form': form, 'detalle_pedido': detalle_pedido})


@login_required
def eliminar_detalle_pedido(request, pk):
    detalle_pedido = get_object_or_404(DetallePedido, pk=pk)
    if request.method == 'POST':
        detalle_pedido.delete()
        return redirect('listar_detalle_pedidos')
    return render(request, 'detalles_pedido/eliminar_detalles.html', {'detalle_pedido': detalle_pedido})


@login_required
def exportar_detalles_pdf(request):
    def limpiar(texto):
        reemplazos = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ñ':'n',
                      'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ñ':'N'}
        for k, v in reemplazos.items():
            texto = texto.replace(k, v)
        return texto

    detalles = DetallePedido.objects.select_related('pedidoId', 'productoId').all()
    pdf = FPDF()
    pdf.add_page()
    ancho = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(ancho, 10, 'Reporte de Detalles de Pedido', ln=True)
    pdf.set_font('Arial', '', 10)
    for detalle in detalles:
        linea = limpiar(
            f"ID: {detalle.detallesId} | Pedido: {detalle.pedidoId.pedidoId} "
            f"| Producto: {detalle.productoId.nombre_producto} "
            f"| Cantidad: {detalle.cantidad} | Subtotal: {detalle.subtotal}"
        )
        pdf.multi_cell(ancho, 8, linea)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="detalles_pedido.pdf"'
    response.write(bytes(pdf.output(dest='S')))
    return response


@login_required
def exportar_detalles_excel(request):
    detalles = DetallePedido.objects.select_related('pedidoId', 'productoId').all()
    wb = Workbook()
    ws = wb.active
    ws.title = 'DetallesPedido'
    ws.append(['ID', 'Pedido', 'Producto', 'Cantidad', 'Subtotal'])
    for detalle in detalles:
        ws.append([
            detalle.detallesId,
            detalle.pedidoId.pedidoId,
            detalle.productoId.nombre_producto,
            detalle.cantidad,
            float(detalle.subtotal),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="detalles_pedido.xlsx"'
    wb.save(response)
    return response

