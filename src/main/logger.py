"""
Logger
This is the class for control logs and communication

Example of Usage:

    @initcontext   <<-- One time usage for initialise context for each micro-service
    def test(self):
        # Log Manager Initialisation
        logmanager = LogManager()
        global_logger = logmanager.get_global_logger()
        MessageFactory() # Auto Init Msg Factory
        
        # do something
        global_logger.error(Message.ERROR_BAD_FORMAT)
        global_logger.info(Message.DYNAMIC_INFO_SERVICE_STARTED.format_string('aaa', 2345))


"""

import logging
import logging.handlers
import os
import sys
import inspect


class LogManager():
    def __init__(self):
        self.context = None

        
    def get_global_logger(self):
        """
        This is the method for getting global logger and
        control all of the logs in any microservices that
        want to use this logger. After getting the logger
        """
        # Prepare logger and send back to caller
        logger = logging.getLogger('root')
        microservice_name = self.context['Microservice_Name'] + " " + self.context['Microservice_Version']
        

        if not logger.hasHandlers():
            # Global Logger Configuration Settings
            log_file = config.get_hms_settings('global_log', 'path')
            log_level = config.get_hms_settings('global_log', 'log_level').upper()
            log_rotate_when = config.get_hms_settings('global_log', 'rotate_when')
            log_max_backups = config.get_hms_settings('global_log', 'max_backups')

            # Set logs format
            log_format = logging.Formatter('%(asctime)s - %(levelname)s - ' + microservice_name +
                                        ' - %(filename)s - %(funcName)s - %(message)s')

            # Log handler initialisation
            log_handler = logging.handlers.TimedRotatingFileHandler(log_file, when=log_rotate_when,
                                                                    backupCount=log_max_backups)
            
            logger = self._log_init(logger, log_handler, log_format, log_level) 
            
            '''
            log_handler.setFormatter(log_format)
            log_handler.setLevel(log_level)

            logger.addHandler(log_handler)
            logger.setLevel(log_level)
            logger.propagate = False
            '''

        return logger


    def get_local_logger(self, logfile=None, log_rotate_when=None, log_max_backups=None, level='info'):
        """
        This is the method for getting local logger and control all the logs in any microservices.
        :param name: name of logger
        :param level: logging level of this handler.  level must be a str
        :logfile: set to null to log to stdout
        :return: Logger Objects
        """
        microservice_name = self.context['Microservice_Name']
        
        # Prepare logger and send back to caller
        logger = logging.getLogger(microservice_name)
        if not logger.hasHandlers():
            # Set level to upper case
            log_level = level.upper()

            # Set log format
            log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')

            # Initial log handler
            if logfile :
                log_handler = logging.handlers.TimedRotatingFileHandler(logfile, when=log_rotate_when,
                                                                    backupCount=log_max_backups)
            else:
                log_handler = logging.StreamHandler(stream=sys.stdout)

            logger = self._log_init(logger, log_handler, log_format, log_level) 
  
        return logger

    def _log_init(self, logger, log_handler, log_format, log_level):
        log_handler.setFormatter(log_format)
        log_handler.setLevel(log_level)

        logger.addHandler(log_handler)
        logger.setLevel(log_level)
        logger.propagate = False
        return logger


'''
Deprecated Warning!!!
DO NOT USE ANY CLASSES BELOW THIS LINE
'''

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.sys.path.insert(0, BASE_DIR)

from hmsutils.confighelper import HMSConfigHelper
config = HMSConfigHelper.get_instance()



class CommonLogger():
    """
        Deprecated Class
        Use:
            import hmsutils.logger as logger
            logger = logger.get_logger("HMS_VL")
            logger.info("any msg")
        Common Logger class
    """

    def __init__(self, str_format, handler_class, name, level, **kwargs):
        self.name = name
        formatter = logging.Formatter(str_format)
        handler = handler_class(**kwargs)
        handler.setFormatter(formatter)
        self.log = logging.getLogger(self.name)
        self.log.setLevel(level)
        self.log = self._adding_handler(handler)

    def _adding_handler(self, handler):
        self.log.addHandler(handler)
        return self.log

    def add_handler(self, str_format, handler_class, **kwargs):
        handler = handler_class(**kwargs)
        formatter = logging.Formatter(str_format)
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

    def getlogger(self):
        return self.log

#============================================


"""
def log(function):
    '''
    This is a decorator for auto prepared logging system
    usage:
        @log
        def anyfunction(global_logger, local_logger):
            global_logger.info("xxx")
            local_logger.info("yyy")

    '''

    def _prepared_logger(*args, **kwargs):
        # Prepare logger for sending to caller method

        context = ContextManager.get_context('logger', function)
        logmanager = LogManager(context)
   
        if 'global_logger' in inspect.getargspec(function).args:
            kwargs['global_logger'] = logmanager.get_global_logger()

        if 'local_logger' in inspect.getargspec(function).args:
            kwargs['local_logger'] = logmanager.get_local_logger()

        # Call Back
        function(*args, **kwargs)
    return _prepared_logger

"""

# ============================================================================
