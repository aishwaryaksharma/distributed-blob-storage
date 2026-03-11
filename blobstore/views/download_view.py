from rest_framework.views import APIView
from rest_framework.response import Response
from blobstore.models import BlobMetadata
from django.http import FileResponse, Http404
import os

class BlobDownloadView(APIView):
    def get(self, request, blob_id):
        # 1. Look up the metadata
        try:
            metadata = BlobMetadata.objects.get(id=blob_id)
        except BlobMetadata.DoesNotExist:
            raise Http404("Blob not found")

        # 2. Check if file exists on disk
        if not os.path.exists(metadata.storage_key):
            return Response({"error": "File missing on storage"}, status=404)

        # 3. Open the file in binary mode
        # FileResponse will automatically handle 'Content-Length' and 'Content-Type'
        file_handle = open(metadata.storage_key, 'rb')
        response = FileResponse(file_handle, content_type=metadata.content_type)
        
        # 4. Force 'Save As' behavior in the browser
        response['Content-Disposition'] = f'attachment; filename="{metadata.filename}"'
        
        return response