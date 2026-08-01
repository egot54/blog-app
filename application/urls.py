from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('addblog/', views.addblog, name='addblog'),
    path('blog/<str:title>/', views.blogcontent, name='blogcontent'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('feed/', views.feed, name='feed'),
    path('request-access/<int:post_id>/', views.request_access, name='request_access'),
    path('approve-access/<int:request_id>/', views.approve_access, name='approve_access'),
    path('my-requests/', views.my_requests, name='my_requests'),
]