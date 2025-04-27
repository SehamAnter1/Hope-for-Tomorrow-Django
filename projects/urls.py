
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet,DonationViewSet
router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('donations', DonationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('<int:project_id>/donate/', DonationViewSet.as_view(), name='donate_to_project'),

]