import logging
import logging.config

def configure_console_logger(name):
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - [%(levelname)s] - [%(filename)s] - %(message)s'}
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            'default': {
                'level': 'DEBUG',
                'handlers': ['console']
            }
        },
        'disable_existing_loggers': False
    })
    return logging.getLogger(name)

def configure_file_logger(name, log_path):
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - [%(levelname)s] - [%(filename)s] - %(message)s'}
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': log_path
            }
        },
        'loggers': {
            'default': {
                'level': 'DEBUG',
                'handlers': ['file']
            }
        },
        'disable_existing_loggers': False
    })
    return logging.getLogger(name)