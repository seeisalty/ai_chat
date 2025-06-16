from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_ui, name='chat_ui'),
    path('stream/', views.chat_stream, name='chat_stream'),
]
