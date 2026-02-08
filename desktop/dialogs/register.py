import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from config import STYLES
from client_utils.api_client import APIClient
from client_utils.helpers import extract_error_message


class RegisterDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api_client = APIClient()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Register New Account")
        self.setGeometry(150, 150, 450, 400)
        self.setWindowModality(Qt.ApplicationModal)
        
        layout = QVBoxLayout()
        
        instructions = QLabel("Create a new account to get started")
        instructions.setStyleSheet(STYLES['info_box'])
        layout.addWidget(instructions)
        
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your.email@example.com")
        
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First name")
        
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last name")
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("At least 8 characters")
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Re-enter password")
        
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        
        register_btn = QPushButton("Create Account")
        register_btn.clicked.connect(self.register)
        register_btn.setStyleSheet(STYLES['success_button'])
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        cancel_btn.setStyleSheet("padding: 8px;")
        
        button_layout.addWidget(register_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def register(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_password_input.text()
        
        if not all([username, email, first_name, last_name, password]):
            QMessageBox.warning(self, "Error", "All fields are required")
            return
        
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "Error", "Please enter a valid email address")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters")
            return
        
        try:
            response = self.api_client.register(
                username, email, first_name, last_name, password, confirm
            )
            
            if response.status_code == 201:
                data = response.json()
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Registration successful!\n\n"
                    f"Welcome {data['user']['username']}!\n"
                    f"You can now login with your credentials."
                )
                self.close()
            else:
                error_msg = extract_error_message(response)
                QMessageBox.warning(self, "Registration Failed", error_msg)
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self, 
                "Connection Error", 
                "Could not connect to server.\n\nMake sure Django server is running on port 8000"
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")