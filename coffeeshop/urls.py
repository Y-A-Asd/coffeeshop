"""
URL configuration for coffeshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from users.views import UsersLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('foods/', include('foodmenu.urls', namespace='foods')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/login/', UsersLoginView.as_view(), ),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('blogs/', include('blog.urls', namespace='blog')),
    path('users/', include('users.urls', namespace='users')),
    path('tables/', include('tables.urls', namespace='tables')),
    path('keys/', include('offkey.urls', namespace='offkey')),
    path('orders/', include('order.urls', namespace='order')),
    path('tags/', include('tag.urls', namespace='tags')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
