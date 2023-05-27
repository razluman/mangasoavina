from rest_framework import permissions, viewsets
from .serializers import ApvSerializer
from .models import Apv


class ApvViewSet(viewsets.ModelViewSet):
    queryset = Apv.objects.all()
    serializer_class = ApvSerializer
    permission_classes = [permissions.IsAuthenticated]
