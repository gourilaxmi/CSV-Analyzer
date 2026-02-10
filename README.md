# Chemical Equipment Data Visualizer

A full-stack application for uploading, processing, and visualizing chemical equipment data with Django REST API backend, React web frontend, and PyQt5 desktop application.

## 🎯 Features

### Core Functionality

- **User Authentication**: Secure JWT-based authentication with password reset capability
- **CSV Upload & Processing**: Upload chemical equipment datasets in CSV format
- **Real-time Status Updates**: Monitor processing progress with automatic polling
- **Data Visualizations**:
  - Equipment type distribution (Pie charts)
  - Equipment-wise averages for each parameter (Bar charts)
  - Outlier detection with boxplots (when outliers are present)
  - Correlation matrices for parameter relationships
- **PDF Report Generation**: Comprehensive reports with statistics and all visualizations
- **Upload History**: Track and access last 5 uploaded datasets via Downloads page
- **Multi-Platform Access**: Web interface, desktop application, and REST API

### Web Frontend (React)

- Modern, responsive UI
- Interactive charts using Chart.js
- Real-time processing status with auto-refresh
- Downloadable PDF reports from Downloads page
- User-friendly navigation

### Desktop Application (PyQt5)

- Native desktop performance
- High-quality Matplotlib visualizations
- Chart navigation with Previous/Next controls
- Same authentication system as web
- Auto-refresh status polling

## 🛠 Technology Stack

### Backend

- **Framework**: Django 5.2+
- **API**: Django REST Framework 3.15+
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Data Processing**: Pandas 2.2.0
- **Visualization**: Matplotlib 3.8.2, Seaborn
- **PDF Generation**: ReportLab 4.2.5
- **Database**: SQLite (Development) / PostgreSQL (Production)

### Frontend (Web)

- **Framework**: React 18.x
- **Routing**: React Router DOM
- **HTTP Client**: Native Fetch API
- **Charts**: Chart.js + react-chartjs-2
- **Styling**: CSS3 with responsive design

### Desktop Application

- **GUI Framework**: PyQt5 5.15.10
- **Visualizations**: Matplotlib 3.8.2
- **HTTP Client**: Requests 2.31.0
- **Image Processing**: Pillow 10.1.0

## 🏗 Project Structure
```
screening_task/
│
├── backend/                    # Django REST API
│   ├── config/                # Project configuration
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # Main URL routing
│   │   └── wsgi.py            # WSGI config
│   │
│   ├── datasets/              # Dataset management app
│   │   ├── models.py          # Database models
│   │   ├── serializers.py     # DRF serializers
│   │   ├── views.py           # API views
│   │   ├── urls.py            # Dataset URLs
│   │   ├── tasks.py           # Async processing
│   │   └── utils/             # Processing utilities
│   │       ├── csv.py         # CSV processing
│   │       ├── chart.py       # Visualization generation
│   │       └── pdf.py         # PDF report generation
│   │
│   ├── authentication/        # Authentication app
│   │   ├── models.py          # User models
│   │   ├── serializers.py     # Auth serializers
│   │   ├── views.py           # Auth views
│   │   └── urls.py            # Auth URLs
│   │
│   ├── media/                 # User uploaded content
│   │   ├── datasets/          # CSV files
│   │   ├── charts/            # Generated visualizations
│   │   └── pdfs/              # PDF reports
│   │
│   ├── manage.py              # Django management
│   └── requirements.txt       # Python dependencies
│
├── frontend/                  # React web application
│   ├── public/                # Static files
│   │   └── index.html
│   │
│   ├── src/                   # Source code
│   │   ├── components/        # React components
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── ForgotPassword.js
│   │   │   ├── MainPage.js
│   │   │   └── Downloads.js
│   │   │
│   │   ├── config.js          # API configuration
│   │   ├── apiHelper.js       # API utilities
│   │   ├── App.js             # Main component
│   │   └── index.js           # Entry point
│   │
│   ├── .env.local             # Environment variables
│   ├── package.json           # Node dependencies
│   └── .gitignore             # Git ignore rules
│
├── desktop/                   # PyQt5 desktop application
│   ├── main.py                # Main application file
│   └── requirements.txt       # Python dependencies
│
├── sample_equipment_data.csv  # Sample CSV for testing
├── README.md                  # This file
└── .gitignore                 # Git ignore rules
```

