from django.urls import path
from penjemputan.views import show_penjemputan, show_json, add_penjemputan, delete_penjemputan, update_penjemputan, add_mobile

app_name = 'penjemputan'

urlpatterns = [
    path('', show_penjemputan, name='show_penjemputan'),
    path('json/', show_json, name='show_json'),
    path('add/', add_penjemputan, name='add_penjemputan'),
    path('add-mobile/', add_mobile, name='add_mobile'),
    path('update/<int:id>', update_penjemputan, name='update_penjemputan'),
    path('delete/<int:id>', delete_penjemputan, name='delete_penjemputan'),
]