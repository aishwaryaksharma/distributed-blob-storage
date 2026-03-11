import os
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from blobstore.models import BlobMetadata

class BlobDeleteView(APIView):
    def delete(self, request, blob_id):
        try:
            # 1. Find the metadata first to get the file path
            metadata = BlobMetadata.objects.get(id=blob_id)
            file_path = metadata.storage_key
            
            # 2. Use a transaction to ensure DB deletion is clean
            with transaction.atomic():
                metadata.delete()
                
                # 3. Physical file deletion
                # Only delete from disk IF the DB record was successfully removed
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            return Response({"message": "Successfully deleted from DB and disk"}, status=204)
            
        except BlobMetadata.DoesNotExist:
            return Response({"error": "Blob not found"}, status=404)
        except Exception as e:
            # Log the error (e.g., file permission issues)
            return Response({"error": f"Deletion failed: {str(e)}"}, status=500)