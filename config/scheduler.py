from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from models.lead_call_plan import LeadCallPlan
from datetime import datetime
import pytz

class CallPlanScheduler:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.scheduler = BackgroundScheduler(timezone=pytz.UTC)

    def reset_daily_call_plan(self):
        """Resets total_calls_today to 0 and updates last_call_at for all leads."""
        try:
            self.db.query(LeadCallPlan).update(
                {
                    LeadCallPlan.total_calls_today: 0,
                    LeadCallPlan.last_call_at: None
                }
            )
            self.db.commit()
            print(f"Call plans reset successfully at {datetime.now(pytz.UTC)} UTC.")
        except Exception as e:
            self.db.rollback()
            print(f"Failed to reset call plans: {e}")

    def start(self):
        """Starts the scheduler with a midnight reset task."""
        trigger = CronTrigger(hour=0, minute=0, timezone=pytz.UTC)
        self.scheduler.add_job(self.reset_daily_call_plan, trigger)
        self.scheduler.start()
        print("Scheduler started and job added for midnight reset.")

    def stop(self):
        """Stops the scheduler."""
        self.scheduler.shutdown()
        print("Scheduler stopped.")
