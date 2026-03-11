from django.urls import path

from .views import BlobUploadView, BlobDownloadView, BlobListView, BlobDeleteView

urlpatterns = [
    path('upload/', BlobUploadView.as_view(), name='blob-upload'),
    path('download/<uuid:blob_id>/', BlobDownloadView.as_view(), name='blob-download'),
    path('list/', BlobListView.as_view(), name='blob-list'),
    path('delete/<uuid:blob_id>/', BlobDeleteView.as_view(), name='blob-delete'),
]