import asyncio
from datetime import timedelta

from app.reduction.dao import ReductionDAO
from app.tasks.celery import celery


@celery.task
def periodic_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ReductionDAO.delete_after_expire())

celery.conf.beat_schedule = {
    'add-every-24-hours': {
        'task': 'app.tasks.tasks.periodic_task',
        'schedule': timedelta(days=1),

    },
}
