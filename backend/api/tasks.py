import os
import logging
from django.conf import settings
from django.db import transaction
from .models import Dataset
from .utils import process_csv, visualization_csv, pdf_report
import threading
logger = logging.getLogger(__name__)

def process_dataset_task(dataset_id):

    try:
        with transaction.atomic():
            dataset = Dataset.objects.get(id=dataset_id)
            dataset.status = 'processing'
            dataset.save()

        csv_path = dataset.dataset_file.path

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        output_dir = os.path.join(settings.MEDIA_ROOT, "charts", str(dataset.id))
        os.makedirs(output_dir, exist_ok=True)

        #process csv
        df, summary = process_csv(csv_path)

        #visualizations
        viz = visualization_csv(df, output_dir, outlier_counts=summary.get('outliers', {}))
        charts = viz.plots() 

        #pdf report
        pdf_filename = f"report_{dataset.id}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, "pdfs", pdf_filename)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        
        pdf_report(pdf_path, summary, charts)

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF was not created: {pdf_path}")

        with transaction.atomic():
            dataset = Dataset.objects.select_for_update().get(id=dataset_id)
            dataset.pdf_file.name = f"pdfs/{pdf_filename}"
            dataset.status = 'completed'
            dataset.error_log = None
            dataset.save()

        return {"status": "success", "dataset_id": dataset_id}
    
    except Dataset.DoesNotExist:
        return {"status": "error", "message": f"Dataset {dataset_id} not found"}

    except Exception as e:
        try:
            with transaction.atomic():
                dataset = Dataset.objects.select_for_update().get(id=dataset_id)
                dataset.status = 'failed'
                dataset.error_log = str(e)
                dataset.save()
            
            logger.info(f"Updated dataset {dataset_id} status to failed")
        
        except Exception as save_error:
            logger.exception(f"Failed to update dataset status: {save_error}")
        
        return {"status": "error", "message": str(e)}
            
def start_processing_thread(dataset_id):

    thread = threading.Thread(
        target=process_dataset_task,
        args=(dataset_id,),
        daemon=True  
    )
    thread.start()
    logger.info(f"Started processing thread for dataset {dataset_id}")
