from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from fpdf import FPDF
from openpyxl import Workbook
from .models import Cliente
from .forms import ClienteForm

# Create your views here.

# Creacion de crud para cliente
# --------------------------------------------------------------------------------
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/listar_cliente.html'
    context_object_name = 'clientes'
    paginate_by = 10
    ordering = ['clienteId']


@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})


@login_required
def ver_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'clientes/ver_cliente.html', {'cliente': cliente})


@login_required
def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/actualizar_cliente.html', {'form': form, 'cliente': cliente})


@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('listar_clientes')


@login_required
def exportar_clientes_pdf(request):
    def limpiar(texto):
        reemplazos = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ñ':'n',
                      'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ñ':'N'}
        for k, v in reemplazos.items():
            texto = texto.replace(k, v)
        return texto

    clientes = Cliente.objects.all()
    pdf = FPDF()
    pdf.add_page()
    ancho = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(ancho, 10, 'Reporte de Clientes', ln=True)
    pdf.set_font('Arial', '', 10)
    for cliente in clientes:
        linea = limpiar(
            f"ID: {cliente.clienteId} | Nombre: {cliente.nombre_cliente} "
            f"| Email: {cliente.email} | Tel: {cliente.teléfono}"
        )
        pdf.multi_cell(ancho, 8, linea)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clientes.pdf"'
    response.write(bytes(pdf.output(dest='S')))
    return response


@login_required
def exportar_clientes_excel(request):
    clientes = Cliente.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.title = 'Clientes'
    ws.append(['ID', 'Nombre', 'Email', 'Direccion', 'Telefono'])
    for cliente in clientes:
        ws.append([
            cliente.clienteId,
            cliente.nombre_cliente,
            cliente.email,
            cliente.dirección,
            cliente.teléfono,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="clientes.xlsx"'
    wb.save(response)
    return response