import requests
from config import BASE_URL, TIMEOUT, ENDPOINTS


class APIClient:
    def __init__(self, token=None):
        self.token = token
        self.base_url = BASE_URL
        
    @property
    def headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    def _build_url(self, endpoint_key, **kwargs):
        endpoint = ENDPOINTS[endpoint_key]
        if kwargs:
            endpoint = endpoint.format(**kwargs)
        return f"{self.base_url}{endpoint}"
    
    def login(self, login_id, password):
        url = self._build_url('login')
        response = requests.post(url, json={
            "login_id": login_id,
            "password": password
        }, timeout=TIMEOUT)
        return response
    
    def register(self, username, email, first_name, last_name, password, password2):
        url = self._build_url('register')
        response = requests.post(url, json={
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "password2": password2
        }, timeout=TIMEOUT)
        return response
    
    def logout(self, refresh_token):
        url = self._build_url('logout')
        response = requests.post(url, json={
            "refresh": refresh_token
        }, headers=self.headers, timeout=TIMEOUT)
        return response
    
    def change_password(self, old_password, new_password, new_password2):
        url = self._build_url('change_password')
        response = requests.post(url, json={
            "old_password": old_password,
            "new_password": new_password,
            "new_password2": new_password2
        }, headers=self.headers, timeout=TIMEOUT)
        return response
    
    def reset_password_request(self, login_id):
        url = self._build_url('password_reset_request')
        response = requests.post(url, json={
            "login_id": login_id
        }, timeout=TIMEOUT)
        return response
    
    def reset_password_confirm(self, login_id, new_password, new_password2):
        url = self._build_url('password_reset_confirm')
        response = requests.post(url, json={
            "login_id": login_id,
            "new_password": new_password,
            "new_password2": new_password2
        }, timeout=TIMEOUT)
        return response
    
    def upload_dataset(self, file_path):
        url = self._build_url('upload_dataset')
        with open(file_path, 'rb') as f:
            files = {'dataset_file': f}
            response = requests.post(url, files=files, headers=self.headers)
        return response
    
    def get_datasets(self):
        url = self._build_url('datasets')
        response = requests.get(url, headers=self.headers)
        return response
    
    def download_pdf(self, dataset_id):
        url = self._build_url('download_pdf', dataset_id=dataset_id)
        response = requests.get(url, headers=self.headers)
        return response
