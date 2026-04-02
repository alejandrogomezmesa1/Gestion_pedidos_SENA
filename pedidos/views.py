# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from fpdf import FPDF
from openpyxl import Workbook
from .models import Pedido
from .forms import PedidoForm
from detalles_pedido.models import DetallePedido

DetalleInlineFormSet = inlineformset_factory(
    Pedido,
    DetallePedido,
    fields=['productoId', 'cantidad'],
    fk_name='pedidoId',
    extra=1,
    can_delete=True,
)
# Crear las vistas para las operaciones CRUD
class PedidoListView(LoginRequiredMixin, ListView):
    template_name = 'pedidos/listar_pedidos.html'
    context_object_name = 'pedidos'
    paginate_by = 10

    def get_queryset(self):
        return Pedido.objects.select_related('clienteId').all().order_by('pedidoId')

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        formset = DetalleInlineFormSet(request.POST, prefix='detalles')
        if form.is_valid() and formset.is_valid():
            pedido = form.save()
            formset.instance = pedido
            formset.save()
            return redirect('listar_pedidos')
    else:
        form = PedidoForm()
        formset = DetalleInlineFormSet(prefix='detalles')
    return render(request, 'pedidos/crear_pedido.html', {'form': form, 'formset': formset})


@login_required
def ver_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'pedidos/ver_pedido.html', {'pedido': pedido})


@login_required
def actualizar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        formset = DetalleInlineFormSet(request.POST, instance=pedido, prefix='detalles')
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('listar_pedidos')
    else:
        form = PedidoForm(instance=pedido)
        formset = DetalleInlineFormSet(instance=pedido, prefix='detalles')
    return render(request, 'pedidos/actualizar_pedido.html', {'form': form, 'pedido': pedido, 'formset': formset})


@login_required
def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if pedido.detalles.exists():
        from django.contrib import messages
        messages.error(request, 'No se puede eliminar el pedido porque tiene productos asociados. Elimine primero los detalles.')
        return redirect('listar_pedidos')
    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')
    return render(request, 'pedidos/eliminar_pedido.html', {'pedido': pedido})


@login_required
def exportar_pedidos_pdf(request):
    def limpiar(texto):
        reemplazos = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ñ':'n',
                      'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ñ':'N'}
        for k, v in reemplazos.items():
            texto = texto.replace(k, v)
        return texto

    pedidos = Pedido.objects.select_related('clienteId').all()
    pdf = FPDF()
    pdf.add_page()
    ancho = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(ancho, 10, 'Reporte de Pedidos', ln=True)
    pdf.set_font('Arial', '', 10)
    for pedido in pedidos:
        linea = limpiar(
            f"ID: {pedido.pedidoId} | Cliente: {pedido.clienteId.nombre_cliente} "
            f"| Fecha: {pedido.fecha_pedido.strftime('%Y-%m-%d')} "
            f"| Estado: {pedido.get_estado_display()}"
        )
        pdf.multi_cell(ancho, 8, linea)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedidos.pdf"'
    response.write(bytes(pdf.output(dest='S')))
    return response


@login_required
def exportar_pedidos_excel(request):
    pedidos = Pedido.objects.select_related('clienteId').all()
    wb = Workbook()
    ws = wb.active
    ws.title = 'Pedidos'
    ws.append(['ID', 'Cliente', 'Fecha', 'Estado'])
    for pedido in pedidos:
        ws.append([
            pedido.pedidoId,
            pedido.clienteId.nombre_cliente,
            pedido.fecha_pedido.strftime('%Y-%m-%d %H:%M:%S'),
            pedido.get_estado_display(),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="pedidos.xlsx"'
    wb.save(response)
    return response


