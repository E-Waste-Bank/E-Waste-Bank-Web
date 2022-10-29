from django.urls import path
from .views import *

app_name = "home"

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('register/', register, name='register'),
]