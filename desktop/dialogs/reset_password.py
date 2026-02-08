import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from config import STYLES
from client_utils.api_client import APIClient
from client_utils.helpers import extract_error_message


class ResetPasswordDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api_client = APIClient()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Reset Password")
        self.setGeometry(200, 200, 450, 250)
        self.setWindowModality(Qt.ApplicationModal)
        
        layout = QVBoxLayout()
        
        instructions = QLabel(
            "Reset Your Password\n\n"
            "Enter your username or email to reset your password."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet(STYLES['info_box'])
        layout.addWidget(instructions)
        
        form_layout = QFormLayout()
        
        self.login_id_input = QLineEdit()
        self.login_id_input.setPlaceholderText("Your username or email")
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("At least 8 characters")
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Re-enter new password")
        
        form_layout.addRow("Username/Email:", self.login_id_input)
        form_layout.addRow("New Password:", self.new_password_input)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        
        layout.addLayout(form_layout)
        
        hint = QLabel("Password must be at least 8 characters long")
        hint.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        layout.addWidget(hint)
        
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Reset Password")
        reset_btn.clicked.connect(self.reset_password)
        reset_btn.setStyleSheet(STYLES['success_button'])
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        cancel_btn.setStyleSheet("padding: 10px;")
        
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def reset_password(self):
        login_id = self.login_id_input.text().strip()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not login_id or not new_password:
            QMessageBox.warning(self, "Error", "All fields are required")
            return
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        if len(new_password) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters")
            return
        
        try:
            response = self.api_client.reset_password_request(login_id)
            
            if response.status_code == 200:
                reset_response = self.api_client.reset_password_confirm(
                    login_id, new_password, confirm_password
                )
                
                if reset_response.status_code == 200:
                    QMessageBox.information(
                        self, 
                        "Success", 
                        "Password reset successful!\n\nYou can now login with your new password."
                    )
                    self.close()
                else:
                    error_msg = extract_error_message(reset_response)
                    QMessageBox.warning(self, "Error", f"Password reset failed: {error_msg}")
            else:
                error_msg = extract_error_message(response)
                QMessageBox.warning(self, "Error", str(error_msg))
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self, 
                "Connection Error", 
                "Could not connect to server.\n\nMake sure Django server is running on port 8000"
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")