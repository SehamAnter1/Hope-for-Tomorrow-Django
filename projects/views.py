from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project,Donation
from .serializers import ProjectSerializer,DonationSerializer

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
        print(f"Received project_id: {project_id}")
    
        try:
            project = Project.objects.get(id=project_id)
            print(f"Project found: {project.title}")
        except Project.DoesNotExist:
            print(f"Project with ID {project_id} does not exist.")
            return  
    
        serializer.save(user=self.request.user, project=project)

