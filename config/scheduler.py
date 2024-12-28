import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from models import LeadCallPlan
from datetime import datetime
from .database import db_instance

class CallPlanScheduler:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        if not cls._initialized:
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        if not CallPlanScheduler._initialized:
            self.scheduler = BackgroundScheduler(timezone=pytz.UTC)
            CallPlanScheduler._initialized = True
    
    def reset_daily_call_plan(self):
        """Resets total_calls_today to 0 and updates last_call_at for all leads."""
        try:
            db_session = db_instance.SessionLocal()
            db_session.query(LeadCallPlan).update(
                {
                    LeadCallPlan.total_calls_today: 0,
                    LeadCallPlan.last_call_at: None
                }
            )
            db_session.commit()
            print(f"Call plans reset successfully at {datetime.now(pytz.UTC)} UTC.")
        except Exception as e:
            print(f"Failed to reset call plans: {e}")
    
    def start(self):
        """Starts the scheduler with a midnight reset task."""
        if not self.scheduler.running:
            trigger = CronTrigger(hour=0, minute=0, timezone=pytz.UTC)
            self.scheduler.add_job(self.reset_daily_call_plan, trigger)
            self.scheduler.start()
            print("Scheduler started and job added for midnight reset.")
    
    def stop(self):
        """Stops the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("Scheduler stopped.")