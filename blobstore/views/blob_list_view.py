from rest_framework.views import APIView
from rest_framework.response import Response
from blobstore.models import BlobMetadata

class BlobListView(APIView):
    def get(self, request):
        blobs = BlobMetadata.objects.all().order_by('-created_at')[:10]
        data = [{
            "id": b.id,
            "filename": b.filename,
            "size": b.size_bytes,
            "download_url": f"/api/download/{b.id}/"
        } for b in blobs]
        return Response(data)