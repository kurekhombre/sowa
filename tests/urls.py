from django.urls import path
from . import views

urlpatterns=[
    path('<str:pk_topic>/<str:pk_note>/', views.test, name='test'),
]