from django.urls import path
from .views import MyTokenObtainPairView, UserSignupView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
]
