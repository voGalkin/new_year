from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from utils import delete_qrcodes

def start_scheduler():
    """Запускает планировщик задач."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        delete_qrcodes, 
        trigger=IntervalTrigger(minutes=10),  # Интервал запуска задачи
        id="delete_qrcodes",  # Уникальный идентификатор задачи
        replace_existing=True
    )
    scheduler.start()
    return scheduler
