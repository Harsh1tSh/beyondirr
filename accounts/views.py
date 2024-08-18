from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSignupSerializer, MyTokenObtainPairSerializer, TransactionUploadSerializer
from .decorators import log_request


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserSignupView(views.APIView):
    @log_request(record_success=True)  # used custom decorator here
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


# Should i use decorator here too?  
class TransactionUploadView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)
    @log_request(record_success=True)
    def post(self, request, *args, **kwargs):
        serializer = TransactionUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Transactions updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

