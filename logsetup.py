import logging
import os
from datetime import datetime


# Setup logging
date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists("./logs/"):
    os.makedirs("./logs/")

## main logs
log_formatter = logging.Formatter(
    "%(asctime)s | %(name)-18.18s | %(threadName)-12s | %(levelname)-8.8s | %(message)s"
)
main_logger = logging.getLogger("main")
main_logger.setLevel(logging.DEBUG)

### log to console
main_console_handler = logging.StreamHandler()
main_console_handler.setLevel(logging.INFO)
main_console_handler.setFormatter(log_formatter)
main_logger.addHandler(main_console_handler)

### log to file
main_file_handler = logging.FileHandler(f"logs/{date_str}_main.log", encoding="utf-8")
main_file_handler.setLevel(logging.DEBUG)
main_file_handler.setFormatter(log_formatter)
main_logger.addHandler(main_file_handler)


# root logs (all logs combined)
log_formatter_with_name = logging.Formatter(
    "%(asctime)s | %(name)-18.18s | %(threadName)-12s | %(levelname)-8.8s | %(message)s"
)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.handlers.clear()

### log to console
root_console_handler = logging.StreamHandler()
root_console_handler.setLevel(logging.WARNING)
root_console_handler.setFormatter(log_formatter_with_name)
root_logger.addHandler(root_console_handler)

### log to file
root_file_handler = logging.FileHandler(f"logs/{date_str}_root.log", encoding="utf-8")
root_file_handler.setLevel(logging.INFO)
root_file_handler.setFormatter(log_formatter_with_name)
root_logger.addHandler(root_file_handler)
