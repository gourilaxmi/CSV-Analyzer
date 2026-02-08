BASE_URL = "http://localhost:8000/api"
TIMEOUT = 5
POLL_INTERVAL = 3000

ENDPOINTS = {
    'login': '/auth/login/',
    'register': '/auth/register/',
    'logout': '/auth/logout/',
    'change_password': '/auth/change-password/',
    'password_reset_request': '/auth/password-reset-request/',
    'password_reset_confirm': '/auth/password-reset-confirm/',
    'upload_dataset': '/upload-dataset/',
    'datasets': '/datasets/',
    'download_pdf': '/download-pdf/{dataset_id}/',
}

STYLES = {
    'success_button': """
        QPushButton { 
            background-color: #28a745; 
            color: white; 
            padding: 8px; 
            font-weight: bold; 
        }
        QPushButton:hover { background-color: #218838; }
    """,
    'primary_button': """
        QPushButton { 
            background-color: #007bff; 
            color: white; 
            padding: 8px; 
        }
        QPushButton:hover { background-color: #0056b3; }
    """,
    'danger_button': """
        QPushButton { 
            background-color: #dc3545; 
            color: white; 
            padding: 5px 10px; 
        }
        QPushButton:hover { background-color: #c82333; }
    """,
    'link_button': """
        QPushButton { 
            color: #007bff; 
            text-decoration: underline; 
            border: none; 
        }
        QPushButton:hover { color: #0056b3; }
    """,
    'info_box': """
        padding: 15px; 
        background-color: #e3f2fd; 
        border-radius: 5px; 
        font-size: 13px; 
        color: #1976d2;
    """,
    'status_ready': "font-size: 14px; padding: 10px; background-color: #f0f0f0;",
    'status_processing': "font-size: 14px; padding: 10px; background-color: #fff3cd;",
    'status_completed': "font-size: 14px; padding: 10px; background-color: #d4edda;",
    'status_failed': "font-size: 14px; padding: 10px; background-color: #f8d7da;",
}