import os
import logging
import logging.handlers
from datetime import datetime


class LoggerSetup:
    """
    This class is used to setup a logger with file rotation and archiving.
    It can be used specify logging filename, directory, and level.
    """
    filename = os.path.basename(__file__)
    def __init__(self, log_file=filename, log_dir='logs', log_level=logging.DEBUG):
        self.log_file = log_file
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = None
        self.setup()

    def setup(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        log_format = ("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
        date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(self.log_dir, f"{self.log_file}_{date_time}.log")

        self.logger = logging.getLogger(self.log_file)
        self.logger.setLevel(self.log_level)

        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file, when='midnight', interval=1, backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(log_format))       
        self.logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
