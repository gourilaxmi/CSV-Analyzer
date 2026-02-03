# Chemical Equipment Data Visualizer

A full-stack application for uploading, processing, and visualizing chemical equipment data with **Django REST API backend**, **React web frontend**, and **PyQt5 desktop application**.

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd screening_task
```

---

### 2. Backend Setup (Django)

#### Step 2.1: Create Virtual Environment

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

#### Step 2.2: Install Dependencies

```bash
pip install -r requirements.txt
```

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

#### Step 2.4: Create Media Directories

```bash
# Windows
mkdir media\uploads media\charts media\reports

# macOS/Linux
mkdir -p media/uploads media/charts media/reports
```

#### Step 2.5: Run Development Server

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


