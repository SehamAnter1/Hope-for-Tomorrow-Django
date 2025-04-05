# zoom_app/views.py
import base64
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from django.conf import settings
import requests
from django.shortcuts import redirect

client_id = settings.ZOOM_CLIENT_ID
client_secret = settings.ZOOM_CLIENT_SECRET
redirect_uri = settings.ZOOM_REDIRECT_URI
@csrf_exempt
def redirect_to_zoom(request):
    client_id = settings.ZOOM_CLIENT_ID
    redirect_uri = settings.ZOOM_REDIRECT_URI
    zoom_url = f"https://zoom.us/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    return redirect(zoom_url)
def zoom_oauth_callback(request):
    code = request.GET.get('code') 
    if not code:
        return JsonResponse({"error": "Code not found in request"})

    token_url = "https://zoom.us/oauth/token"
    client_id = settings.ZOOM_CLIENT_ID
    client_secret = settings.ZOOM_CLIENT_SECRET
    redirect_uri = settings.ZOOM_REDIRECT_URI

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }

    response = requests.post(token_url, data=data, auth=(client_id, client_secret))

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return JsonResponse({"access_token": access_token})
    else:
        return JsonResponse({"error": "Failed to get access token", "details": response.json()})

@csrf_exempt
def create_zoom_meeting(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "Access token is missing or invalid"}, status=400)

    access_token = auth_header.split(" ")[1]

    # Zoom API URL for creating meetings
    url = "https://api.zoom.us/v2/users/me/meetings"

    # Meeting data
    meeting_data = {
        "topic": "Test Meeting",
        "type": 2, 
        "start_time": "2025-01-30T10:00:00Z",  # ISO 8601 format
        "duration": 30,  # Duration in minutes
        "password": "123456"
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, json=meeting_data)
        response.raise_for_status() 

        meeting_url = response.json().get('join_url')
        return JsonResponse({
            "message": "Meeting created successfully",
            "meeting_url": meeting_url
        })

    except requests.exceptions.RequestException as e:
        error_message = str(e)
        return JsonResponse({
            "error": "Zoom API Error",
            "details": error_message,
            "response_text": response.text if 'response' in locals() else None,
        }, status=response.status_code if 'response' in locals() else 500)
@csrf_exempt
def exchange_code_for_token(request):
    code = request.GET.get('code')  

    client_id = settings.ZOOM_CLIENT_ID
    client_secret = settings.ZOOM_CLIENT_SECRET
    redirect_uri = settings.ZOOM_REDIRECT_URI

    url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        refresh_token = response.json().get('refresh_token')
        return JsonResponse({
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    else:
        return JsonResponse({"error": response.json()}, status=response.status_code)

    access_token = request.GET.get('access_token')  # You should save this token after OAuth
    if not access_token:
        return JsonResponse({"error": "Access token is missing"}, status=400)

    result = create_zoom_meeting(access_token)
    return JsonResponse(result)