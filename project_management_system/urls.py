"""project_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from project_management_system import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^client/', views.client),
    url(r'^instructor/', views.instructor),
    url(r'^student/', views.student),
    url(r'^login/', views.login_view),
    url(r'^register/', views.register),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^projects/', views.projects),
    url(r'^project/(\d+)', views.project_view),
    url(r'^menu/', views.menu),
    url(r'^messages/', views.messages),
    url(r'^makesection/', views.make_a_section)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
