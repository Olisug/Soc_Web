from django.urls import path

from . import views

app_name = 'Posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('my_posts/', views.show_my_posts, name='my_posts'),
    path('create_post/', views.create, name='create_post'),
    path('edit_post/<int:pk>', views.EditPost.as_view(), name='edit_post'),
    path('delete/<int:id>', views.delete, name='delete_post'),
    path('like/<int:post_id>/', views.like, name='like'),
    path('liked_posts/', views.show_liked_posts, name='liked_posts'),
    path('<int:user_id>/another_profile_posts/', views.show_another_profile_posts, name='another_user_posts')]
