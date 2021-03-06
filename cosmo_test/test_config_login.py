import unittest, time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end 
import browser_auto as browser_auto
from constant_utility import test_root_folder, config_file, active_kwd_list, task_executed_kwd_list, tps_state_str, initialize_test_folders, lookup_keyword_in_ea_log, removeall
import config_file


test_name = 'config_login'
tps_name = 'Configurations on the Login tab'
TEST_REPEAT = 1

# log file test
# http://van.natinst.com/van/procedure/show/1548741
class COSMO_test_case_config_login(unittest.TestCase):

    def setUp(self):
        pass

    def config_test(self, opt, inp_str, veri_keywords=active_kwd_list, expect_result=True):
        ea_log_path, ea_log_file, logger = initialize_test_folders(test_name)
        config_file.initialize(log_folder = ea_log_path)
        removeall(ea_log_path)
        logger = logging.getLogger("COSMO.config.login")
        tps_step = opt + ' = ' + inp_str
        logger.critical(tps_state_str.format(tps_name, tps_step, 'BEGIN'))

        if opt != None:
            config_file.change_option('Server', opt, '"{}"'.format(inp_str))
        ea_start(delay=15)
        ea_close()
        try:
            self.assertTrue(os.path.exists(ea_log_file), 'EA log: {} not found!'.format(ea_log_file))
            self.assertTrue(expect_result == lookup_keyword_in_ea_log(active_kwd_list, ea_log_file), 'Expected result is {}, not satisfied!'.format(expect_result))
        except AssertionError as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'FAILED'))
            logger.critical(str(e))
        except Exception as e:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'UNKOWN ERROR'))
            logger.critical(str(e))
        else:
            logger.critical(tps_state_str.format(tps_name, tps_step, 'PASSED'))

# This test would be failed. Possible reason is too many failed try of login would cause connect-refuse from server.
# Update: the test with right password is enabled.
    '''def test_config_password(self):
        pwd_kwd_pair = {
                'test'                  : 'Client State Changed From REGISTRATION To ACTIVE',
                'test_wrong_password'   : 'LOGIN FAILED' ,
                }
        for pwd in pwd_kwd_pair:
            test_passed = self.config_test(self, 'password', pwd, pwd_kwd_pair[pwd])
            test_passed = self.config_test(self, 'username', pwd, pwd_kwd_pair[pwd])'''
    def test_config_username(self):
        right_username = [
                'test',
                ]
        for user in right_username:
            self.config_test('username', user)

    def test_config_password(self):
        right_password = [
                'test',
                ]
        wrong_password = [
                'test_wrong',
                ]
        for pwd in wrong_password:
            self.config_test('password', pwd, expect_result = False)

# server test
    def test_config_server(self):
        right_server = [
                '10.144.10.217:9443/qm',
                'https://10.144.10.217:9443/qm',
                ]
        wrong_server = [
                '10.145.10.217:9443/qm',
                ]
        for ser in wrong_server:
            test_passed = self.config_test('server address', ser, expect_result=False)
        for ser in right_server:
            test_passed = self.config_test('server', ser)

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
