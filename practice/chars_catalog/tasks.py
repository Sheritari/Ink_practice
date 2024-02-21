from celery import shared_task
from .export import export_characteristics_to_excel

@shared_task(bind=True)
def export_task(self):
    self.update_state(state='PENDING')
    data = export_characteristics_to_excel()
    self.update_state(state='COMPLETE')
    return {'result': data}