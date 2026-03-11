import uuid
from django.db import models

class BlobMetadata(models.Model):
    # UUID prevents ID guessing and makes distributed merging easier
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100) # e.g., image/jpeg
    size_bytes = models.BigIntegerField()
    
    # Checksum for deduplication and corruption checks
    checksum = models.CharField(max_length=64, db_index=True) 
    
    # Internal path to where the file is physically stored
    storage_key = models.CharField(max_length=512)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blob_metadata'