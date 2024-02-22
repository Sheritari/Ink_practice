from celery import shared_task
from practice.celery import app
from .export import export_characteristics_to_excel, export_data_to_excel

@shared_task(bind=True)
def export_task(self):
    self.update_state(state='PENDING')
    data = export_characteristics_to_excel()
    self.update_state(state='COMPLETE')
    return {'result': data}

@app.task(bind=True)
def export_data_to_excel_task(self):
    self.update_state(state='PENDING')
    file_path = export_data_to_excel()
    self.update_state(state='COMPLETE')
    return {'result': file_path}
