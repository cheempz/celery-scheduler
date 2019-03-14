import celery
import os


os.environ['APPOPTICS_SERVICE_KEY'] = '<appoptics-service-key>'
os.environ['APPOPTICS_DEBUG_LEVEL'] = '4'

import appoptics_apm

@celery.task()
def print_hello():
    ready_check = appoptics_apm.appoptics_ready(3000, True)
    print('====> ready check result: %s' % ready_check)
    try:
        # start a trace, and set a transaction name on this task
        appoptics_apm.start_trace('celery_stick', keys=None, xtr=None)
        appoptics_apm.set_transaction_name('celery_stick')
        logger = print_hello.get_logger()
        logger.info("Hello")
        pizza()
    finally:
        # end the trace
        appoptics_apm.end_trace('celery_stick')

@appoptics_apm.log_method('pizza')
def pizza():
    logger = print_hello.get_logger()
    logger.info('In pizza')
