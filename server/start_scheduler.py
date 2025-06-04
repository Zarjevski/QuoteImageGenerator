from dotenv import load_dotenv
load_dotenv()

import schedule
import time
import logging
from services.post_job import run_scheduled_post

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
)

def scheduled_job():
    logging.info("Running scheduled post...")
    try:
        run_scheduled_post()
        logging.info("✅ Post completed successfully.")
    except Exception as e:
        logging.error(f"❌ Error during post: {e}")

# Schedule every 6 hours
schedule.every(24).hours.do(scheduled_job)

scheduled_job()  # Run first immediately


logging.info("🚀 Scheduler started. Waiting for next run...")

while True:
    schedule.run_pending()
    time.sleep(60)
