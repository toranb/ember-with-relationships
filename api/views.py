from api.models import Session
from api.serializers import SessionSerializer
from rest_framework.viewsets import ModelViewSet

class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
