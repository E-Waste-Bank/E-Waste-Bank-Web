from django.urls import path
from keuangan.views import *

app_name = 'keuangan'

urlpatterns = [
    path('', show_keuangan, name='show_keuangan'),
    path('admin/', show_admin, name='show_admin'),
    path('user/', show_user, name='show_user'),
    path('cashout/<int:id>/', user_get_cashout_html, name='user_get_cashout_html'),
    path('user/create-cashout/', user_create_cashout, name='user_create_cashout'),
    path('user/create-cashout-api/', user_create_cashout_api, name='user_create_cashout_api'),
    path('json/user/', user_get_keuangan_data_json, name='user_get_keuangan_data_json'),
    path('json/user-api/', user_get_keuangan_data_json_api, name='user_get_keuangan_data_json_api'),
    path('json/user-cashouts/', user_get_all_cashouts_json, name='user_get_all_cashouts_json'),
    path('json/user-cashouts-api/', user_get_all_cashouts_json_api, name='user_get_all_cashouts_json_api'),
    path('json/admin/', admin_get_keuangan_data_json, name='admin_get_keuangan_data_json'),
    path('json/admin-cashouts/', admin_get_all_cashouts_json, name='admin_get_all_cashouts_json'),
    path('edit-cashout/<int:id>/', admin_edit_cashout, name='admin_edit_cashout'),
    path('edit-uang-user/<int:id>/', admin_edit_uang_user, name='admin_edit_uang_user'),
    path('edit-cashout-api/<int:id>/', admin_edit_cashout_api, name='admin_edit_cashout'),
    path('edit-uang-user-api/<int:id>/', admin_edit_uang_user_api, name='admin_edit_uang_user'),
]