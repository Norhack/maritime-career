import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger("scheduler")


async def job_collection():
    logger.info("Running hourly job collection")


async def news_collection():
    logger.info("Running hourly news collection")


async def daily_report():
    logger.info("Running daily report")


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_collection, CronTrigger(minute=0))
    scheduler.add_job(news_collection, CronTrigger(minute=0))
    scheduler.add_job(daily_report, CronTrigger(hour=6, minute=0))
    scheduler.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_scheduler()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
