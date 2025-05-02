
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import Subscribers
from .serializers import SubscriptionSerializer

class SubscriptionViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = Subscribers.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]
