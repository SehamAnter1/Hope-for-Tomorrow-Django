from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Project
from .serializers import ProjectSerializer

# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    # check user is logged in
    permission_classes = [permissions.IsAuthenticated]
    def create_project(self,serializer):
        serializer.save(user=self.request.user)

