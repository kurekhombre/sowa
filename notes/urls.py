from django.urls import path
from . import views

urlpatterns = [
    path('', views.topic_list, name='topic-list'),
    path('create-topic/', views.create_topic, name='create-topic'),
    path('update-topic/<str:pk>/', views.update_topic, name='update-topic'),
    path('delete-topic/<str:pk>/', views.delete_topic, name='delete-topic'),
    path('<str:pk>/', views.topic_detail, name='topic-detail'),
    path('<str:pk_topic>/<str:pk_note>', views.note_view, name='note-detail'),
    path('<str:pk>/create-note/', views.create_note, name='create-note'),
    path('<str:pk_topic>/update-note/<str:pk_note>', views.update_note, name='note-update'),
]