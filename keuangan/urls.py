from django.urls import path
from keuangan.views import *

app_name = 'keuangan'

urlpatterns = [
    path('', show_keuangan, name='show_keuangan'),
    path('admin/', show_admin, name='show_admin'),
    path('user/', show_user, name='show_user'),
]