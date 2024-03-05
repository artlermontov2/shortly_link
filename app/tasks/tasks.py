from datetime import timedelta
import asyncio
from app.tasks.celery import celery
from app.reduction.dao import ReductionDAO

@celery.task
def periodic_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ReductionDAO.delete_after_expire())

celery.conf.beat_schedule = {
    'add-every-24-hours': {
        'task': 'app.tasks.tasks.periodic_task',
        'schedule': 20,

    },
}
# timedelta(days=1)