## ✅ Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **Node.js**: 14.x or higher
- **npm**: 6.x or higher
- **pip**: Latest version
- **Git**: For cloning repository

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/screening_task.git
cd screening_task
```

### 2. Backend Setup (Django)

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

**Backend requirements.txt:**
```txt
Django==5.2.10
djangorestframework==3.15.2
djangorestframework-simplejwt==5.4.0
django-cors-headers==4.6.0
pandas==2.2.0
matplotlib==3.8.2
seaborn==0.12.0
reportlab==4.2.5
Pillow==10.1.0
```

#### Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Run Backend Server
```bash
python manage.py runserver
```

✅ **Backend running at:** http://localhost:8000

### 3. Frontend Setup (React)

Open a new terminal:

#### Navigate to Frontend Directory
```bash
cd frontend
```

#### Install Dependencies
```bash
npm install
```

#### Configure Environment

Create `.env.local` file in `frontend/src` directory:
```env
REACT_APP_API_URL=http://localhost:8000
```

#### Run Frontend Server
```bash
npm start
```

✅ **Frontend running at:** http://localhost:3000

### 4. Desktop Application Setup (PyQt5)

Open a new terminal:

#### Navigate to Desktop Directory
```bash
cd desktop
```

#### Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

**Desktop requirements.txt:**
```txt
PyQt5==5.15.10
matplotlib==3.8.2
Pillow==10.1.0
requests==2.31.0
```

#### Run Desktop Application
```bash
python main.py
```

✅ **PyQt5 desktop application launches**

## ▶️ Running the Application

### Quick Start Guide

You need **3 terminal windows** for full functionality:

**Terminal 1 - Backend (Django)**
```bash
cd backend
python manage.py runserver
```

**Terminal 2 - Frontend (React)**
```bash
cd frontend
npm start
```

**Terminal 3 - Desktop App (PyQt5)**
```bash
cd desktop
python main.py
```

## 📖 Usage Guide

### Web Interface (React)

#### 1. Registration & Login

1. Navigate to http://localhost:3000
2. Click **"Register"** to create a new account
3. Fill in: Username, Email, First Name, Last Name, Password
4. Or click **"Login"** with existing credentials

#### 2. Forgot Password

1. Click **"Forgot Password?"** on login page
2. Enter your username or email
3. Set new password in the modal

#### 3. Upload Dataset

1. After login, you'll see the Main Page
2. Click **"Upload Dataset"** button
3. Select a CSV file with chemical equipment data
4. Click **"Upload"**
5. Processing status updates automatically (Pending → Processing → Completed)

#### 4. View Visualizations (Chart.js)

Once processing completes, visualizations appear:

- **Equipment Type Distribution**: Pie chart showing equipment distribution
- **Equipment Averages**: Bar charts for each parameter (Flowrate, Pressure, Temperature, etc.)
- **Outlier Analysis**: Boxplots for parameters with detected outliers
- **Correlation Matrix**: Heatmap showing parameter relationships

#### 5. Download PDF Report

1. Click **"Download PDF Report"** button
2. PDF includes all statistics, charts, and analysis

#### 6. View History

1. Navigate to **"Downloads"** page
2. View your last 5 uploaded datasets
3. Check processing status for each
4. Download PDF reports from completed datasets
5. See upload timestamps and file details

### Desktop Application (PyQt5)

#### 1. Login

1. Launch the application with `python main.py`
2. Enter your Django username and password (same as web)
3. Click **"Login"**

#### 2. Upload & Process

1. In **"Upload Dataset"** tab
2. Click **"Select CSV File"** button
3. Choose your dataset
4. Click **"Upload & Process"**
5. Status updates automatically every 3 seconds
6. Progress indicator shows processing state

#### 3. View Visualizations (Matplotlib)

1. Switch to **"Visualizations"** tab after processing completes
2. High-quality Matplotlib charts display:
   - Equipment type distribution (Pie chart)
   - Equipment-wise parameter averages (Bar charts)
   - Outlier boxplots (if outliers detected)
   - Correlation matrix (Heatmap)
3. Use **"Previous"** and **"Next"** buttons to navigate
4. Chart counter shows position 

#### 4. Download Report

1. Return to **"Upload Dataset"** tab
2. Click **"Download PDF Report"** when status is "Completed"
3. Choose save location
4. PDF contains all statistics and visualizations

#### 5. View History

1. Switch to **"History"** tab
2. Click **"Refresh History"** to see latest uploads
3. View last 5 datasets
4. Click **"View"** on any dataset to load its visualizations

## 🔌 API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securePassword123",
  "password2": "securePassword123"
}
```

**Response: 201 Created**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json
```

**Request Body:**
```json
{
  "login_id": "john_doe",
  "password": "securePassword123"
}
```

**Response: 200 OK**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "Login successful"
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response: 200 OK**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout
```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response: 200 OK**
```json
{
  "message": "Logout successful"
}
```

#### Password Reset Request
```http
POST /api/auth/password-reset-request/
Content-Type: application/json
```

**Request Body:**
```json
{
  "login_id": "john_doe"
}
```

**Response: 200 OK**
```json
{
  "message": "User verified. You can now reset your password."
}
```

#### Password Reset Confirm
```http
POST /api/auth/password-reset-confirm/
Content-Type: application/json
```

