@echo off
REM Quick Setup Script for PyQt5 Desktop Application (Windows)
REM Run this script to set up everything automatically

echo ==================================
echo PyQt5 Desktop App - Quick Setup
echo ==================================

REM Step 1: Install Python dependencies
echo.
echo Step 1: Installing Python packages...
pip install PyQt5==5.15.10 matplotlib==3.8.2 Pillow==10.1.0 requests==2.31.0

REM Step 2: Verify installation
echo.
echo Step 2: Verifying PyQt5 installation...
python -c "from PyQt5.QtWidgets import QApplication; print('✓ PyQt5 installed successfully!')"
if errorlevel 1 (
    echo ✗ PyQt5 installation failed!
    pause
    exit /b 1
)

python -c "import matplotlib; print('✓ Matplotlib installed successfully!')"
if errorlevel 1 (
    echo ✗ Matplotlib installation failed!
    pause
    exit /b 1
)

echo.
echo ==================================
echo Setup completed successfully!
echo ==================================
echo.
echo Next steps:
echo 1. Make sure Django backend is running:
echo    cd backend/
echo    python manage.py runserver
echo.
echo 2. Run the PyQt5 application:
echo    python pyqt5_app.py
echo.
echo ==================================
pause
