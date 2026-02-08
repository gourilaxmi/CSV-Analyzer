import os
import json
import logging
import threading
from django.conf import settings
from django.db import transaction
from .models import Dataset
from .utils import process_csv, visualization_csv, pdf_report

logger = logging.getLogger(__name__)

def process_dataset_task(dataset_id):
    try:
        
        with transaction.atomic():
            dataset = Dataset.objects.select_for_update().get(id=dataset_id)
            dataset.status = 'processing'
            dataset.save()

        csv_path = dataset.dataset_file.path
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file missing at: {csv_path}")

        # make required directories if it doesn't exist to store csv files, charts ad pdf's
        base_dir = os.path.join(settings.MEDIA_ROOT, "analysis", str(dataset.id))
        chart_dir = os.path.join(base_dir, "charts")
        pdf_dir = os.path.join(settings.MEDIA_ROOT, "pdfs")
        
        os.makedirs(chart_dir, exist_ok=True)
        os.makedirs(pdf_dir, exist_ok=True)

        # do csv processing
        df, stats = process_csv(csv_path)

        # create charts
        viz = visualization_csv(
            df, 
            chart_dir, 
            outlier_counts=stats.get('outliers', {}),
            equip_dist=stats.get('equip_dist', {}),
            equip_averages=stats.get('equip_averages', {})
        )
        charts = viz.plots() 

        pdf_filename = f"report_{dataset.id}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        # pdf generation
        pdf_report(pdf_path, stats, charts)

        #analysis results for Chart.js
        analysis_results = {
            'total_rows': stats.get('total_rows', 0),
            'equipment_distribution': stats.get('equip_dist', {}),
            'equipment_averages': stats.get('equip_averages', {}),
            'field_statistics': stats.get('stats', {}),
            'outliers': stats.get('outliers', {}),
            'numeric_columns': list(df.select_dtypes(include=['number']).columns.tolist()),
            'correlation_data': df.select_dtypes(include=['number']).corr().to_dict() if df.select_dtypes(include=['number']).shape[1] >= 2 else {}
        }

        with transaction.atomic():
            dataset = Dataset.objects.select_for_update().get(id=dataset_id)
            dataset.pdf_file.name = f"pdfs/{pdf_filename}"
            dataset.analysis_results = json.dumps(analysis_results)
            dataset.status = 'completed'
            dataset.error_log = None
            dataset.save()

    except Exception as e:
        logger.exception(f"Failed to process dataset {dataset_id}")
        Dataset.objects.filter(id=dataset_id).update(
            status='failed', 
            error_log=str(e)
        )

def start_processing_thread(dataset_id):
    thread = threading.Thread(
        target=process_dataset_task,
        args=(dataset_id,),
        daemon=True  
    )
    thread.start()
    logger.info(f"Asynchronous thread started for Dataset ID: {dataset_id}")