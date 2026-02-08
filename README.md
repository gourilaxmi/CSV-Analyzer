# Chemical Equipment Data Visualizer

A full-stack application for uploading, processing, and visualizing chemical equipment data with **Django REST API backend**, **React web frontend**, and **PyQt5 desktop application**.

## 🎯 Features

### Core Functionality
- **User Authentication**: Secure JWT-based authentication system
- **CSV Upload & Processing**: Upload chemical equipment datasets in CSV format
- **Real-time Status Updates**: Monitor processing progress with automatic polling
- **Data Visualizations**: 
  - Histograms for numeric distributions
  - Boxplots for outlier detection
  - Correlation matrices for relationship analysis
- **PDF Report Generation**: Comprehensive reports with statistics and charts
- **Upload History**: Track and access last 5 uploaded datasets
- **Multi-Platform Access**: Web interface, desktop application, and REST API

### Web Frontend (React)
- Modern, responsive UI
- Interactive charts using Chart.js
- Real-time processing status
- Downloadable PDF reports
- User-friendly navigation

### Desktop Application (PyQt5)
- Native desktop performance
- High-quality Matplotlib visualizations
- Offline capability (after authentication)
- Chart navigation with Previous/Next controls
- Auto-refresh status polling

---

## 🛠 Technology Stack

### Backend
- **Framework**: Django 5.2.10
- **API**: Django REST Framework 3.15.2
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Data Processing**: Pandas 2.2.0
- **Visualization**: Matplotlib 3.8.2
- **PDF Generation**: ReportLab 4.2.5
- **Task Queue**: Celery 5.3.4 (Production)
- **Message Broker**: Redis 5.0.1 (Production)
- **Database**: SQLite (Development) / PostgreSQL (Production)

### Frontend
- **Framework**: React 18.x
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Charts**: Chart.js + react-chartjs-2
- **Styling**: CSS3 with responsive design

### Desktop Application
- **GUI Framework**: PyQt5 5.15.10
- **Visualizations**: Matplotlib 3.8.2
- **HTTP Client**: Requests 2.31.0
- **Image Processing**: Pillow 10.1.0

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                       │
├──────────────────┬──────────────────┬──────────────────────┤
│  React Web App   │  PyQt5 Desktop   │   Mobile/External    │
│  (Port 3000)     │    Application   │   API Consumers      │
└────────┬─────────┴────────┬─────────┴──────────┬───────────┘
         │                  │                    │
         └──────────────────┼────────────────────┘
                            │
                   ┌────────▼────────┐
                   │  Django REST    │
                   │   Framework     │
                   │  (Port 8000)    │
                   └────────┬────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
    │ Database│      │   Celery   │     │   Redis   │
    │(SQLite/ │      │   Worker   │     │  (Broker) │
    │  Postgres)│      │(Async Tasks)│     │           │
    └─────────┘      └───────────┘     └───────────┘
                            │
                     ┌──────▼──────┐
                     │ Media Files │
                     │ - Uploads   │
                     │ - Charts    │
                     │ - Reports   │
                     └─────────────┘
```

---

## ✅ Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Node.js**: 14.x or higher
- **npm**: 6.x or higher
- **pip**: Latest version
- **Git**: For cloning repository

### Optional (Production)
- **PostgreSQL**: 12 or higher
- **Redis**: 5.0 or higher
- **Nginx**: For reverse proxy
- **Gunicorn**: WSGI HTTP Server

---

## 🚀 Installation & Setup

### Clone the Repository

```bash
git clone <repository-url>
cd screening_task
```

---

### 1. Backend Setup (Django)

#### Step 1.1: Create Virtual Environment

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### Step 1.2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Backend `requirements.txt`:**
```txt
Django==5.2.10
djangorestframework==3.15.2
djangorestframework-simplejwt==5.4.0
django-cors-headers==4.6.0
pandas==2.2.0
matplotlib==3.8.2
reportlab==4.2.5
Pillow==10.1.0
```


#### Step 1.4: Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
```


#### Step 1.5: Create Media Directories

```bash
# Windows
mkdir media\uploads media\charts media\reports

# macOS/Linux
mkdir -p media/uploads media/charts media/reports
```

#### Step 1.6: Run Development Server

