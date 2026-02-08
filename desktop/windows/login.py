import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from config import STYLES
from client_utils.api_client import APIClient
from client_utils.helpers import extract_error_message
from dialogs.reset_password import ResetPasswordDialog
from dialogs.register import RegisterDialog


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None
        self.refresh_token = None
        self.user_data = None
        self.api_client = APIClient()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Login - Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 400, 250)
        
        layout = QVBoxLayout()
        
        title = QLabel("Chemical Equipment Visualizer")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or Email")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.returnPressed.connect(self.login)
        
        form_layout.addRow("Username/Email:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        
        layout.addLayout(form_layout)
        
        forgot_link_layout = QHBoxLayout()
        forgot_link_layout.addStretch()
        
        forgot_password_btn = QPushButton("Forgot/Reset Password?")
        forgot_password_btn.setFlat(True)
        forgot_password_btn.setCursor(Qt.PointingHandCursor)
        forgot_password_btn.setStyleSheet(STYLES['link_button'])
        forgot_password_btn.clicked.connect(self.show_reset_password)
        
        forgot_link_layout.addWidget(forgot_password_btn)
        layout.addLayout(forgot_link_layout)
        
        button_layout = QHBoxLayout()
        
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        login_btn.setStyleSheet(STYLES['success_button'])
        
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.show_register)
        register_btn.setStyleSheet(STYLES['primary_button'])
        
        button_layout.addWidget(login_btn)
        button_layout.addWidget(register_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def login(self):
        login_id = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not login_id or not password:
            QMessageBox.warning(self, "Error", "Please enter username/email and password")
            return
        
        try:
            response = self.api_client.login(login_id, password)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['tokens']['access']
                self.refresh_token = data['tokens']['refresh']
                self.user_data = data.get('user', {})
                
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Welcome {self.user_data.get('username', 'User')}!"
                )
                self.close()
            else:
                error_msg = extract_error_message(response)
                QMessageBox.warning(self, "Login Failed", error_msg)
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self, 
                "Connection Error", 
                "Could not connect to server.\n\n"
                "Make sure Django server is running on port 8000:\n"
                "python manage.py runserver"
            )
        except requests.exceptions.Timeout:
            QMessageBox.critical(self, "Timeout", "Connection timed out. Please try again.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def show_reset_password(self):
        dialog = ResetPasswordDialog(self)
        dialog.show()
    
    def show_register(self):
        dialog = RegisterDialog(self)
        dialog.show()
