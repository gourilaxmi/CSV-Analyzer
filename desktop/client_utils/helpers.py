import os
from datetime import datetime


def format_timestamp():
    return datetime.now().strftime("%H:%M:%S")


def get_media_path():
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    possible_paths = [
        os.path.join(os.path.dirname(current_dir), "backend", "media"),
        os.path.join(current_dir, "backend", "media"),
        os.path.join(current_dir, "media"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return os.path.join(current_dir, "backend", "media")


def get_charts_path(media_path, dataset_id):
    return os.path.join(media_path, "analysis", str(dataset_id), "charts")


def load_chart_files(charts_dir):
    if not os.path.exists(charts_dir):
        return []
    
    all_files = os.listdir(charts_dir)
    return [
        os.path.join(charts_dir, f) 
        for f in all_files 
        if f.endswith('.png')
    ]


def extract_error_message(response):
    try:
        error_data = response.json()
        
        if 'error' in error_data:
            return error_data['error']
        elif 'detail' in error_data:
            return error_data['detail']
        
        errors = []
        for field, messages in error_data.items():
            if isinstance(messages, list):
                errors.extend(messages)
            else:
                errors.append(str(messages))
        
        return '\n'.join(errors) if errors else response.text
    except:
        return response.text