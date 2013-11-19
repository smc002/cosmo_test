import time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end, ea_initialize_test
import browser_auto as browser_auto
from constant_utility import config_file, active_kwd_list, task_executed_kwd_list, initialize_test_folders, lookup_keyword_in_ea_log, removeall, time_sleep
import config_file


test_name = 'stress_test'
TEST_REPEAT = 1000

def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)
        return callHelper
    return repeatHelper

def stress_test(repeat_times = 10):
    ea_log_path, ea_log_file, logger = initialize_test_folders(test_name)
    logger.critical("Initialize Stress Test.")

    #ea_initialize_test(log_folder=ea_log_path)
    config_file.initialize(log_folder=ea_log_path)
    '''shutil.copy('ea/Configuration.ini', config_file)
    ea_start(delay=15)
    ea_click(item='file_name')
    ea_config('folder', ea_log_path)
    ea_close()'''

    logger.critical("Initialize Stress Test Finished.")

    cnt = 0
    passed_number = 0
    while cnt < repeat_times:
        cnt += 1

        logger.critical("Stress Test No.{} BEGIN.".format(cnt))
        removeall(ea_log_path)
        ea_start(delay=0)
        passed = browser_auto.run_normal_test()
        ea_close()

        try:
            assert passed, 'Browser Automation FAILED!'
            assert os.path.exists(ea_log_file), 'EA log: {} not found!'.format(ea_log_file)
            assert lookup_keyword_in_ea_log(active_kwd_list + task_executed_kwd_list, ea_log_file), 'Not all the keywords were found in EA log!'
        except AssertionError as e:
            logger.critical("Stress Test No.{} FAILED.".format(cnt))
            logger.critical(str(e))
        except Exception as e:
            logger.critical("Stress Test No.{} UNKOWN ERROR.".format(cnt))
            logger.critical(str(e))
        else:
            logger.critical("Stress Test No.{} PASSED.".format(cnt))
            passed_number += 1
        logger.critical('Pass rate till now is {}'.format(passed_number/cnt))

        if cnt%100 == 0:
            time_sleep(2)  #delete temp file too hurry might prevent firefox from closing
            removeall(r'C:\Users\msun\AppData\Local\temp')  #the files here could be too large, if running for hours

if __name__ == "__main__":
    stress_test(50)

    
    '''while 1:
        try:
            unittest.main(verbosity=2,exit=False)
        except:
            print("An exception is detected.")
            logging.warning("An exception is detected.")
            continue
        else:
            suc_cnt += 1
            print("Test {} successed.".format(suc_cnt))
            logging.info("Test {} successed.".format(suc_cnt))'''

