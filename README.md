# Sistema de Gestión de Pedidos

Aplicación web desarrollada con Django 6 y MySQL para gestionar clientes, productos, pedidos y sus detalles. Incluye autenticación con JWT, exportación a PDF y Excel, paginación y confirmaciones con SweetAlert2.

---

## Tabla de contenidos

1. [Instalación del entorno](#1-instalación-del-entorno)
2. [Creación del proyecto](#2-creación-del-proyecto)
3. [Modelos](#3-modelos)
4. [Migraciones](#4-migraciones)
5. [Vistas CRUD](#5-vistas-crud)
6. [Templates](#6-templates)
7. [Paginación](#7-paginación)
8. [SweetAlert2](#8-sweetalert2)
9. [Exportación PDF y Excel](#9-exportación-pdf-y-excel)
10. [Capturas paso a paso](#10-capturas-paso-a-paso)

---

## 1. Instalación del entorno

### Requisitos previos

- Python 3.10 o superior
- MySQL 8.0
- Git

### Clonar el repositorio

```bash
git clone https://github.com/alejandrogomezmesa1/Gestion_pedidos_SENA.git
cd Gestion_pedidos_SENA
```

### Crear y activar el entorno virtual

```bash
# Crear
python -m venv env

# Activar en Windows
env\Scripts\activate

# Activar en Linux/Mac
source env/bin/activate
```

### Instalar dependencias

```bash
pip install -r requeriments.txt
```

Las dependencias principales son:

| Paquete | Versión | Uso |
|---|---|---|
| Django | 6.0.3 | Framework principal |
| mysqlclient | 2.2.8 | Conector MySQL |
| djangorestframework | 3.17.1 | API REST |
| djangorestframework-simplejwt | 5.5.1 | Autenticación JWT |
| fpdf2 | 2.8.7 | Exportación PDF |
| openpyxl | 3.1.5 | Exportación Excel |

### Configurar la base de datos

Iniciar el servicio MySQL (Windows):

```powershell
# En PowerShell como administrador
net start MYSQL80
```

Crear la base de datos en MySQL:

```sql
CREATE DATABASE sistema_pedidos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Configurar `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sistema_pedidos',
        'USER': 'root',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 2. Creación del proyecto

### Estructura del proyecto

```
proyecto_pedidos/
├── manage.py
├── requeriments.txt
├── .gitignore
├── static/
│   └── css/
│       └── base.css          ← CSS global
├── templates/
│   ├── home.html
│   └── partials/
│       └── navbar.html       ← Navbar compartido
├── proyecto_pedidos/         ← Configuración Django
│   ├── settings.py
│   └── urls.py
├── clientes/                 ← App clientes
├── productos/                ← App productos
├── pedidos/                  ← App pedidos
├── detalles_pedido/          ← App detalles
└── usuarios/                 ← App autenticación JWT
```

### Crear el proyecto y las apps

```bash
django-admin startproject proyecto_pedidos
cd proyecto_pedidos

python manage.py startapp clientes
python manage.py startapp productos
python manage.py startapp pedidos
python manage.py startapp detalles_pedido
python manage.py startapp usuarios
```

### Registrar las apps en `settings.py`

```python
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Terceros
    'rest_framework',
    'rest_framework_simplejwt',
    # Apps del proyecto
    'pedidos',
    'clientes',
    'productos',
    'detalles_pedido',
    'usuarios',
]
```

### Configuración de autenticación

```python
LOGIN_URL = '/usuarios/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/usuarios/login/'
```

---

## 3. Modelos

### Diagrama de relaciones

```
Cliente  ──(1:N)──  Pedido  ──(1:N)──  DetallePedido  ──(N:1)──  Producto
```

- Un **Cliente** puede tener muchos **Pedidos**
- Un **Pedido** puede tener muchos **DetallePedido**
- Cada **DetallePedido** referencia un **Producto**
- La combinación `(pedidoId, productoId)` es única — no se repite el mismo producto en un pedido

### `clientes/models.py`

```python
from django.db import models

class Cliente(models.Model):
    clienteId      = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    email          = models.EmailField()
    dirección      = models.CharField(max_length=100)
    teléfono       = models.CharField(max_length=20)

    class Meta:
        db_table = "cliente"

    def __str__(self):
        return self.nombre_cliente
```

### `productos/models.py`

```python
from django.db import models
from django.core.validators import MinValueValidator

class Producto(models.Model):
    productoId      = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    precio          = models.DecimalField(max_digits=10, decimal_places=2,
                                          validators=[MinValueValidator(0)])
    unidades_stock  = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = "producto"

    def __str__(self):
        return self.nombre_producto
```

### `pedidos/models.py`

```python
from django.db import models
from django.core.exceptions import ValidationError

class Pedido(models.Model):
    ESTADOS_CHOICES = [
        ('pendiente',  'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado',    'Enviado'),
        ('entregado',  'Entregado'),
        ('cancelado',  'Cancelado'),
    ]

    # Transiciones de estado permitidas
    TRANSICIONES_VALIDAS = {
        'pendiente':  ['procesando', 'cancelado'],
        'procesando': ['enviado',    'cancelado'],
        'enviado':    ['entregado',  'cancelado'],
        'entregado':  [],
        'cancelado':  [],
    }

    pedidoId    = models.AutoField(primary_key=True)
    clienteId   = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE,
                                     related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado       = models.CharField(max_length=20, choices=ESTADOS_CHOICES,
                                    default='pendiente')

    class Meta:
        db_table = "pedido"

    def clean(self):
        if self.pk:
            estado_anterior = Pedido.objects.get(pk=self.pk).estado
            if estado_anterior != self.estado:
                permitidos = self.TRANSICIONES_VALIDAS.get(estado_anterior, [])
                if self.estado not in permitidos:
                    raise ValidationError(
                        {'estado': f'No se puede pasar de "{estado_anterior}" a "{self.estado}".'}
                    )
```

### `detalles_pedido/models.py`

```python
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class DetallePedido(models.Model):
    detallesId = models.AutoField(primary_key=True)
    pedidoId   = models.ForeignKey(Pedido,   on_delete=models.CASCADE, related_name='detalles')
    productoId = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles')
    cantidad   = models.IntegerField(validators=[MinValueValidator(1)])
    subtotal   = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "detalle_pedido"
        constraints = [
            models.UniqueConstraint(fields=['pedidoId', 'productoId'],
                                    name='unique_producto_por_pedido')
        ]

    def clean(self):
        # Valida que haya stock suficiente
        ...

    def save(self, *args, **kwargs):
        # Descuenta stock y calcula subtotal automáticamente
        ...

    def delete(self, *args, **kwargs):
        # Restaura el stock al eliminar
        ...
```

> **Reglas de negocio implementadas:**
> - Stock nunca puede quedar negativo
> - El subtotal se calcula automáticamente: `precio × cantidad`
> - Al editar una cantidad, se devuelve el stock anterior antes de descontar el nuevo
> - Al eliminar un detalle, el stock se restaura
> - Un pedido con detalles no puede eliminarse directamente

---

## 4. Migraciones

```bash
# Crear migraciones iniciales
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate
```

Salida esperada:

```
Migrations for 'clientes':
  clientes\migrations\0001_initial.py
    + Create model Cliente
Migrations for 'productos':
  productos\migrations\0001_initial.py
    + Create model Producto
...
Operations to perform:
  Apply all migrations: admin, auth, clientes, ...
Running migrations:
  Applying clientes.0001_initial... OK
  Applying productos.0001_initial... OK
  Applying pedidos.0001_initial... OK
  Applying detalles_pedido.0001_initial... OK
```

### Crear superusuario

```bash
python manage.py createsuperuser
```

---

## 5. Vistas CRUD

Cada app implementa las siguientes operaciones:

| Operación | Método HTTP | Descripción |
|---|---|---|
| Listar | GET | `ListView` con paginación |
| Ver detalle | GET | `get_object_or_404` |
| Crear | GET + POST | Formulario con validación |
| Actualizar | GET + POST | Formulario prerellenado |
| Eliminar | GET + POST | Confirmación antes de borrar |

### Ejemplo — `clientes/views.py`

```python
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

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
def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/actualizar_cliente.html',
                  {'form': form, 'cliente': cliente})

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})
```

### URLs — `clientes/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('',                     views.ClienteListView.as_view(), name='listar_clientes'),
    path('crear/',               views.crear_cliente,             name='crear_cliente'),
    path('ver/<int:pk>/',        views.ver_cliente,               name='ver_cliente'),
    path('actualizar/<int:pk>/', views.actualizar_cliente,        name='actualizar_cliente'),
    path('eliminar/<int:pk>/',   views.eliminar_cliente,          name='eliminar_cliente'),
]
```

### Formset para múltiples productos en un pedido

```python
from django.forms import inlineformset_factory

DetalleInlineFormSet = inlineformset_factory(
    Pedido,
    DetallePedido,
    fields=['productoId', 'cantidad'],
    fk_name='pedidoId',
    extra=1,
    can_delete=True,
)

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        form    = PedidoForm(request.POST)
        formset = DetalleInlineFormSet(request.POST, prefix='detalles')
        if form.is_valid() and formset.is_valid():
            pedido          = form.save()
            formset.instance = pedido
            formset.save()
            return redirect('listar_pedidos')
    else:
        form    = PedidoForm()
        formset = DetalleInlineFormSet(prefix='detalles')
    return render(request, 'pedidos/crear_pedido.html',
                  {'form': form, 'formset': formset})
```

---

## 6. Templates

Todos los templates heredan estilos del navbar compartido ubicado en `templates/partials/navbar.html`, que carga el CSS global y SweetAlert2.

### Incluir el navbar en cada template

```html
{% include 'partials/navbar.html' %}
```

### Estructura de un template de lista

```html
{% include 'partials/navbar.html' %}
<div class="page-wrapper">
    <div class="page-header">
        <h1>Clientes</h1>
        <a href="{% url 'crear_cliente' %}" class="btn btn-primary">+ Crear</a>
    </div>

    <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for cliente in clientes %}
                <tr>
                    <td>{{ cliente.clienteId }}</td>
                    <td>{{ cliente.nombre_cliente }}</td>
                    <td>
                        <a href="{% url 'ver_cliente' cliente.pk %}"     class="btn btn-sm btn-info">Ver</a>
                        <a href="{% url 'actualizar_cliente' cliente.pk %}" class="btn btn-sm btn-warning">Editar</a>
                        <a href="{% url 'eliminar_cliente' cliente.pk %}"   class="btn btn-sm btn-danger">Eliminar</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Paginación -->
    {% include 'partials/pagination.html' %}
</div>
```

### Formulario de creación/edición

```html
{% include 'partials/navbar.html' %}
<div class="page-wrapper">
    <div class="card">
        <h2>Crear Cliente</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Guardar</button>
                <a href="{% url 'listar_clientes' %}" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>
```

---

## 7. Paginación

Se utiliza `ListView` con el atributo `paginate_by` en lugar de `Paginator` manual.

### Vista

```python
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/listar_cliente.html'
    context_object_name = 'clientes'
    paginate_by = 10          # 10 registros por página
    ordering = ['clienteId']
```

### Template — bloque de paginación

```html
{% if is_paginated %}
<nav class="pagination">
    {% if page_obj.has_previous %}
        <a href="?page=1">&laquo; Primera</a>
        <a href="?page={{ page_obj.previous_page_number }}">Anterior</a>
    {% endif %}

    <span>Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>

    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Siguiente</a>
        <a href="?page={{ page_obj.paginator.num_pages }}">Última &raquo;</a>
    {% endif %}
</nav>
{% endif %}
```

> `page_obj` y `is_paginated` son variables que Django inyecta automáticamente cuando se usa `ListView`.

---

## 8. SweetAlert2

Se utiliza SweetAlert2 para mostrar confirmaciones antes de ejecutar acciones críticas (crear, editar, eliminar).

### Carga desde CDN en `navbar.html`

```html
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
```

### Lógica de interceptación de clics y envíos

El script en `navbar.html` intercepta automáticamente todos los botones y enlaces de acción:

```javascript
document.addEventListener('click', function(event) {
    var link = event.target.closest('a[href]');
    if (!link || link.closest('nav')) return;

    var action = getActionFromText(link.textContent);
    if (!action) return;

    event.preventDefault();
    var cfg = getConfirmConfig(action);

    Swal.fire({
        title: cfg.title,
        text: cfg.text,
        icon: cfg.icon,
        showCancelButton: true,
        confirmButtonText: cfg.confirmButtonText,
        cancelButtonText: 'Cancelar'
    }).then(function(result) {
        if (result.isConfirmed) {
            window.location.href = link.href;
        }
    });
});
```

### Tipos de confirmación según el texto del botón

| Texto del botón | Tipo de alerta |
|---|---|
| Contiene "eliminar" | `warning` — rojo |
| Contiene "editar" / "actualizar" | `question` — azul |
| Contiene "crear" / "guardar" | `question` — azul |

---

## 9. Exportación PDF y Excel

Cada módulo incluye dos endpoints de exportación protegidos con `@login_required`.

### Exportación PDF con fpdf2

```python
from fpdf import FPDF
from django.http import HttpResponse

@login_required
def exportar_clientes_pdf(request):
    clientes = Cliente.objects.all()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Reporte de Clientes', ln=True)
    pdf.set_font('Arial', '', 10)
    for cliente in clientes:
        pdf.multi_cell(0, 8,
            f"ID: {cliente.clienteId} | Nombre: {cliente.nombre_cliente} "
            f"| Email: {cliente.email} | Tel: {cliente.teléfono}"
        )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clientes.pdf"'
    response.write(bytes(pdf.output(dest='S')))
    return response
```

### Exportación Excel con openpyxl

```python
from openpyxl import Workbook

@login_required
def exportar_clientes_excel(request):
    clientes = Cliente.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.title = 'Clientes'
    ws.append(['ID', 'Nombre', 'Email', 'Dirección', 'Teléfono'])
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
```

### URLs de exportación

```python
path('exportar/pdf/',   views.exportar_clientes_pdf,   name='exportar_clientes_pdf'),
path('exportar/excel/', views.exportar_clientes_excel, name='exportar_clientes_excel'),
```

### Botones en el template

```html
<div class="export-bar">
    <a href="{% url 'exportar_clientes_pdf' %}"   class="btn btn-danger btn-sm">Exportar PDF</a>
    <a href="{% url 'exportar_clientes_excel' %}" class="btn btn-success btn-sm">Exportar Excel</a>
</div>
```

---

## 10. Capturas paso a paso

### Iniciar el servidor

```bash
# Activar entorno virtual
env\Scripts\activate

# Iniciar MySQL (PowerShell como administrador)
net start MYSQL80

# Ejecutar servidor Django
python manage.py runserver
```

Abrir en el navegador: **http://127.0.0.1:8000/**

---

### Pantalla de login

Al abrir la aplicación se redirige automáticamente a `/usuarios/login/`. Ingresa las credenciales del superusuario creado con `createsuperuser`.

```
URL: http://127.0.0.1:8000/usuarios/login/
```

---

### Home con navbar

Después de iniciar sesión el sistema muestra el panel principal con la barra de navegación que incluye acceso a todos los módulos y el botón **Cerrar sesión** con el nombre del usuario activo.

---

### Módulo Clientes

| URL | Acción |
|---|---|
| `/clientes/` | Listar todos los clientes (paginado) |
| `/clientes/crear/` | Formulario para nuevo cliente |
| `/clientes/ver/1/` | Detalle del cliente ID 1 |
| `/clientes/actualizar/1/` | Editar cliente ID 1 |
| `/clientes/eliminar/1/` | Eliminar cliente ID 1 |
| `/clientes/exportar/pdf/` | Descargar reporte PDF |
| `/clientes/exportar/excel/` | Descargar reporte Excel |

---

### Módulo Pedidos — formulario con múltiples productos

Al crear o editar un pedido se muestra un formulario principal (datos del pedido) y una tabla de productos (formset inline) donde se pueden agregar filas dinámicamente con el botón **"+ Agregar producto"**.

---

### Confirmación con SweetAlert2

Al hacer clic en **Eliminar**, **Editar** o **Crear** aparece un diálogo de confirmación antes de ejecutar la acción.

---

### Protección de rutas

Todas las vistas requieren autenticación. Si el usuario no ha iniciado sesión y accede a cualquier URL, es redirigido automáticamente a `/usuarios/login/?next=/ruta/solicitada/`.
