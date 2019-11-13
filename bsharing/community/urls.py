from django.urls import path
from . import views
from .views import Community_Listview, Community_DetailView

app_name = "community"

urlpatterns = [
    path('',views.Community_Listview.as_view(), name = 'index'),
    path('<pk>/', views.Community_DetailView.as_view(), name = "community_detail"),
    path('community/add/', views.Community_Create.as_view(), name ="community_create")
    # path('<int:community_id>/', views.community, name = 'community')
]