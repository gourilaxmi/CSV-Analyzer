from rest_framework import serializers
from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'dataset_file', 'pdf_file', 'status', 'error_log', 'uploaded_at']
        read_only_fields = ['id', 'pdf_file', 'status', 'error_log', 'uploaded_at']