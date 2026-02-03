from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="datasets")
    dataset_file = models.FileField(upload_to="datasets/")
    pdf_file = models.FileField(upload_to="pdfs/", null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_log = models.TextField(null=True, blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.uploaded_at}"