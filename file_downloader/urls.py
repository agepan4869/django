from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('directory/<path:directory>/', views.directory_files, name='directory_files'),
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
]