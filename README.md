# Chemical Equipment Data Visualizer

A full-stack application for uploading, processing, and visualizing chemical equipment data with Django REST API backend, React web frontend, and PyQt5 desktop application.


##  Installation & Setup

### 1. Clone the Repository

git clone <repository-url>
cd screening_task
\

### 2. Backend Setup (Django)

#### Step 2.1: Create Virtual Environment

Windows:

cd backend
python -m venv venv
venv\Scripts\activate


macOS/Linux:

cd backend
python3 -m venv venv
source venv/bin/activate


#### Step 2.2: Install Dependencies

pip install -r requirements.txt


**Backend `requirements.txt` includes:**
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

#### Step 2.3: Configure Database

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 2.4: Create Superuser

```bash
python manage.py createsuperuser
```

Follow prompts to set username, email, and password.

#### Step 2.5: Create Media Directories

```bash
# Windows
mkdir media\uploads media\charts media\reports

# macOS/Linux
mkdir -p media/uploads media/charts media/reports
```

#### Step 2.6: Run Development Server

```bash
python manage.py runserver
```

✅ Backend should now be running at: **http://localhost:8000**

---

### 3. Frontend Setup (React)

Open a **new terminal** (keep backend running):

#### Step 3.1: Navigate to Frontend

```bash
cd frontend
```

#### Step 3.2: Install Dependencies

```bash
npm install
```

**Frontend dependencies include:**
- react, react-dom, react-router-dom
- axios
- chart.js, react-chartjs-2

#### Step 3.3: Configure Environment

Create `.env.local` file in `frontend/` directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

#### Step 3.4: Run Development Server

```bash
npm start
```

✅ Frontend should now be running at: **http://localhost:3000**

Your browser should automatically open. If not, navigate to http://localhost:3000

---

### 4. Desktop App Setup (PyQt5)

Open a **new terminal**:

#### Step 4.1: Navigate to Desktop Directory

```bash
cd desktop
```

#### Step 4.2: Create Virtual Environment (Optional but Recommended)

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

#### Step 4.3: Install Dependencies

**Option A - Manual Installation:**
```bash
pip install PyQt5==5.15.10 matplotlib==3.8.2 Pillow==10.1.0 requests==2.31.0
```

**Option B - Using Requirements File:**
```bash
pip install -r requirements.txt
```

**Option C - Automated Setup Scripts:**

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

#### Step 4.4: Verify Installation

```bash
python test_installation.py
```

This will check if all dependencies are correctly installed and if the backend is accessible.

#### Step 4.5: Run Desktop Application

```bash
python desktop_app.py
```

✅ PyQt5 desktop application should now launch

---

## ▶️ Running the Application

### Quick Start (After Initial Setup)

You need **3 terminal windows**:

#### Terminal 1 - Backend
```bash
cd backend
# Activate venv if using one
python manage.py runserver
```

#### Terminal 2 - React Frontend
```bash
cd frontend
npm start
```

#### Terminal 3 - Desktop App (Optional)
```bash
cd desktop
# Activate venv if using one
python desktop_app.py
```

---

## 📖 Usage Guide

### Using the Web Interface (React)

1. **Register/Login**
   - Navigate to http://localhost:3000
   - Click "Register" to create an account or "Login" with existing credentials
   - Use the superuser credentials you created during backend setup

2. **Upload Dataset**
   - Click "Upload Dataset" or navigate to upload page
   - Select a CSV file with chemical equipment data
   - Click "Upload" and wait for processing

3. **View Results**
   - Processing status updates automatically
   - Once complete, view generated visualizations
   - Download PDF report with all statistics and charts

4. **Browse History**
   - View previously uploaded datasets
   - Access their visualizations and reports

### Using the Desktop App (PyQt5)

1. **Login**
   - Launch the application
   - Enter your Django credentials
   - Click "Login"

2. **Upload & Process**
   - Click "Select CSV File"
   - Choose your dataset
   - Click "Upload & Process"
   - Status updates automatically every 3 seconds

3. **View Visualizations**
   - Switch to "Visualizations" tab after processing completes
   - Use "Previous" and "Next" buttons to navigate charts
   - Charts are rendered locally for high quality

4. **Download Report**
   - Click "Download PDF Report" when ready
   - Choose save location
   - PDF includes all statistics and visualizations

### Sample CSV Format

