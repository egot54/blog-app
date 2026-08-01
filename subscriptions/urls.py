from django.urls import path
from . import views

urlpatterns = [
    path('toggle/<int:user_id>/', views.toggle_subscription, name='toggle_subscription'),
]