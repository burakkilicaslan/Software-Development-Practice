from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    # path('<int:community_id>/', views.community, name = 'community')
]