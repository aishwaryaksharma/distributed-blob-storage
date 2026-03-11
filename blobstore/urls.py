from django.urls import path

from .views import BlobUploadView, BlobDownloadView

urlpatterns = [
    path('upload/', BlobUploadView.as_view(), name='blob-upload'),
    path('download/<uuid:blob_id>/', BlobDownloadView.as_view(), name='blob-download'),
]