import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from config import STYLES
from client_utils.api_client import APIClient
from client_utils.helpers import extract_error_message

class ChangePasswordDialog(QWidget):
    def __init__(self, token, parent=None):
        super().__init__(parent)
        self.api_client = APIClient(token)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Change Password")
        self.setGeometry(200, 200, 450, 280)
        self.setWindowModality(Qt.ApplicationModal)
        
        layout = QVBoxLayout()
        
        instructions = QLabel(
            "Change Your Password\n\n"
            "Enter your current password and choose a new one."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet(STYLES['info_box'])
        layout.addWidget(instructions)
        
        form_layout = QFormLayout()
        
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.old_password_input.setPlaceholderText("Current password")
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("At least 8 characters")
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Re-enter new password")
        
        form_layout.addRow("Current Password:", self.old_password_input)
        form_layout.addRow("New Password:", self.new_password_input)
        form_layout.addRow("Confirm New Password:", self.confirm_password_input)
        
        layout.addLayout(form_layout)
        
        hint = QLabel("Password must be at least 8 characters long")
        hint.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        layout.addWidget(hint)
        
        button_layout = QHBoxLayout()
        
        change_btn = QPushButton("Change Password")
        change_btn.clicked.connect(self.change_password)
        change_btn.setStyleSheet(STYLES['success_button'])
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        cancel_btn.setStyleSheet("padding: 10px;")
        
        button_layout.addWidget(change_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def change_password(self):
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not old_password or not new_password:
            QMessageBox.warning(self, "Error", "All fields are required")
            return
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "New passwords do not match")
            return
        
        if len(new_password) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters")
            return
        
        if old_password == new_password:
            QMessageBox.warning(self, "Error", "New password must be different from current password")
            return
        
        try:
            response = self.api_client.change_password(
                old_password, new_password, confirm_password
            )
            
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Password changed successfully!")
                self.close()
            else:
                error_msg = extract_error_message(response)
                QMessageBox.warning(self, "Error", f"Password change failed: {error_msg}")
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self, 
                "Connection Error", 
                "Could not connect to server.\n\nMake sure Django server is running on port 8000"
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")