from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "core"
urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('dashboard', views.DashboardView.as_view(),name='dashboard'),
    path('retrieve-changes/<int:log_id>/', views.RetrieveChangesView.as_view(), name='retrieve-changes'),
    path('logs', views.LogListView.as_view(),name='logs'),
    path('about-us/', views.about_us, name='about-us'),
    # path('doc:-/', views.document, name='doc'),
]
