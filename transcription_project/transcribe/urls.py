# urls.py

from django.urls import path
from .views import transcribe_view,download_transcribed_file

urlpatterns = [
    path('', transcribe_view, name='transcribe'),
    path('download-transcribed-file/', download_transcribed_file, name='download_transcribed_file'),
]