**Request Body:**
```json
{
  "login_id": "john_doe",
  "new_password": "newPassword123",
  "new_password2": "newPassword123"
}
```

**Response: 200 OK**
```json
{
  "message": "Password reset successful"
}
```

### Dataset Endpoints

#### Upload Dataset
```http
POST /api/upload-dataset/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Form Data:**
- `dataset_file`: <file.csv>

**Response: 202 Accepted**
```json
{
  "message": "File uploaded successfully. Analysis is in progress.",
  "dataset_id": 1,
  "status": "pending"
}
```

#### List User Datasets (Last 5)
```http
GET /api/datasets/
Authorization: Bearer <access_token>
```

**Response: 200 OK**
```json
[
  {
    "id": 1,
    "dataset_file": "/media/datasets/equipment_data.csv",
    "pdf_file": "/media/pdfs/report_1.pdf",
    "status": "completed",
    "error_log": null,
    "uploaded_at": "2024-02-10T10:30:00Z"
  },
  {
    "id": 2,
    "dataset_file": "/media/datasets/equipment_data_2.csv",
    "pdf_file": null,
    "status": "processing",
    "error_log": null,
    "uploaded_at": "2024-02-10T11:00:00Z"
  }
]
```

#### Get Dataset Status & Analysis
```http
GET /api/dataset-status/<dataset_id>/
Authorization: Bearer <access_token>
```

**Response: 200 OK**
```json
{
  "dataset_id": 1,
  "status": "completed",
  "uploaded_at": "2024-02-10T10:30:00Z",
  "analysis": {
    "total_rows": 100,
    "equipment_distribution": {
      "Reactor": 25,
      "Pump": 20,
      "HeatEx": 30,
      "Column": 15,
      "Compressor": 10
    },
    "equipment_averages": {
      "Reactor": {
        "Flowrate": 150.5,
        "Pressure": 2.5,
        "Temperature": 350.0
      },
      "Pump": {
        "Flowrate": 200.0,
        "Pressure": 3.0,
        "Temperature": 25.0
      }
    },
    "field_statistics": {
      "Flowrate": {
        "mean": 175.5,
        "std": 45.2,
        "min": 95.7,
        "max": 300.5
      }
    },
    "outliers": {
      "Flowrate": 5,
      "Pressure": 3
    },
    "correlation_data": {
      "Flowrate": {
        "Pressure": 0.75,
        "Temperature": 0.45
      }
    }
  }
}
```

#### Download PDF Report
```http
GET /api/download-pdf/<dataset_id>/
Authorization: Bearer <access_token>
```

**Response: 200 OK**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="pdf_report_1.pdf"
```

## 📊 Data Processing & Visualizations

### Processing Pipeline

1. **CSV Upload**: User uploads CSV file
2. **Data Cleaning**:
   - Missing numeric values filled with median
   - Missing categorical values filled with "Unknown"
3. **Outlier Detection**: IQR method identifies outliers
4. **Outlier Handling**: Capping strategy 
5. **Statistics Calculation**:
   - Field statistics (mean, std, min, max, quartiles)
   - Equipment type distribution
   - Equipment-wise averages for each parameter
6. **Visualization Generation**:
   - Equipment distribution pie chart
   - Equipment averages bar charts
   - Outlier boxplots (if outliers exist)
   - Correlation matrix heatmap
7. **PDF Report Generation**: All statistics and charts compiled

### Visualizations Included

#### 1. Equipment Type Distribution
- **Type**: Pie chart
- **Purpose**: Shows proportion of each equipment type
- **Web**: Chart.js
- **Desktop**: Matplotlib

#### 2. Equipment-Wise Averages
- **Type**: Bar charts (one per parameter)
- **Purpose**: Shows average values for each parameter by equipment type
- **Parameters**: Flowrate, Pressure, Temperature, Efficiency, etc.
- **Web**: Chart.js
- **Desktop**: Matplotlib

#### 3. Outlier Analysis
- **Type**: Boxplots
- **Purpose**: Identifies outliers in numeric parameters
- **Condition**: Only shown if outliers detected
- **Method**: IQR (Interquartile Range)
- **Web**: Chart.js
- **Desktop**: Matplotlib

#### 4. Correlation Matrix
- **Type**: Heatmap
- **Purpose**: Shows relationships between numeric parameters
- **Range**: -1 to 1 (negative to positive correlation)
- **Web**: Chart.js
- **Desktop**: Matplotlib


## 📝 Notes

- **Processing**: Runs asynchronously using threading (production should use Celery)
- **Auto-refresh**: Frontend polls every 3 seconds for status updates
- **History Limit**: Last 5 datasets stored per user
- **File Storage**: Media files stored in `/media/` directory
- **Authentication**: Same credentials work for both web and desktop

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created for: **FOSSEE Internship Screening Task**

**Version**: 1.0.0  
**Last Updated**: February 2026


