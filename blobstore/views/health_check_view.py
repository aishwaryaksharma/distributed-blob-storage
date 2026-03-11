from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def system_health_check(request):
    return Response({
        "status": "online",
        "service": "Blob Storage System",
        "version": "1.0.0"
    })