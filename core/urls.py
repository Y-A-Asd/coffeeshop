from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "core"
urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('dashboard', views.DashboardView.as_view(),name='dashboard'),
    path('about-us/', views.about_us, name='about-us'),
    # path('doc:-/', views.document, name='doc'),
]
