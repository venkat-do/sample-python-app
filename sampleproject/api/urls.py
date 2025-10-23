from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health', views.health, name='health'),
    path('api/users', views.users, name='users'),
    path('api/stats', views.stats, name='stats'),
    path('api/echo', views.echo, name='echo'),
]