Your CSV should contain chemical equipment data. Example structure:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature,Efficiency
Reactor A,Reactor,150.5,2.5,350.0,95.2
Pump B,Pump,200.0,3.0,25.0,87.5
Heat Exchanger C,HeatExchanger,175.5,2.8,280.0,92.1
Compressor D,Compressor,220.0,5.0,45.0,89.3
```

**Requirements:**
- First row must contain column headers
- Include numeric columns for analysis
- CSV format (comma-separated)
- Max file size: 20MB

---

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/token/` - Login (get JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token

### Dataset Operations
- `POST /api/upload-dataset/` - Upload and process CSV
- `GET /api/datasets/` - List recent datasets
- `GET /api/datasets/{id}/` - Get specific dataset details
- `GET /api/datasets/{id}/status/` - Check processing status
- `GET /api/download-pdf/{id}/` - Download PDF report

### Example API Usage

```bash
# Login
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'

# Upload dataset (with auth token)
curl -X POST http://localhost:8000/api/upload-dataset/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@dataset.csv" \
  -F "name=Chemical Equipment Data"
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem: `ModuleNotFoundError` when running Django**
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

**Problem: `django.db.utils.OperationalError: no such table`**
```bash
# Solution: Run migrations
python manage.py makemigrations
python manage.py migrate
```

**Problem: Port 8000 already in use**
```bash
# Solution: Run on different port
python manage.py runserver 8080
# Update REACT_APP_API_URL in frontend/.env.local accordingly
```

### Frontend Issues

**Problem: `npm: command not found`**
```bash
# Solution: Install Node.js from https://nodejs.org/
```

**Problem: CORS errors in browser console**
```bash
# Solution: Check backend settings.py has:
# CORS_ALLOW_ALL_ORIGINS = True  # For development
```

**Problem: Can't connect to backend**
```bash
# Solution: Verify backend is running at http://localhost:8000
# Check .env.local has correct REACT_APP_API_URL
```

### Desktop App Issues

**Problem: `ModuleNotFoundError: No module named 'PyQt5'`**
```bash
# Solution: Install PyQt5
pip install PyQt5==5.15.10
```

**Problem: Charts not loading**
```bash
# Solution: 
# 1. Ensure backend completed processing (status = "Completed")
# 2. Check media/charts/{dataset_id}/ directory exists
# 3. Verify file permissions on media directory
```

**Problem: "Connection refused" error**
```bash
# Solution: Start Django backend first
cd backend
python manage.py runserver
```

### Common Issues

**Problem: Cannot login with created superuser**
```bash
# Solution: Create user via Django admin or API registration endpoint
# Superuser is for admin panel, regular users need to register via API
```

**Problem: Uploaded file not processing**
```bash
# Solution: 
# 1. Check CSV format is correct (comma-separated, headers in first row)
# 2. File size must be under 20MB
# 3. Check Django logs for specific error messages
```

---

## 🌟 Project Features

### Data Processing Pipeline
1. **Upload**: CSV file uploaded via API
2. **Validation**: File format and size validation
3. **Analysis**: Statistical analysis using pandas
4. **Visualization**: Charts generated with matplotlib
5. **Report**: PDF report created with reportlab
6. **Storage**: Files and metadata stored in database

### Security Features
- JWT token authentication
- Password hashing
- File type validation
- Size limit enforcement
- CSRF protection
- CORS configuration

### Visualization Types
1. **Histograms**: Distribution of numeric values
2. **Box Plots**: Outlier detection and quartile analysis
3. **Correlation Matrix**: Relationships between variables

---

## 📝 Development Notes

### Adding New Features

**Backend:**
- Add new endpoints in `backend/api/views.py`
- Update URLs in `backend/api/urls.py`
- Create models in `backend/api/models.py`

**React Frontend:**
- Add components in `frontend/src/components/`
- Add pages in `frontend/src/pages/`
- Update routes in `frontend/src/App.js`

**Desktop App:**
- Modify `desktop/desktop_app.py`
- Add new tabs or features in MainWindow class

### Testing

```bash
# Backend
cd backend
python manage.py test

# Frontend
cd frontend
npm test

# Desktop app
cd desktop
python test_installation.py
```

---

## 📜 License

This project is for educational/internship screening purposes.

---

## 🤝 Contributing

This is a screening task project. For feedback or questions, please contact the project maintainer.

---

## 📞 Support

If you encounter issues during setup:

1. Check the [Troubleshooting](#troubleshooting) section
2. Verify all [Prerequisites](#prerequisites) are installed
3. Ensure all three components (backend, frontend, desktop) are properly configured
4. Check terminal/console logs for specific error messages

---

## ✅ Setup Verification Checklist

Use this checklist to ensure everything is set up correctly:

- [ ] Python 3.8+ installed
- [ ] Node.js and npm installed
- [ ] Backend virtual environment created and activated
- [ ] Backend dependencies installed
- [ ] Database migrations completed
- [ ] Superuser created
- [ ] Backend running on port 8000
- [ ] Frontend dependencies installed
- [ ] Frontend .env.local configured
- [ ] Frontend running on port 3000
- [ ] Desktop app dependencies installed
- [ ] Desktop app can connect to backend
- [ ] Can login via web interface
- [ ] Can upload CSV and see processing
- [ ] Can view visualizations
- [ ] Can download PDF report

---

**Happy Coding! 🚀**
