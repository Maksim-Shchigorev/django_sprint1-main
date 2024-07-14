from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.index, name='index'),
    path('<int:pk>/', views.posts_detail, name='posts_detail'),
    path('<slug:category>/', views.posts_category, name='posts_category')

]
