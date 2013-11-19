import unittest, time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end 
import browser_auto as browser_auto
from constant_utility import test_root_folder, config_file, active_kwd_list, task_executed_kwd_list, tps_state_str, initialize_test_folders, lookup_keyword_in_ea_log, removeall, shutdown_kwd_list 
import config_file
import ts_auto


test_name = 'abort_ts'
tps_name = 'Abort TestStand before test'
# http://van.natinst.com/van/procedure/show/1552046
TEST_REPEAT = 1

class COSMO_test_case_ini_file(unittest.TestCase):

    def setUp(self):
        pass

    def test_config_ini_file(self):
        ea_log_path, ea_log_file, logger = initialize_test_folders(test_name)
        config_file.initialize(log_folder = ea_log_path)
        removeall(ea_log_path)
        tps_step = '1-5'
        ea_start(delay=5)
        if not ts_auto.ts_close():# todo: ts_close is not stable enough
            logger.critical('Close TestStand FAILED!')
        ea_close()
        try:
            self.assertTrue(os.path.exists(ea_log_file), 'EA log: {} not found!'.format(ea_log_file))
            self.assertTrue(lookup_keyword_in_ea_log(shutdown_kwd_list, ea_log_file), 'Not all the keywords were found in EA log!')
        except AssertionError as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'UNKOWN ERROR'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))
        # todo: step 6 of the tps; browser auto improvement is needed

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
