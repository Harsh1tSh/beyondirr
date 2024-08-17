from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def validate_arn_selenium(arn_number, user_email):
    options = Options()
    options.headless = True  
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://www.amfiindia.com/locate-your-nearest-mutual-fund-distributor-details')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))  

        arn_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "NearestFindAdvisorsARN"))
        )
        arn_input.send_keys(arn_number)
        
        submit_button = driver.find_element(By.XPATH, '//input[@value="Go"]')
        submit_button.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'divExcel'))) 
        results_table = driver.find_element(By.TAG_NAME, 'table')
        rows = results_table.find_elements(By.TAG_NAME, 'tr')
        
        for row in rows[1:]:  # Skip header row
            cells = row.find_elements(By.TAG_NAME, 'td')
            arn_from_table = cells[0].text.strip()  
            email_from_table = cells[4].text.strip()  
            if arn_from_table == arn_number and email_from_table.lower() == user_email.lower():
                return True

        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    finally:
        driver.quit()

# :(

# import requests
# from bs4 import BeautifulSoup

# def verify_arn(arn_number, signup_email):
#     # URL of the form
#     url = "https://www.amfiindia.com/locate-your-nearest-mutual-fund-distributor-details"

#     # Form data
#     data = {
#         'AMFI Registration Number(ARN)': arn_number,

#     }

#     # Submit the form
#     response = requests.post(url, data=data)

#     # Check if the request was successful
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         table = soup.find('table', {'id': 'NearestFindAdvisorsARN'}) 

#         # Extract email from the table
#         email_from_table = None
#         for row in table.find_all('tr'):
#             cols = row.find_all('td')
#             if len(cols) > 1: 
#                 if "Email" in cols[0].text:
#                     email_from_table = cols[1].text.strip()
#                     break
        
   
#         if email_from_table == signup_email:
#             return True
#         else:
#             return False

#     else:
#         return False


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'arn_number']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        arn_number = attrs.get('arn_number')
        email = attrs.get('email')
        if not validate_arn_selenium(arn_number, email):
            raise serializers.ValidationError({"arn_number": "ARN number is invalid or does not match the provided email."})
        return attrs

    # def validate(self, attrs):
    #     arn_number = attrs.get('arn_number')
    #     email = attrs.get('email')
    #     if not verify_arn(arn_number, email):
    #         raise serializers.ValidationError({"arn_number": "ARN number is invalid or does not match the provided email."})
    #     return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            arn_number=validated_data['arn_number']
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
