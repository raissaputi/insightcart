from django.urls import path
from .views import dashboard_view, cluster_detail_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('cluster-detail/', cluster_detail_view, name='cluster_detail'),
]
