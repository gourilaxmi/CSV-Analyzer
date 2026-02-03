from rest_framework import serializers
from .models import Dataset
import os

class DatasetSerializer(serializers.ModelSerializer):
    
    error_message = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = ['id', 'dataset_file', 'pdf_file', 'status', 'uploaded_at', 'error_message']
        read_only_fields = ['pdf_file', 'status', 'uploaded_at', 'error_message']

    def get_error_message(self, obj):
        return obj.error_log

    def validate_dataset_file(self, value):
        MAX_SIZE = 20 * 1024 * 1024  # 20MB
        
        if value.size > MAX_SIZE:
            raise serializers.ValidationError("File size exceeds 20MB.")
        
        ext = os.path.splitext(value.name)[1].lower()
        if ext != '.csv':
            raise serializers.ValidationError("Only CSV files are allowed.")
        
        return value