from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index_tips'),
    path('add', add, name='add_tips'),
    path('load-more', load_more, name='load-more'),
    path('search-json', search_json, name='search_json'),
    path('post-json', get_all_post, name='get_all_post'),
    path('add-mobile', add_mobile, name='add_mobile'),
    # path('get-username/<int:idUser>', get_user_username, name='get_user_username'),
]