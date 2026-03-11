from rest_framework.views import APIView
from rest_framework.response import Response
from .services import BlobUploadService

class BlobUploadView(APIView):
    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=400)

        metadata = BlobUploadService.handle_upload(file_obj)
        
        return Response({
            "id": str(metadata.id),
            "filename": metadata.filename,
            "checksum": metadata.checksum,
            "size": metadata.size_bytes
        }, status=201)