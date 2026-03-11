from django.urls import path
from .views import BlobUploadView

urlpatterns = [
    path('api/upload/', BlobUploadView.as_view(), name='upload'),    
]