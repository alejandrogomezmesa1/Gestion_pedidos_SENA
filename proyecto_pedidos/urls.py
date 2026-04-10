"""proyecto_pedidos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from clientes.views import login_view, registro_view


urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    path("admin/", admin.site.urls),
    path("pedidos/", include("pedidos.urls")),
    path("api/pedidos/", include("pedidos.api_urls")),
    path("clientes/", include("clientes.urls")),
    path("api/clientes/", include("clientes.api_urls")),
    path("productos/", include("productos.urls")),
    path("api/productos/", include("productos.api_urls")),
    path("detalles_pedido/", include("detalles_pedido.urls")),
    path("api/detalles_pedido/", include("detalles_pedido.api_urls")),
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
]
