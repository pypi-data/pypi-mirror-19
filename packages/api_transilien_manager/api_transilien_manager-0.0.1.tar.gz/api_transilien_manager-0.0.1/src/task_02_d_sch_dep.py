import os
import logging
from os import sys, path
import datetime

if __name__ == '__main__':
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    # Logging configuration
    from src.utils_misc import set_logging_conf
    set_logging_conf(log_name="task02_d_sch_dep.log")

from src.utils_mongo import mongo_async_upsert_chunks
from src.mod_02_find_schedule import save_scheduled_departures_of_day_mongo
from src.utils_misc import get_paris_local_datetime_now

logger = logging.getLogger(__name__)

# Save for next day
logger.info("Task: daily update of scheduled departures: today and tomorrow")

today_paris = get_paris_local_datetime_now()
today_paris_str = today_paris.strftime("%Y%m%d")
tomorrow_paris = today_paris + datetime.timedelta(days=1)
tomorrow_paris_str = tomorrow_paris.strftime("%Y%m%d")

logger.info("Paris today date is %s" % today_paris_str)

# logger.info("Updating scheduled departures for %s" % today_paris_str)
# save_scheduled_departures_of_day_mongo(today_paris_str)

logger.info("Updating scheduled departures for %s" % today_paris_str)
save_scheduled_departures_of_day_mongo(tomorrow_paris_str)
