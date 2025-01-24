from celery import Celery

app = Celery(
    "flag_pattern_detection",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.tasks"]
)

app.conf.beat_schedule = {
    "fetch-data-every-minute": {
        "task": "app.tasks.fetch_data",
        "schedule": 60.0,  # Every minute
    },
    "detect-patterns-every-5-minutes": {
        "task": "app.tasks.detect_and_save_patterns",
        "schedule": 360.0,  # Every 5 minutes
    },
    "clean-old-data-every-1-hour":{
        "task":"app.tasks.cleanup_old_data",
        "schedule":3600.0 , #every 1 hour
    }

}
app.conf.timezone = "UTC"
