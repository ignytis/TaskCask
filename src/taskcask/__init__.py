import logging
import os

logging.basicConfig(format="%(asctime)s PID %(process)d [%(levelname)s] %(name)s: %(message)s")

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.getLogger(__name__).setLevel(log_level)
