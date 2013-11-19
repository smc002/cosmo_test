import unittest, time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end 
import browser_auto as browser_auto
from constant_utility import test_root_folder, config_file, active_kwd_list, task_executed_kwd_list, tps_state_str, initialize_test_folders, lookup_keyword_in_ea_log, removeall
import config_file


test_name = 'config_ini_file'
tps_name = 'Save/load ini file which contains global EA settings'
TEST_REPEAT = 1

# http://van.natinst.com/van/procedure/show/1548649
class COSMO_test_case_ini_file(unittest.TestCase):

    def setUp(self):
        pass

    def test_config_ini_file(self):
        ea_log_path, ea_log_file, logger = initialize_test_folders(test_name)
        tps_step = '1-2'
        removeall(config_file)
        ea_start(handle_ts=False)
        try:
            with open(config_file, 'r') as f:
                self.assertTrue(len(f.read())==0, 'config file is not empty')
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))
        tps_step = '3'
        # test_items = ['server', 'username', 'password', 'project_area', 'adapter_name']
        # todo: cann't test password; encrypt make the file a mess, python could not read that file
        test_items = ['server', 'username', 'project_area', 'adapter_name']
        for i in test_items:
            t_i = 'test_' + i
            print(t_i)
            ea_config(i, t_i)
        ea_close()
        try:
            with open(config_file, 'r') as f:
                config_content = f.read()
            for i in test_items:
                t_i = 'test_' + i
                if i != 'password':
                    self.assertTrue(t_i in config_content, 'content: {} could not be found'.format(t_i))
                else:
                    self.assertTrue(t_i not in config_content, 'password is read directly')
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))

    def tearDown(self):
        try:
            ea_close()
        except:
            pass
        pass
        #self.driver.close()

if __name__ == "__main__":
    for cnt in range(TEST_REPEAT):
        unittest.main(verbosity=2, exit=False)
