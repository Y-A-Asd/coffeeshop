from django.urls import path
from . import views


app_name = 'offkey'
urlpatterns = [
    path('off/', views.OffKeyView.as_view(), name='off'),
    ]