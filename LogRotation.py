import logging
import logging.config
import time
from  logging.handlers import TimedRotatingFileHandler
import os
import shutil



#-------------------------------------------------------------------------
def owned_file_handler(filename, owner=None, *args, **kwargs):
    print("## IN ## : owned_file_handler")
    if owner:
        if not os.path.exists(filename):
            open(filename, 'a').close()
        #shutil.chown(filename, *owner, *owner)        
        group = 'klaud'
        shutil.chown(filename, group, group)        
    return logging.handlers.TimedRotatingFileHandler(filename, *args, **kwargs )
    #return TimedRotatingFileHandler(filename, *args, **kwargs )
    #return create_timed_rotation_log(filename)
   


#--------------------------------------------------------------------------

if __name__ == '__main__':
    #from optparse import OptionParser
    #parser = OptionParser("Test Logging")
    #parser.add_option('-d','–debug' , type='string', help='Available levels are CRITICAL (3), ERROR (2), WARNING (1), INFO (0), DEBUG (-1)',default='CRITICAL' )
    #options,args = parser.parse_args()

    config ={
        "version": 1,
        "formatters": {
            "simple": {"format": "[%(name)s] %(message)s"},
            "complex": {
                "format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": "DEBUG",
            },
            "file": {
                #"class": "logging.FileHandler",
                #"filename": "error.log",
                #"formatter": "complex",
                #"level": "ERROR",
                '()': owned_file_handler,  
                'owner': ['klaud', 'klaud'],
                'level': 'INFO',
                #'class': 'logging.handlers.TimedRotatingFileHandler',
                #'class': 'TimedRotatingFileHandler',
                'when': 'M',
                #'backupCount': 8,
                #'filename': f'/home/klaud/logs/aaa.log',
                'filename': f'/home/klaud/timed_test.log',               
                
            },
        },
        "klaud": {"handlers": ["console", "file"], "level": "WARNING"},
        "loggers": {"parent": {"level": "INFO"}, "parent.child": {"level": "DEBUG"},},
    }



    log_file = "timed_test.log"    

    #logging.config.fileConfig('logging.conf')
    logging.config.dictConfig(config)
    logger = logging.getLogger("klaud")
    #logger = logging.getLogger("sLogger")    
    logger.setLevel(logging.INFO)

    #create_timed_rotation_log(log_file)
    print("## Calling : owned_file_handler")
    handler = owned_file_handler(log_file, "klaud", when='m', 
                                            interval=1
                                            );


    #handler = TimedRotatingFileHandler( path,
    #                                    when="m",
    #                                    interval=1,
    #                                    backupCount=5)
    logger.addHandler(handler)

    for i in range(6):
        logger.info("This is a test!")
        time.sleep(75)


    




