from django.urls import path
# from .views import schedule_zoom_meeting
from . import views

urlpatterns = [
    # path('schedule/', schedule_zoom_meeting, name='schedule_zoom_meeting'),
    # path('create-zoom-meeting/', views.create_meeting, name='create_zoom_meeting'),
    path('redirect/', views.redirect_to_zoom, name='zoom_redirect'),
    path('callback/', views.zoom_oauth_callback, name='zoom_oauth_callback'),
    path('create-meeting/', views.create_zoom_meeting, name='create_zoom_meeting'),


]
