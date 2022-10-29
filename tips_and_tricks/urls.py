from django.urls import path
from .views import index, add, load_more, search_json

urlpatterns = [
    path('', index, name='index_tips'),
    path('add', add, name='add_tips'),
    path('load-more', load_more, name='load-more'),
    path('search-json', search_json, name='search_json'),
]