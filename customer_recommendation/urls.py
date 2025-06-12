from django.urls import path
from . import views

urlpatterns = [
    path('cluster-detail/', views.recommend_items_view, name='recommend_items'),
    path('item-detail/', views.recommend_results_view, name='recommend_results'),
]
