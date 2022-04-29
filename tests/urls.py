from django.urls import path
from . import views

urlpatterns=[
    path('test/<str:pk_topic>/<str:pk_note>/', views.test, name='test'),
]