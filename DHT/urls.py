from django.urls import path
from . import views
from . import api

urlpatterns = [
    # API Données
    path("api/", api.Dlist, name='json'),
    path("api/post", api.Dhtviews.as_view(), name='json'),

    # API pour le Dashboard (IA)
    path("latest/", views.latest_json, name="latest_json"),

    # Page d'accueil
    path('', views.dashboard, name='dashboard'),

    # ❌ Anciennes pages désactivées (avec un # devant)
    # path('index/', views.table, name='table'),
    # path('myChart/', views.graphique, name='myChart'),  <-- C'est celle-ci qui bloquait !

    # Pages Graphiques
    path('graph-temp/', views.graph_temp, name='graph_temp'),
    path('graph-hum/', views.graph_hum, name='graph_hum'),
    path('graph-co/', views.graph_co, name='graph_co'),
    path('graph-light/', views.graph_light, name='graph_light'),

    # Export CSV
    path('download_csv/', views.download_csv, name='download_csv'),
]