from django.urls import path
from . import views
from .views import Community_Listview, Community_DetailView, login, register_form

app_name = "community"

urlpatterns = [
    path('',views.Community_Listview.as_view(), name = 'index'),
    path('<pk>/', views.Community_DetailView.as_view(), name = "community_detail"),
    path('community/add/', views.Community_Create, name ="community_create"),
    path('add/<int:community_header_id>/', views.post_type_create, name ="post_type_create"),
    path('post_type_detail/<pk>/', views.Post_Type_DetailView.as_view(), name = "post_type_detail"),
    path('post/add/<int:post_type_id>/', views.post_create, name = "post_create"),
    path('community/registration/', views.register_form.as_view(), name="register"),
    path('community/login/', views.login_user.as_view(), name= "login"),
    path('community/logout/', views.UserLogout, name= "logout")
    # path('<int:community_id>/', views.community, name = 'community')
]