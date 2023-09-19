from django.urls import path
from . import views

urlpatterns = [
    path('passages/', views.passage_list, name='passage_list'),
    path('', views.passage_list, name='passage_list1'),
    path('passage/', views.display_passage, name='display_passage'),
    path('capture_audio/', views.capture_audio, name='capture_audio'),
    path('results/', views.results, name='results')
    # Add more URLs as needed
]