```bash
python manage.py runserver
```

✅ Backend should now be running at: **http://localhost:8000**

---

### 2. Frontend Setup (React)

Open a **new terminal** (keep backend running):

#### Step 2.1: Navigate to Frontend

```bash
cd frontend
```

#### Step 2.2: Install Dependencies

```bash
npm install
```

**Frontend `package.json` dependencies:**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0"
  }
}
```

#### Step 2.3: Configure Environment

Create `.env.local` file in `frontend/` directory:

**Development (.env.local):**
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_MEDIA_URL=http://localhost:8000/media
REACT_APP_ENV=development
```

#### Step 2.4: Run Development Server

```bash
npm start
```

✅ Frontend should now be running at: **http://localhost:3000**

#### Step 2.5: Build for Production

```bash
npm run build
```

This creates optimized production files in `build/` directory.

---

### 3. Desktop App Setup (PyQt5)

Open a **new terminal**:

#### Step 3.1: Navigate to Desktop Directory

```bash
cd desktop
```

#### Step 3.2: Create Virtual Environment (Recommended)

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

#### Step 3.3: Install Dependencies

**Option A - Using Requirements File:**
```bash
pip install -r requirements.txt
```

**Option B - Manual Installation:**
```bash
pip install PyQt5==5.15.10 matplotlib==3.8.2 Pillow==10.1.0 requests==2.31.0
```

**Desktop `requirements.txt`:**
```txt
PyQt5==5.15.10
matplotlib==3.8.2
Pillow==10.1.0
requests==2.31.0
```

#### Step 3.4: Configure Settings (Optional)

You can customize the backend URL in `desktop_app.py`:

```python
self.base_url = "http://localhost:8000"  
```

#### Step 3.5: Verify Installation

```bash
python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 installed successfully!')"
```

#### Step 3.6: Run Desktop Application

```bash
python main.py
```

✅ PyQt5 desktop application should now launch

---

## ▶️ Running the Application

### Quick Start (After Initial Setup)

You need **3 terminal windows** for full functionality:

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py runserver
```

#### Terminal 2 - Frontend (Web)
```bash
cd frontend
npm start
```

#### Terminal 3 - Desktop App 
```bash
cd desktop
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

## 📖 Usage Guide

### Using the Web Interface (React)

#### 1. Register/Login
- Navigate to http://localhost:3000
- Click "Register" to create an account
- Or "Login" with existing credentials

#### 2. Upload Dataset
- Click "Upload Dataset" button
- Select a CSV file with chemical equipment data
- Click "Upload" and wait for processing
- Status updates automatically every 3 seconds

#### 3. View Results
- Processing status shows: Pending → Processing → Completed
- Once complete, visualizations appear automatically
- View histograms, boxplots, and correlation matrices
- Download PDF report with all statistics and charts

#### 4. Browse History
- Navigate to "History" page
- View your last 5 uploaded datasets
- Click on any dataset to view its visualizations
- Re-download reports as needed

### Using the Desktop App (PyQt5)

#### 1. Login
- Launch the application
- Enter your Django username and password
- Click "Login"
- Use the same credentials as web interface

#### 2. Upload & Process
- Click "Select CSV File" button
- Choose your dataset
- Click "Upload & Process"
- Status updates automatically every 3 seconds
- Progress shows in real-time

#### 3. View Visualizations
- Switch to "Visualizations" tab after processing completes
- Use "Previous" and "Next" buttons to navigate charts
- Charts are high-quality Matplotlib renderings
- Shows current chart position (e.g., "Chart 2 of 5")

#### 4. Download Report
- Return to "Upload Dataset" tab
- Click "Download PDF Report" when status shows "Completed"
- Choose save location
- PDF includes all statistics and visualizations

#### 5. View History
- Switch to "History" tab
- Click "Refresh History" to see latest uploads
- Click "View" on any dataset to load its visualizations

### Sample CSV Format

