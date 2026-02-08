import os
import requests
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem,
    QTabWidget, QTextEdit, QApplication
)
from PyQt5.QtCore import QTimer
from config import STYLES, POLL_INTERVAL
from client_utils.api_client import APIClient
from client_utils.helpers import (
    format_timestamp, get_media_path, get_charts_path, 
    load_chart_files, extract_error_message
)
from widgets.chart import Chart
from dialogs.change_password import ChangePasswordDialog
from PyQt5.QtCore import QTimer, Qt


class HomePage(QMainWindow):
    def __init__(self, token, user_data=None, refresh_token=None):
        super().__init__()
        self.token = token
        self.refresh_token = refresh_token
        self.user_data = user_data or {}
        self.api_client = APIClient(token)
        self.current_dataset_id = None
        self.chart_paths = []
        self.current_chart_index = 0
        
        self.media_path = get_media_path()
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        username = self.user_data.get('username', 'User')
        self.setWindowTitle(f"Chemical Equipment Visualizer - {username}")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.create_header())
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_upload_tab(), "Upload Dataset")
        self.tabs.addTab(self.create_visualization_tab(), "Visualizations")
        self.tabs.addTab(self.create_history_tab(), "History")
        
        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)
        
        QTimer.singleShot(500, lambda: self.log(f"Media path: {self.media_path}"))
    
    def create_header(self):
        header_layout = QHBoxLayout()
        
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        user_label = QLabel(f"Logged in as: {self.user_data.get('username', 'User')}")
        user_label.setStyleSheet("padding: 10px; font-size: 12px;")
        header_layout.addWidget(user_label)
        
        change_password_btn = QPushButton("Change Password")
        change_password_btn.clicked.connect(self.show_change_password)
        change_password_btn.setStyleSheet("padding: 5px 10px;")
        header_layout.addWidget(change_password_btn)
        
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet(STYLES['danger_button'])
        header_layout.addWidget(logout_btn)
        
        return header_layout
    
    def create_upload_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        upload_section = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.select_btn = QPushButton("Select CSV File")
        self.select_btn.clicked.connect(self.select_file)
        self.upload_btn = QPushButton("Upload & Process")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        
        upload_section.addWidget(self.file_label)
        upload_section.addWidget(self.select_btn)
        upload_section.addWidget(self.upload_btn)
        layout.addLayout(upload_section)
        
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet(STYLES['status_ready'])
        layout.addWidget(self.status_label)
        
        self.download_btn = QPushButton("Download PDF Report")
        self.download_btn.clicked.connect(self.download_pdf)
        self.download_btn.setEnabled(False)
        layout.addWidget(self.download_btn)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        layout.addWidget(QLabel("Activity Log:"))
        layout.addWidget(self.log_text)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_visualization_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("← Previous Chart")
        self.prev_btn.clicked.connect(self.show_previous_chart)
        self.next_btn = QPushButton("Next Chart →")
        self.next_btn.clicked.connect(self.show_next_chart)
        
        self.chart_info_label = QLabel("No charts loaded")
        self.chart_info_label.setAlignment(Qt.AlignCenter)
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.chart_info_label)
        nav_layout.addWidget(self.next_btn)
        layout.addLayout(nav_layout)
        
        self.chart_canvas = Chart(self)
        layout.addWidget(self.chart_canvas)
        
        self.prev_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        
        widget.setLayout(layout)
        return widget
    
    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.clicked.connect(self.load_datasets)
        layout.addWidget(refresh_btn)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["ID", "Status", "Uploaded At", "Actions"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.history_table)
        
        widget.setLayout(layout)
        return widget
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.upload_btn.setEnabled(True)
            self.log(f"Selected file: {os.path.basename(file_path)}")
    
    def upload_file(self):
        if not hasattr(self, 'selected_file'):
            return
        
        try:
            response = self.api_client.upload_dataset(self.selected_file)
            
            if response.status_code == 202:
                data = response.json()
                self.current_dataset_id = data.get('dataset_id')
                self.log(f"Upload successful! Dataset ID: {self.current_dataset_id}")
                self.log(data.get('message', 'Processing started'))
                self.status_label.setText("Status: Processing...")
                self.status_label.setStyleSheet(STYLES['status_processing'])
                self.start_status_polling()
            else:
                error_msg = extract_error_message(response)
                self.log(f"Upload failed: {error_msg}")
                QMessageBox.warning(self, "Error", f"Upload failed: {error_msg}")
        
        except Exception as e:
            self.log(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Upload error: {str(e)}")
    
    def start_status_polling(self):
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.check_status)
        self.poll_timer.start(POLL_INTERVAL)
    
    def check_status(self):
        if not self.current_dataset_id:
            return
        
        try:
            response = self.api_client.get_datasets()
            
            if response.status_code == 200:
                datasets = response.json()
                current = next((d for d in datasets if d['id'] == self.current_dataset_id), None)
                
                if current:
                    status = current['status']
                    self.status_label.setText(f"Status: {status.capitalize()}")
                    
                    if status == 'completed':
                        self.status_label.setStyleSheet(STYLES['status_completed'])
                        self.log("Processing completed! PDF ready for download.")
                        self.download_btn.setEnabled(True)
                        self.poll_timer.stop()
                        self.load_charts()
                    
                    elif status == 'failed':
                        self.status_label.setStyleSheet(STYLES['status_failed'])
                        error_msg = current.get('error_message', 'Unknown error')
                        self.log(f"Processing failed: {error_msg}")
                        QMessageBox.warning(self, "Processing Failed", error_msg)
                        self.poll_timer.stop()
        
        except Exception as e:
            self.log(f"Status check error: {str(e)}")
    
    def load_charts(self):
        if not self.current_dataset_id:
            return
        
        charts_dir = get_charts_path(self.media_path, self.current_dataset_id)
        self.log(f"Looking for charts in: {charts_dir}")
        
        self.chart_paths = load_chart_files(charts_dir)
        
        if self.chart_paths:
            self.current_chart_index = 0
            self.show_chart(0)
            self.update_chart_navigation()
            self.log(f"Loaded {len(self.chart_paths)} charts")
        else:
            self.log(f"No charts found in {charts_dir}")
    
    def show_chart(self, index):
        if 0 <= index < len(self.chart_paths):
            self.chart_canvas.plot_image(self.chart_paths[index])
            self.chart_info_label.setText(
                f"Chart {index + 1} of {len(self.chart_paths)}: "
                f"{os.path.basename(self.chart_paths[index])}"
            )
    
    def show_previous_chart(self):
        if self.current_chart_index > 0:
            self.current_chart_index -= 1
            self.show_chart(self.current_chart_index)
            self.update_chart_navigation()
    
    def show_next_chart(self):
        if self.current_chart_index < len(self.chart_paths) - 1:
            self.current_chart_index += 1
            self.show_chart(self.current_chart_index)
            self.update_chart_navigation()
    
    def update_chart_navigation(self):
        self.prev_btn.setEnabled(self.current_chart_index > 0)
        self.next_btn.setEnabled(self.current_chart_index < len(self.chart_paths) - 1)
    
    def download_pdf(self):
        if not self.current_dataset_id:
            return
        
        try:
            response = self.api_client.download_pdf(self.current_dataset_id)
            
            if response.status_code == 200:
                save_path, _ = QFileDialog.getSaveFileName(
                    self, 
                    "Save PDF Report", 
                    f"report_{self.current_dataset_id}.pdf", 
                    "PDF Files (*.pdf)"
                )
                
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    self.log(f"PDF saved to: {save_path}")
                    QMessageBox.information(self, "Success", "PDF report downloaded successfully!")
            else:
                error_msg = extract_error_message(response)
                QMessageBox.warning(self, "Error", error_msg)
        
        except Exception as e:
            self.log(f"Download error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Download error: {str(e)}")
    
    def load_datasets(self):
        try:
            response = self.api_client.get_datasets()
            
            if response.status_code == 200:
                datasets = response.json()
                self.history_table.setRowCount(len(datasets))
                
                for row, dataset in enumerate(datasets):
                    self.history_table.setItem(row, 0, QTableWidgetItem(str(dataset['id'])))
                    self.history_table.setItem(row, 1, QTableWidgetItem(dataset['status']))
                    self.history_table.setItem(row, 2, QTableWidgetItem(dataset['uploaded_at']))
                    
                    view_btn = QPushButton("View")
                    view_btn.clicked.connect(lambda checked, d_id=dataset['id']: self.view_dataset(d_id))
                    self.history_table.setCellWidget(row, 3, view_btn)
                
                self.log(f"Loaded {len(datasets)} datasets from history")
            else:
                self.log(f"Failed to load datasets: {response.text}")
        
        except Exception as e:
            self.log(f"Error loading history: {str(e)}")
    
    def view_dataset(self, dataset_id):
        self.current_dataset_id = dataset_id
        self.status_label.setText(f"Viewing Dataset ID: {dataset_id}")
        self.download_btn.setEnabled(True)
        self.load_charts()
        self.tabs.setCurrentIndex(1)
    
    def show_change_password(self):
        dialog = ChangePasswordDialog(self.token, self)
        dialog.show()
    
    def logout(self):
        reply = QMessageBox.question(
            self, 
            'Logout', 
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if self.refresh_token:
                    self.api_client.logout(self.refresh_token)
            except:
                pass
            
            self.close()
            QApplication.quit()
    
    def log(self, message):
        timestamp = format_timestamp()
        self.log_text.append(f"[{timestamp}] {message}")
