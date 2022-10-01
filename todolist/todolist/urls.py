from django.contrib import admin
from django.urls import path
from tasksapi.views import TasksViewSet


urlpatterns = [
    path('api/tasks/', TasksViewSet.as_view({'get':'filter','post':'create'})),
    path('api/tasks/<int:pk>/', TasksViewSet.as_view({'put':'update','get':'retrieve', 'delete':'destroy'})),
    path('api/tasks/to-do/', TasksViewSet.as_view({'get':'todo'})),
    path('api/tasks/expired/', TasksViewSet.as_view({'get':'expired'})),
    path('api/tasks/in_progress/', TasksViewSet.as_view({'get':'in_progress'})),
    path('api/tasks/done/', TasksViewSet.as_view({'get':'done'})),
    
]
