from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('position/', views.position, name='position'),

    path('start_strategy/', views.start_strategy, name='start_strategy'),
]