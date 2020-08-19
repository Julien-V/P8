from django.urls import path

from .import views


urlpatterns = [
    path('search_results', views.search_results, name='search_results'),
    path('substitute', views.substitute, name='substitute'),
    path('product', views.product, name='product'),
    path('user_auth', views.user_auth, name='authentification'),
    path('user_deauth', views.user_deauth, name='deauthentification'),
    path('user_reg', views.user_reg, name="register"),
    path('terms', views.terms, name="terms"),
    path('home', views.index, name='home')
]
