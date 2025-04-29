from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Project,Donation,Category
from .serializers import ProjectSerializer,DonationSerializer,CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action

# ___________________ CategoriesViewSet _____________________
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)
    # check user is logged in
    # permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ['list','retreive']:
            return [AllowAny()]
        return [IsAuthenticated()]

# ___________________ProjectViewSet_____________________
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    # check user is logged in
    # permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ['list','retreive']:
            return [AllowAny()]
        return [IsAuthenticated()]

    
    def perform_create(self,serializer):
        serializer.save()
        serializer.save(user=self.request.user)


# ___________________DonationViewSet_____________________
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all().order_by('-created_at')
    serializer_class = DonationSerializer
    # check user is logged in
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        project_id = self.request.data.get('project_id')  
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return  
    
        serializer.save(user=self.request.user, project=project)


