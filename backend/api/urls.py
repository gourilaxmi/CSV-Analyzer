from django.urls import path
from .views import DatasetUpload, UserDatasetList, DownloadPDF, DatasetStatus

urlpatterns = [
    path('upload-dataset/', DatasetUpload.as_view(), name='upload_dataset'),
    path('datasets/', UserDatasetList.as_view(), name='user_datasets'),
    path('dataset-status/<int:dataset_id>/', DatasetStatus.as_view(), name='dataset_status'),
    path('download-pdf/<int:dataset_id>/', DownloadPDF.as_view(), name='download_pdf'),
]