
from django.urls import path
from .views import home, test, registro, exit

urlpatterns = [
    path('', home, name='home'),
    path('test/', test, name='test'),
    path('registro/', registro, name='registro'),
    path('logout/', exit, name='exit'),
]