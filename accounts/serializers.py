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
    options.headless = True  # Running in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://www.amfiindia.com/locate-your-nearest-mutual-fund-distributor-details')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))  

        # Find and fill the ARN input field
        arn_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "NearestFindAdvisorsARN"))
        )
        arn_input.send_keys(arn_number)
        print(arn_number)

        # Submit the form
        submit_button = driver.find_element(By.XPATH, '//input[@value="Go"]')
        submit_button.click()

        # Wait for results to load and parse them
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body"))) 
        results_table = driver.find_element(By.ID, 'divExcel')
        rows = results_table.find_elements(By.TAG_NAME, 'tr')
        
        for row in rows:  
            cells = row.find_elements(By.TAG_NAME, 'th')
            arn_from_table = cells[1].text.strip()  
            email_from_table = cells[5].text.strip()  
            if arn_from_table == arn_number and email_from_table.lower() == user_email.lower():
                return True

        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    finally:
        driver.quit()
# :(


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
