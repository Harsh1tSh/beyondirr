# BeyondIRR Hiring Assignment - August 2024


## Project Overview
This project is a submission for the BeyondIRR Hiring Assignment, August 2024. The assignment focuses on developing a Django-based FinTech application with various features like JWT authentication, custom user models, ARN validation, transaction management, and more.

## Features Implemented
1. **JWT Authentication**: Secure API endpoints with JWT using the RS256 algorithm.
2. **Custom User Model**: A custom user model that includes email and ARN number as unique fields.
3. **ARN Validation**: Integration with AMFI to validate ARN numbers during the user signup process.
4. **Transaction Management**: Users can upload Excel files to update their transaction records.
5. **Yearly Transaction Summary**: Endpoint to generate a summary of transactions by asset class for each financial year.
6. **Error Logging**: Custom decorator to log request and response details for debugging and audit purposes.

## Technologies Used
- **Django 5.1**: Web framework for the project.
- **Django REST Framework**: For building RESTful APIs.
- **Simple JWT**: For JWT authentication.
- **Selenium**: For scraping the AMFI website to validate ARN numbers.
- **Pandas**: For processing Excel files in the transaction upload feature.
- **SQLite**: Database for development.

## Setup Instructions

### Prerequisites
- Python 3.x
- Virtualenv (optional but recommended)

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd beyondirr
2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
4. **Apply migrations:**
    ```bash
    python manage.py migrate
5. **Create a superuser:**
   ```bash
    python manage.py createsuperuser
6. **Run the Development server:**
    ```bash
    python manage.py runserver


## API Documentation

### 1. User Authentication
- **Login**: `/api/login/` (POST)
  - **Request**: `email`, `password`
  - **Response**: `JWT token`

- **Signup**: `/api/signup/` (POST)
  - **Request**: `email`, `password`, `arn_number`
  - **Response**: User details

### 2. Transaction Management
- **Upload Transactions**: `/api/upload-transactions/` (POST)
  - **Request**: Excel file with transactions.
  - **Response**: Success message.

- **Yearly Summary**: `/api/summary/` (GET)
  - **Response**: Yearly transaction summary by asset class.

## Project Structure
beyondirr/
│
├── beyondirr/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── decorators.py
│
├── manage.py
├── requirements.txt
├── README.md
├── initial_data.json (optional)
└── venv/ (optional, not included in the repository)

