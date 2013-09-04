import sys, os, logging


test_root_folder = 'C:\\cosmo_autotest\\'

config_path = r'C:\Users\Public\Documents\National Instruments\Test Integration Adapter 1.0'
config_file = os.path.join(config_path, 'Configuration.ini')
active_kwd_list = ['Client State Changed From INITIALIZATION To LOGIN',
        'Client State Changed From LOGIN To REGISTRATION',
        'Client State Changed From REGISTRATION To ACTIVE',
        ]
task_executed_kwd_list = [
        'Process Task',
        'Finished Execution',
        ]

tps_state_str = 'TPS: {}, step: {}, state: {}'

def initialize_test_folders(test_name):
    if not os.path.exists(test_root_folder):
        os.mkdir(test_root_folder)
    ea_log_path = test_root_folder + test_name + '\\'
    if not os.path.exists(ea_log_path):
        os.mkdir(ea_log_path)
    ea_log_file = os.path.join(ea_log_path, 'system log.html')

def lookup_keyword_in_ea_log(keywords, ea_log):
    if not os.path.exists(ea_log):
        logger.error('EA log file not found in {}'.format(ea_log))
        return False
    with open(ea_log, 'rt') as f:
        log_content = f.read()
    logger.debug(log_content)
    keyword_found = True
    for kwd in keywords:
        if not kwd in log_content:
            logger.info('Keyword {} is NOT found in EA log {}'.format(kwd, ea_log))
            keyword_found = False
        else:
            logger.info('Keyword {} is found in EA log {}'.format(kwd, ea_log))
    return keyword_found

# removeall function
ERROR_STR= """Cann't removing {}, error: {} """  
  
def rmgeneric(path, __func__):  
  
    logger = logging.getLogger("COSMO")

    try:  
        __func__(path)  
        logger.info('Removed: {}'.format(path))
        ##print ('Removed ', path  )
    except OSError as err:  
        logger.info('Remove failed: {}'.format(path))
        logger.info(str(err))
        ##print (ERROR_STR.format(path, err))
        pass
              
def removeall(path):  
  
    if not os.path.isdir(path):  
        if os.path.exists(path):
            f=os.remove  
            rmgeneric(path, f)  
        return  
      
    files=os.listdir(path)  
  
    for x in files:  
        fullpath=os.path.join(path, x)  
        if os.path.isfile(fullpath):  
            f=os.remove  
            rmgeneric(fullpath, f)  
        elif os.path.isdir(fullpath):  
            removeall(fullpath)  
            f=os.rmdir  
            rmgeneric(fullpath, f)  
