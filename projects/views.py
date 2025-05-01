from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Project,Donation,Category
from .serializers import ProjectSerializer,DonationSerializer,CategorySerializer,TopDonatorsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F

# ___________________ CategoriesViewSet _____________________
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    parser_classes = (MultiPartParser, FormParser)
    # check user is logged in
    # permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

# ___________________ProjectViewSet_____________________
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    # check user is logged in
    # permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ['list','retrieve','latest_projects']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False,methods=['get'],url_path='latest',)
    def latest_projects(self,request):        
        latest = Project.objects.all().order_by('-created_at')[:3]
        serializer=self.get_serializer(latest,many=True)
        return Response(serializer.data)
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
        
# ___________________TopDonatorsViewSet_____________________
class TopDonatorsViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @action(detail=False,methods=['get'],url_path='overall',)
    def overall(self,request):        
        top_donators = (Donation.objects
        .values('user_id', username=F('user__email'))
        .annotate(total_donated=Sum('amount'))
        .order_by('-total_donated')[:5])
        serializer = TopDonatorsSerializer(top_donators, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'], url_path='project')
    def project_top_donators(self, request, pk=None):
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found"}, status=404)
    
        top_donators = (
    Donation.objects.filter(project_id=pk)
    .values('user_id', username=F('user__email'))
    .annotate(total_donated=Sum('amount'))
    .order_by('-total_donated')[:5]
)

    
        serializer = TopDonatorsSerializer(top_donators, many=True)
        return Response(serializer.data)
    
