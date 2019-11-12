from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('',views.Community_Listview.as_view(), name = 'index'),
    # path('<int:community_id>/', views.community, name = 'community')
]