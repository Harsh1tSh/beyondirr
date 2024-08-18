from django.urls import path
from .views import MyTokenObtainPairView, UserSignupView, TransactionUploadView, TransactionSummaryView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('upload-transactions/', TransactionUploadView.as_view(), name='upload-transactions'),
    path('summary/', TransactionSummaryView.as_view(), name='transaction-summary'),
]
