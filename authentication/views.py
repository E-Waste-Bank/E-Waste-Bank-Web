from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request: HttpRequest):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            
            # asumsikan di awal user bkn admin
            role = "user"

            # check if user is admin
            if request.user.groups.exists():
                groups = request.user.groups.all()

                for group in groups:
                    if group.name == "admin":
                        role = "admin"
                        break
            
            return JsonResponse({
                "status": True,
                "message": "Successfully logged in!",
                "role": role
            }, status=200)
        
        else:
            return JsonResponse({
                "status": False,
                "message": "Failed to login, account is disabled."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Failed to login, check your email/password."
        }, status=401)

@csrf_exempt
def logout(request: HttpRequest):
    auth_logout(request)
    
    return JsonResponse({
        "status": True,
    }, status=200)