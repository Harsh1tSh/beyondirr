from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, views
from rest_framework.response import Response
from .serializers import UserSignupSerializer, MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserSignupView(views.APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'email': user.email,
                'arn_number': user.arn_number
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from django.http import JsonResponse

def signup_view(request):
    if request.method == 'POST':
        print("Request Body:", request.body)  # Log raw request body
        serializer = UserSignupSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            return JsonResponse({"message": "User created successfully", "user_id": user.id}, status=201)
        else:
            print("Errors:", serializer.errors)  # Log serializer errors
            return JsonResponse({"errors": serializer.errors}, status=400)
    return JsonResponse({"message": "Invalid request"}, status=405)

