from django.shortcuts import render

# Create your views here.


# react
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt 
def user_loginnn(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from Website.models import ProductCategory
def show_user(request):
    # Retrieve all user profiles from the database
    user_profiles = ProductCategory.objects.all()
    
    # Convert user profiles to JSON format
    user_profiles_json = [
        {
            'id': profile.categ_id,
            'name': profile.categ_name,
            'image': request.build_absolute_uri(profile.categ_image.url) if profile.categ_image else None,
            'craeted_at': profile.created_at,

        }
        for profile in user_profiles
    ]
    
    # Return the user profiles as a JSON response
    return JsonResponse(user_profiles_json, safe=False)