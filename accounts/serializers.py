from rest_framework import serializers
from .models import User, Transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.db import transaction as db_transaction
import pandas as pd


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


def validate_arn_selenium(arn_number, user_email):
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://www.amfiindia.com/locate-your-nearest-mutual-fund-distributor-details')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "NearestFinAdvisorsARN")))

        arn_input = driver.find_element(By.ID, "NearestFinAdvisorsARN")
        arn_input.send_keys(arn_number)
        submit_button = driver.find_element(By.ID, 'hrfGo')
        submit_button.click()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "divExcel")))

        results_table = driver.find_element(By.ID, 'divExcel').find_element(By.TAG_NAME, 'tbody')
        rows = results_table.find_elements(By.TAG_NAME, 'tr')

        for index, row in enumerate(rows):
            if index == 0:
                continue  # skip header
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) < 5:  
                continue
            arn_from_table = cells[1].text.strip()
            email_from_table = cells[5].text.strip()
            print(f"Row {index}: ARN={arn_from_table}, Email={email_from_table}")  # Debug output

            if arn_from_table == arn_number and email_from_table.lower() == user_email.lower():
                return True
        return False  
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    finally:
        driver.quit()


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'arn_number']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        arn_number = attrs.get('arn_number')
        email = attrs.get('email')
        print(arn_number)
        print(email)
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
    

class TransactionUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError("Invalid file format. Please upload an Excel file.")
        return value

    def create(self, validated_data):
        file = validated_data.get('file')
        user = self.context['request'].user

        try:
            print("Reading Excel file...")
            df = pd.read_excel(file)
            print("Excel file read successfully!")

            # Process each row in the Excel file
            for _, row in df.iterrows():
                print(f"Processing row: {row}")
                try:
                    with db_transaction.atomic():
                        # try to update the existing transaction
                        transaction_instance = Transaction.objects.get(
                            user=user,
                            product=row['Product'],
                            date=row['Date']
                        )
                        transaction_instance.asset_class = row['Asset Class']
                        transaction_instance.units = row['Units']
                        transaction_instance.amount = row['Amount']
                        transaction_instance.save()
                        print(f"Updated existing transaction: {transaction_instance}")
                except Transaction.DoesNotExist:
                    # If the transaction does not exist, create it
                    Transaction.objects.create(
                        user=user,
                        product=row['Product'],
                        asset_class=row['Asset Class'],
                        date=row['Date'],
                        units=row['Units'],
                        amount=row['Amount']
                    )
                    print(f"Created new transaction: {row['Product']} on {row['Date']}")
        except Exception as e:
            print(f"Error while processing file: {str(e)}")
            raise serializers.ValidationError(f"Error processing file: {str(e)}")
        return {"status": "success"}
