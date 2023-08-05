import sys
import logging

def main():
    """Entry point for the application script"""
    print("Call your main application code here")


log = logging.getLogger(__name__)
root_logger = logging.getLogger()
for handler in root_logger.handlers:
    root_logger.removeHandler(handler)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
for handler in log.handlers:
    log.removeHandler(handler)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log.addHandler(stream_handler)
