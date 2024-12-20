from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from utils import delete_qrcodes, delete_postcards

def start_scheduler():
    """Запускает планировщик задач."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        delete_qrcodes, 
        trigger=IntervalTrigger(minutes=5),
        id="delete_qrcodes",
        replace_existing=True
    )
    scheduler.add_job(
        delete_postcards, 
        trigger=IntervalTrigger(minutes=5),
        id="delete_postcards",
        replace_existing=True
    )
    scheduler.start()
    return scheduler