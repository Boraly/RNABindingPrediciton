from django.urls import path

from webinterface import views

app_name = 'webinterface'

urlpatterns = [
    path('', views.home, name='home'),
    path('download-csv/', views.download_csv, name='download_csv'),
]

