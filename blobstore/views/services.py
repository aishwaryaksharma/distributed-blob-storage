import os
import hashlib
from django.conf import settings
from django.db import transaction
from blobstore.models.blobmeta import BlobMetadata

class BlobUploadService:
    @staticmethod
    def handle_upload(uploaded_file):
        # 1. Define storage path (In prod, this would be S3)
        storage_dir = os.path.join(settings.MEDIA_ROOT, 'blobs')
        os.makedirs(storage_dir, exist_ok=True)
        
        sha256 = hashlib.sha256()
        temp_path = os.path.join(storage_dir, f"{uploaded_file.name}.tmp")

        # 2. Stream the file to disk and calculate checksum simultaneously
        with open(temp_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks(): # Django's chunking saves RAM
                sha256.update(chunk)
                destination.write(chunk)

        checksum = sha256.hexdigest()
        final_path = os.path.join(storage_dir, checksum)

        # 3. Atomic Transaction: Metadata + File Rename
        # This prevents "orphan files" if the DB save fails
        try:
            with transaction.atomic():
                # Deduplication check
                metadata, created = BlobMetadata.objects.get_or_create(
                    checksum=checksum,
                    defaults={
                        'filename': uploaded_file.name,
                        'content_type': uploaded_file.content_type,
                        'size_bytes': uploaded_file.size,
                        'storage_key': final_path
                    }
                )
                
                # If it's a new file, rename from temp to the checksum-based name
                if created:
                    os.rename(temp_path, final_path)
                else:
                    os.remove(temp_path) # Cleanup temp file if it's a duplicate
                
                return metadata
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e