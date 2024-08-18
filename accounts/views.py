from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSignupSerializer, MyTokenObtainPairSerializer, TransactionUploadSerializer
from .decorators import log_request
from .models import Transaction
from django.db.models import Sum, F, Q
from datetime import date


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
        
# Not tested yet, Incomplete
class TransactionSummaryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        summary = {}
        for year in range(2023, 2026): 
            start_date = date(year, 4, 1)
            end_date = date(year + 1, 3, 31)

            year_label = f"FY{year % 100}-{(year + 1) % 100}"
            summary[year_label] = {
                'Equity': self.get_net_transactions(user, 'Equity', start_date, end_date),
                'Debt': self.get_net_transactions(user, 'Debt', start_date, end_date),
                'Alternate': self.get_net_transactions(user, 'Alternate', start_date, end_date),
            }

        return Response(summary, status=status.HTTP_200_OK)

    def get_net_transactions(self, user, asset_class, start_date, end_date):
        result = Transaction.objects.filter(
            user=user,
            asset_class=asset_class,
            date__range=(start_date, end_date)
        ).aggregate(net=Sum(F('amount')))
        return result['net'] if result['net'] is not None else 0