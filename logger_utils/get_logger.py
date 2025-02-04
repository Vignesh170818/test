from configparser import ConfigParser, ExtendedInterpolation
import os
import logging
from logging.handlers import RotatingFileHandler
import json
import settings

def get_logger(name: str =__name__,filename: str =None, log_folder: str =None):
    """
    create a logger object either reading logging configuration from
    a file or create logger which logs to console."""
    if settings.app_json['AppLog']:
        #config = ConfigParser(interpolation=ExtendedInterpolation())
        #config.read_file(fh)
        log_dir = settings.app_json['AppLog']['LogDir']
        try:
            if not os.path.isdir(log_dir):
                os.mkdir(log_dir)
        except Exception as e:
            log_dir = os.getcwd()

        #logfile = os.path.join(log_dir, config.get('app_log', 'filename'))
        if filename and  log_folder == None:
            logfile = os.path.join(log_dir,filename)
        elif filename and log_folder:
            log_dir = os.path.join(log_dir,log_folder)
            logfile = os.path.join(log_dir,filename)
        else:
            logfile = os.path.join(log_dir, settings.app_json['AppLog']['FileName'])


        # logger.info(f"Initializing logger obj, log file is '{logfile}'")
        log_format = settings.app_json['AppLog']['Format']
        max_bytes = int(settings.app_json['AppLog']['MaxLogBytes'])
        backups = int(settings.app_json['AppLog']['BackUps'])
        # "log_level" will hold value of type String from R4.0, 
        # this is OCD requirement to support "MyWizardLogLevel" placeholder
        log_level = settings.app_json['AppLog']['LogLevel']
        log_level = log_level.upper()
        if log_level == 'ALL' or log_level == 'DEBUG':
            log_level = logging.DEBUG
        elif log_level == 'INFO':
            log_level = logging.INFO
        elif log_level == 'WARN':
            log_level = logging.WARN
        elif log_level == 'ERROR':
            log_level = logging.ERROR
        elif log_level == 'FATAL':
            log_level = logging.FATAL
        else:
            msg = "Configuration attr 'log_level' is not to one of these: \
                'ALL', 'DEBUG', 'INFO', 'WARN', 'ERROR' or 'FATAL'. This is a required \
                value. This value is supplied from 'MyWizardLogLevel' placeholder in the configuration."
            raise ValueError(msg)
        
        nlogger = logging.getLogger(name)
        handler = RotatingFileHandler(logfile, maxBytes=max_bytes, backupCount=backups)
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        nlogger.addHandler(handler)
        #nlogger.propagate=False
    else:
        log_format = '{"LogType":"%(levelname)s","DateTime":"%(asctime)s","AppService":"%(app_name)s","Message": "%(info)s" ,"Component":"%(filename)s","SubComponent":"%(funcName)s","Title":"%(title)s","ClientUId":"%(ClientUId)s", "DeliveryConstructUId":"%(DeliveryConstructUId)s","AssemblyNamespace":"%(pathname)s","CorrelationUId":"%(CorrelationUId)s","Exception":"%(Exception)s"}'
        log_level = 'DEBUG'
        nlogger = logging.getLogger(name)
        #nlogger.propagate=False
        if not nlogger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)
            nlogger.addHandler(handler)

    nlogger.setLevel(log_level)
    for log_name, log_obj in nlogger.manager.loggerDict.items():
       if isinstance(log_obj,logging.Logger):
          for i in ['botocore','binaryornot','azure','chardet']:
             if i in log_name:
                  log_obj.setLevel("ERROR")

    return nlogger