Your CSV file should contain chemical equipment data:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature,Efficiency
Reactor A,Reactor,150.5,2.5,350,95.2
Pump B,Pump,200.0,3.0,25,87.5
Heat Exchanger C,HeatEx,175.2,2.8,200,92.1
Distillation Column D,Column,125.8,1.5,180,89.3
Compressor E,Compressor,300.5,5.0,50,91.7
```

**Requirements:**
- First row must be headers
- At least 3 numeric columns for meaningful visualizations
- CSV format (.csv extension)
- UTF-8 encoding recommended

---

## 🔌 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123"
}

Response: 201 Created
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

#### Login (Get JWT Token)
```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securePassword123"
}

Response: 200 OK
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Dataset Endpoints

#### Upload Dataset
```http
POST /api/upload-dataset/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <csv_file>

Response: 201 Created
{
  "id": 1,
  "filename": "equipment_data.csv",
  "status": "pending",
  "uploaded_at": "2024-01-15T10:30:00Z"
}
```

#### List Datasets
```http
GET /api/datasets/
Authorization: Bearer <access_token>

Response: 200 OK
[
  {
    "id": 1,
    "filename": "equipment_data.csv",
    "status": "completed",
    "uploaded_at": "2024-01-15T10:30:00Z",
    "processed_at": "2024-01-15T10:30:45Z"
  }
]
```

#### Get Dataset Details
```http
GET /api/datasets/<id>/
Authorization: Bearer <access_token>

Response: 200 OK
{
  "id": 1,
  "filename": "equipment_data.csv",
  "status": "completed",
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed_at": "2024-01-15T10:30:45Z",
  "charts": [
    "/media/charts/1/Flowrate_dist.png",
    "/media/charts/1/Pressure_boxplot.png",
    "/media/charts/1/correlation_matrix.png"
  ],
  "statistics": {
    "row_count": 100,
    "column_count": 6,
    "numeric_columns": ["Flowrate", "Pressure", "Temperature"]
  }
}
```

#### Download PDF Report
```http
GET /api/download-pdf/<id>/
Authorization: Bearer <access_token>

Response: 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="report_1.pdf"

<PDF binary data>
```
## 📁 Project Structure

```
screening_task/
│
├── backend/                    # Django REST API
│   ├── config/                 # Project configuration
│   │   ├── __init__.py
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # URL routing
│   │   ├── wsgi.py             # WSGI config
│   │   └── celery.py           # Celery configuration
│   │
│   ├── api/                    # Main application
│   │   ├── models.py           # Database models
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API views
│   │   ├── urls.py             # API URLs
│   │   ├── tasks.py            # Celery tasks
│   │   └── utils.py            # Helper functions
│   │
│   ├── media/                  # User uploaded content
│   │   ├── uploads/            # CSV files
│   │   ├── charts/             # Generated visualizations
│   │   └── reports/            # PDF reports
│   │
│   ├── manage.py               # Django management
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (dev)
│   └── .env.production         # Environment variables (prod)
│
├── frontend/                   # React web application
│   ├── public/                 # Static files
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── src/                    # Source code
│   │   ├── components/         # React components
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Upload.js
│   │   │   ├── Visualizations.js
│   │   │   └── History.js
│   │   │
│   │   ├── services/           # API services
│   │   │   └── api.js
│   │   │
│   │   ├── App.js              # Main component
│   │   ├── App.css             # Styles
│   │   └── index.js            # Entry point
│   │
│   ├── package.json            # Node dependencies
│   ├── .env.local              # Environment variables (dev)
│   └── .env.production         # Environment variables (prod)
│
├── desktop/                    # PyQt5 desktop application
│   ├── desktop_app.py          # Main application
│   ├── requirements.txt        # Python dependencies
│   └── README.md               # Desktop-specific docs
│
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

---

## 🎨 Application Screenshots

### Web Interface
- Login/Register page with clean UI
- Upload page with drag-and-drop support
- Real-time processing status indicator
- Interactive visualizations with Chart.js
- Responsive design for mobile devices

### Desktop Application
- Native login window
- Three-tab interface (Upload, Visualizations, History)
- High-quality Matplotlib charts
- Auto-polling status updates
- Chart navigation controls



## 📊 Monitoring & Logging

### Setup Logging

**Django settings:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/chemequip/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'api': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```





**Version:** 1.0.0  
**Last Updated:** February 2026  
**Created for:** Internship Screening Task

For the most up-to-date information, check the repository or contact the development team.
