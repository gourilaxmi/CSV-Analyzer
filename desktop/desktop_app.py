import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QTabWidget, QTextEdit, QLineEdit, QFormLayout
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PIL import Image
import io


class LoginWindow(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Login - Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)
        
        button_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login)
        
        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.show_register)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.register_btn)
        
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        try:
            response = requests.post(
                "http://localhost:8000/api/auth/token/",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access')
                self.refresh_token = data.get('refresh')
                QMessageBox.information(self, "Success", "Login successful!")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid credentials")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {str(e)}\nMake sure Django server is running on port 8000")
    
    def show_register(self):
        QMessageBox.information(self, "Register", "Please register using the web interface or API")


class ChartCanvas(FigureCanvas):
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(8, 6))
        super().__init__(self.fig)
        self.setParent(parent)
    
    def plot_image(self, image_path):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        try:
            img = Image.open(image_path)
            ax.imshow(img)
            ax.axis('off')
            self.draw()
        except Exception as e:
            ax.text(0.5, 0.5, f'Error loading image:\n{str(e)}', 
                   ha='center', va='center', transform=ax.transAxes)
            self.draw()


class MainWindow(QMainWindow):
    
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
        self.base_url = "http://localhost:8000/api"
        self.current_dataset_id = None
        self.chart_paths = []
        
        self.setup_paths()
        
        self.init_ui()
        self.load_datasets()
    
    def setup_paths(self):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        if os.path.basename(current_dir) == 'desktop':
            project_root = os.path.dirname(current_dir)
            self.media_path = os.path.join(project_root, "backend", "media")
        else:

            if os.path.exists(os.path.join(current_dir, "backend", "media")):
                self.media_path = os.path.join(current_dir, "backend", "media")

            elif os.path.exists(os.path.join(current_dir, "media")):
                self.media_path = os.path.join(current_dir, "media")
            else:
                self.media_path = os.path.join(current_dir, "backend", "media")
        
        self.log_message = f"Media path set to: {self.media_path}"
    
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        self.tabs = QTabWidget()
        
        upload_tab = self.create_upload_tab()
        self.tabs.addTab(upload_tab, "Upload Dataset")
        
        viz_tab = self.create_visualization_tab()
        self.tabs.addTab(viz_tab, "Visualizations")
        
        history_tab = self.create_history_tab()
        self.tabs.addTab(history_tab, "History")
        
        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)
        
        QTimer.singleShot(500, lambda: self.log(self.log_message))
    
    def create_upload_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Upload section
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
        self.status_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #f0f0f0;")
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
        
        self.chart_canvas = ChartCanvas(self)
        layout.addWidget(self.chart_canvas)
        
        self.prev_btn.setEnabled(False)
        self.next_btn.setEnabled(False)
        self.current_chart_index = 0
        
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
        """Upload CSV file to backend"""
        if not hasattr(self, 'selected_file'):
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'dataset_file': f}
                response = requests.post(
                    f"{self.base_url}/upload-dataset/",
                    files=files,
                    headers=self.headers
                )
            
            if response.status_code == 202:
                data = response.json()
                self.current_dataset_id = data.get('dataset_id')
                self.log(f"Upload successful! Dataset ID: {self.current_dataset_id}")
                self.log(data.get('message', 'Processing started'))
                self.status_label.setText("Status: Processing...")
                self.status_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #fff3cd;")
                
                self.start_status_polling()
            else:
                self.log(f"Upload failed: {response.text}")
                QMessageBox.warning(self, "Error", f"Upload failed: {response.text}")
        
        except Exception as e:
            self.log(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Upload error: {str(e)}")
    
    def start_status_polling(self):
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.check_status)
        self.poll_timer.start(3000)  
    
    def check_status(self):
        if not self.current_dataset_id:
            return
        
        try:
            response = requests.get(
                f"{self.base_url}/datasets/",
                headers=self.headers
            )
            
            if response.status_code == 200:
                datasets = response.json()
                current = next((d for d in datasets if d['id'] == self.current_dataset_id), None)
                
                if current:
                    status = current['status']
                    self.status_label.setText(f"Status: {status.capitalize()}")
                    
                    if status == 'completed':
                        self.status_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #d4edda;")
                        self.log("Processing completed! PDF ready for download.")
                        self.download_btn.setEnabled(True)
                        self.poll_timer.stop()
                        
                        self.load_charts()
                    
                    elif status == 'failed':
                        self.status_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #f8d7da;")
                        error_msg = current.get('error_message', 'Unknown error')
                        self.log(f"Processing failed: {error_msg}")
                        self.poll_timer.stop()
        
        except Exception as e:
            self.log(f"Status check error: {str(e)}")
    
    def load_charts(self):
        if not self.current_dataset_id:
            return
        
        charts_dir = os.path.join(self.media_path, "charts", str(self.current_dataset_id))
        
        self.log(f"Looking for charts in: {charts_dir}")
        
        if os.path.exists(charts_dir):
            all_files = os.listdir(charts_dir)
            self.chart_paths = [
                os.path.join(charts_dir, f) 
                for f in all_files
                if f.endswith('.png')
            ]
            
            if self.chart_paths:
                self.current_chart_index = 0
                self.show_chart(0)
                self.update_chart_navigation()
                self.log(f"Loaded {len(self.chart_paths)} charts")
            else:
                self.log(f"No PNG charts found in {charts_dir}")
                self.log(f"Files found: {all_files}")
        else:
            self.log(f"Charts directory not found: {charts_dir}")
            self.log("Make sure the backend has finished processing the dataset.")
    
    def show_chart(self, index):
        if 0 <= index < len(self.chart_paths):
            self.chart_canvas.plot_image(self.chart_paths[index])
            self.chart_info_label.setText(
                f"Chart {index + 1} of {len(self.chart_paths)}: {os.path.basename(self.chart_paths[index])}"
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
            response = requests.get(
                f"{self.base_url}/download-pdf/{self.current_dataset_id}/",
                headers=self.headers
            )
            
            if response.status_code == 200:
                # Save file
                save_path, _ = QFileDialog.getSaveFileName(
                    self, "Save PDF Report", f"report_{self.current_dataset_id}.pdf", "PDF Files (*.pdf)"
                )
                
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    self.log(f"PDF saved to: {save_path}")
                    QMessageBox.information(self, "Success", "PDF report downloaded successfully!")
            else:
                error_data = response.json()
                QMessageBox.warning(self, "Error", error_data.get('error', 'Download failed'))
        
        except Exception as e:
            self.log(f"Download error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Download error: {str(e)}")
    
    def load_datasets(self):
        try:
            response = requests.get(
                f"{self.base_url}/datasets/",
                headers=self.headers
            )
            
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
        
        except Exception as e:
            self.log(f"Error loading history: {str(e)}")
    
    def view_dataset(self, dataset_id):
        self.current_dataset_id = dataset_id
        self.status_label.setText(f"Viewing Dataset ID: {dataset_id}")
        self.load_charts()
        self.tabs.setCurrentIndex(1)  
    
    def log(self, message):
        self.log_text.append(f"[{self.get_timestamp()}] {message}")
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")


def main():
    app = QApplication(sys.argv)
    
    login_window = LoginWindow()
    login_window.show()
    
    app.exec_()
    
    if login_window.token:
        main_window = MainWindow(login_window.token)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()