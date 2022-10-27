from django.urls import path
from keuangan.views import show_admin

app_name = 'keuangan'

urlpatterns = [
    path('admin/', show_admin, name='show_admin'),
]