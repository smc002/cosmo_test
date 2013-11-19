import unittest, time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end 
import browser_auto as browser_auto
from constant_utility import test_root_folder, config_file, active_kwd_list, task_executed_kwd_list, tps_state_str, initialize_test_folders, lookup_keyword_in_ea_log, removeall, shutdown_kwd_list, time_sleep
import config_file
import ts_auto


test_name = 'two_ts'
tps_name = 'Start client while TestStand is running'
# http://van.natinst.com/van/procedure/show/1548727
TEST_REPEAT = 1

class COSMO_test_case_ini_file(unittest.TestCase):

    def setUp(self):
        pass

    def test_config_ini_file(self):
        ea_log_path, ea_log_file, logger = initialize_test_folders(test_name)
        config_file.initialize(log_folder = ea_log_path)
        removeall(ea_log_path)
        tps_step = '1-5'
        ts_auto.ts_start(delay=5)
        ea_start(delay=15)
        passed = browser_auto.run_normal_test()
        time_sleep(20)
        ea_close()
        ts_closed = ts_auto.ts_close()
        try:
            self.assertTrue(passed, 'Browser Automation Failed!')
            self.assertTrue(ts_closed, 'TestStand close Failed!')
            self.assertTrue(os.path.exists(ea_log_file), 'EA log: {} not found!'.format(ea_log_file))
            self.assertTrue(lookup_keyword_in_ea_log(active_kwd_list, ea_log_file), 'Not all the keywords were found in EA log!')
            self.assertTrue(lookup_keyword_in_ea_log(task_executed_kwd_list, ea_log_file), 'Not all the keywords were found in EA log!')
        except AssertionError as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'UNKOWN ERROR'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))

    def tearDown(self):
        try:
            os.system('taskkill /f /im "Test Integration Adapter.exe"')
            os.system('taskkill /f /im SeqEdit.exe')
        except:
            pass
        pass
        #self.driver.close()

if __name__ == "__main__":
    for cnt in range(TEST_REPEAT):
        unittest.main(verbosity=2, exit=False)
