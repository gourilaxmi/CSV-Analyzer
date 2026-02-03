# Chemical Equipment Visualizer - PyQt5 Desktop Application

A desktop application built with PyQt5 that connects to the Django backend to upload CSV files, process chemical equipment data, and display visualizations.

## Features

- **User Authentication**: Login using Django JWT tokens
- **CSV Upload**: Select and upload CSV files containing chemical equipment data
- **Real-time Status**: Monitor processing status with auto-refresh
- **Visualizations**: View generated charts (histograms, boxplots, correlation matrix)
- **PDF Download**: Download comprehensive PDF reports
- **History**: View last 5 uploaded datasets

## Prerequisites

- Python 3.8 or higher
- Django backend running on `http://localhost:8000`
- Pip package manager

## Installation Steps

### Step 1: Install PyQt5 and Dependencies

Open your terminal/command prompt and run:

```bash
pip install PyQt5==5.15.10 matplotlib==3.8.2 Pillow==10.1.0 requests==2.31.0
```

Or use the requirements file:

```bash
pip install -r requirements_pyqt5.txt
```

### Step 2: Verify Installation

Test if PyQt5 is installed correctly:

```bash
python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 installed successfully!')"
```

### Step 3: Ensure Django Backend is Running

Before starting the PyQt5 app, make sure your Django backend is running:

```bash
# Navigate to your Django project directory
cd backend/

# Run migrations (first time only)
python manage.py makemigrations
python manage.py migrate

# Create a superuser (first time only)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

The backend should be accessible at `http://localhost:8000`

### Step 4: Run the PyQt5 Application

```bash
python pyqt5_app.py
```

## How to Use

### 1. Login
- When the app starts, you'll see a login window
- Enter your Django username and password
- Click "Login"
- If you don't have an account, register using the web interface first

### 2. Upload Dataset
- Click "Select CSV File" button
- Choose your CSV file (must be .csv format)
- Click "Upload & Process"
- The app will automatically check the processing status every 3 seconds

### 3. View Visualizations
- Once processing is complete, switch to the "Visualizations" tab
- Use "Previous" and "Next" buttons to navigate through charts
- Charts include:
  - Histograms for numeric columns
  - Boxplots showing outlier distributions
  - Correlation matrix

### 4. Download PDF Report
- On the "Upload Dataset" tab, click "Download PDF Report" when ready
- Choose where to save the PDF file
- The PDF contains all statistics and visualizations

### 5. View History
- Switch to "History" tab
- Click "Refresh History" to see your last 5 uploads
- Click "View" on any dataset to see its visualizations

## Application Structure

```
pyqt5_app.py
├── LoginWindow        # Handles authentication
├── MainWindow         # Main application window
│   ├── Upload Tab     # CSV upload and status monitoring
│   ├── Viz Tab        # Chart visualization with navigation
│   └── History Tab    # Recent datasets list
├── ChartCanvas        # Matplotlib chart display widget
└── Helper Methods     # API calls, file handling, etc.
```

## API Endpoints Used

The PyQt5 app interacts with these Django endpoints:

- `POST /api/auth/token/` - Login and get JWT token
- `POST /api/upload-dataset/` - Upload CSV file
- `GET /api/datasets/` - Get list of recent datasets
- `GET /api/download-pdf/{id}/` - Download PDF report

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'PyQt5'"

**Solution**: Install PyQt5
```bash
pip install PyQt5
```

### Issue: "Connection refused" or "Connection error"

**Solution**: Make sure Django backend is running
```bash
python manage.py runserver
```

### Issue: Charts not loading

**Solution**: The app looks for charts in `media/charts/{dataset_id}/`. Make sure:
1. Django backend has completed processing
2. The media directory exists and has correct permissions
3. You're running the PyQt5 app from the same directory as the Django project

### Issue: Login fails

**Solution**: 
1. Verify your username/password
2. Make sure you've created a user in Django (use `python manage.py createsuperuser`)
3. Check that the Django server is accessible at `http://localhost:8000`

### Issue: PDF download shows "Report not ready"

**Solution**: Wait for processing to complete. The status should show "Completed" before you can download the PDF.

## Sample CSV Format

Your CSV file should have these columns (or similar):
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor A,Reactor,150.5,2.5,350
Pump B,Pump,200.0,3.0,25
...
```

## Directory Structure for Charts

When a dataset is processed, charts are saved in:
```
media/
└── charts/
    └── {dataset_id}/
        ├── Flowrate_dist.png
        ├── Pressure_dist.png
        ├── Temperature_dist.png
        ├── Flowrate_boxplot.png
        └── correlation_matrix.png
```

## Key Features Explained

### Auto-Polling
The app automatically checks processing status every 3 seconds and updates the UI when complete.

### Chart Navigation
- Displays one chart at a time (better for detailed viewing)
- Shows chart filename and position (e.g., "Chart 2 of 5")
- Previous/Next buttons automatically enable/disable

### Error Handling
- Connection errors show helpful messages
- Invalid credentials alert the user
- File size/type validation on backend

## Development Notes

### Customization

You can customize the app by modifying:

1. **Polling Interval**: Change `3000` in `self.poll_timer.start(3000)` (line ~234)
2. **Backend URL**: Change `http://localhost:8000` in `self.base_url` (line ~164)
3. **Chart Size**: Modify `figsize=(8, 6)` in ChartCanvas (line ~77)
4. **Window Size**: Change `setGeometry(100, 100, 1200, 800)` (line ~158)

### Adding Features

To add new features:
1. Add a new tab in `create_*_tab()` methods
2. Create corresponding API endpoints in Django
3. Add methods to handle the new functionality

## Comparison: PyQt5 vs Web Frontend

| Feature | PyQt5 Desktop | React Web |
|---------|---------------|-----------|
| Installation | Requires Python + packages | Just needs browser |
| Performance | Native, faster | Depends on browser |
| Charts | Matplotlib (desktop-quality) | Chart.js (web-optimized) |
| Offline | Works offline (after auth) | Needs internet |
| Updates | Manual update needed | Auto-updates |

## License

This project is for educational purposes as part of an internship screening task.

## Support

For issues with:
- **Django Backend**: Check Django console logs
- **PyQt5 App**: Check terminal output where you ran `python pyqt5_app.py`
- **Authentication**: Verify credentials in Django admin panel

## Future Enhancements

Possible improvements:
- [ ] Add data table view in PyQt5
- [ ] Export individual charts as images
- [ ] Add dark mode theme
- [ ] Remember login credentials (securely)
- [ ] Add dataset comparison feature
- [ ] Real-time preview of CSV before upload
