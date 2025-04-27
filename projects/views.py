from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project,Donation,Category
from .serializers import ProjectSerializer,DonationSerializer,CategorySerializer


# ___________________ CategoriesViewSet _____________________
class CategorViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # check user is logged in
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)



# ___________________ProjectViewSet_____________________
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    # check user is logged in
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
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


