from django.urls import path

from .import views


urlpatterns = [
    path('search_results', views.search_results, name='search_results'),
    path('my_substitute', views.substitute, name='substitute')
]
