import logging
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Dataset
from .serializers import DatasetSerializer
from .tasks import start_processing_thread

logger = logging.getLogger(__name__)

class DatasetUpload(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DatasetSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        dataset = serializer.save(user=request.user, status='pending')

        start_processing_thread(dataset.id)

        return Response({
            "message": "File uploaded. Pls wait while pdf is being generated. Pls visit Downloads to get the pdf",
            "dataset_id": dataset.id,
            "check_status_at": f"/api/datasets/"
        }, status=status.HTTP_202_ACCEPTED)

class UserDatasetList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DatasetSerializer

    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user).order_by('-uploaded_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DownloadPDF(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)

        if dataset.status != 'completed':
            return Response(
                {"error": f"Report not ready. Current status is {dataset.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not dataset.pdf_file:
            return Response({
                "error": "No PDF available",
                "dataset_id": dataset_id
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            return FileResponse(
                dataset.pdf_file.open('rb'),
                as_attachment=True,
                filename=f"pdf_report_{dataset.id}.pdf"
            )
        except FileNotFoundError:
            return Response({
                "error": "PDF file not found",
                "dataset_id": dataset_id
            }, status=status.HTTP_404_NOT_FOUND)