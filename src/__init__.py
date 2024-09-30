import logging.handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_format_string = "%(asctime)s %(levelname)-8s --- %(message)-80s --- %(name)s:%(lineno)d "
logfile_format_string = "%(asctime)s %(levelname)-8s --- %(message)s --- %(name)s:%(lineno)d "

console_datetime_fmt = "%H:%M:%S"
logfile_datetime_fmt = "%Y-%m-%d %H:%M:%S"

console_formatter = logging.Formatter(fmt=console_format_string, datefmt=console_datetime_fmt)
logfile_formatter = logging.Formatter(fmt=logfile_format_string, datefmt=logfile_datetime_fmt)

console_handler = logging.StreamHandler()
logfile_handler = logging.FileHandler(filename="../logs/log.log", mode="w")
rotating_logfile_handler = logging.handlers.RotatingFileHandler(filename="../logs/rotating_log.log",
                                                                maxBytes=1000000,
                                                                backupCount=2)

console_handler.setFormatter(console_formatter)
logfile_handler.setFormatter(logfile_formatter)
rotating_logfile_handler.setFormatter(logfile_formatter)

console_handler.setLevel(logging.DEBUG)
logfile_handler.setLevel(logging.DEBUG)
rotating_logfile_handler.setLevel(logging.WARNING)

logger.addHandler(console_handler)
logger.addHandler(logfile_handler)
logger.addHandler(rotating_logfile_handler)

logger.info(f"Logger {__name__} started.")
