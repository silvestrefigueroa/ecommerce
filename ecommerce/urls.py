"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.conf.urls.static import static#esto viene del upload de las imagenes
from django.conf import settings #tambien me lo traje para arreglar el upload de imagenes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('store/', include('store.urls')),#en vez de cargarla aca, la incluyo de las definiciones de la App
    path('cart/', include('carts.urls')),#en vez de cargarlas aca, las incluyo de la definicion dentro de la App
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
