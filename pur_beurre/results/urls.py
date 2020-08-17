from django.urls import path

from .import views


urlpatterns = [
    path('search_results', views.search_results, name='search_results'),
    path('substitute', views.substitute, name='substitute'),
    path('user_auth', views.user_auth, name='authentification'),
    path('user_deauth', views.user_deauth, name='deauthentification'),
    path('user_reg', views.user_reg, name="register"),
    path('legals', views.legals, name="legals"),
    path('home', views.index, name='home')
]
