import unittest, time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end 
import browser_auto as browser_auto
from constant_utility import test_root_folder, config_file, active_kwd_list, task_executed_kwd_list, tps_state_str, initialize_test_folders, lookup_keyword_in_ea_log, removeall
import config_file


test_name = 'performance_restart_time'
tps_name = 'Performance: Restart Time'
TEST_REPEAT = 1

# http://nippm.natinst.com/itg/web/knta/crt/RequestDetail.jsp?REQUEST_ID=422416
class COSMO_test_case_performance(unittest.TestCase):

    def setUp(self):
        pass

    def restart_time_test(self, opt, inp_str, veri_keywords=active_kwd_list, expect_result=True):
        ea_log_path, ea_log_file, logger = initialize_test_folders(test_name)
        config_file.initialize(log_folder = ea_log_path)
        removeall(ea_log_path)
        logger = logging.getLogger("COSMO.config.login")
        tps_step = opt + ' = ' + inp_str
        logger.critical(tps_state_str.format(tps_name, tps_step, 'BEGIN'))
        if opt != None:
            config_file.change_option('Server', opt, '"{}"'.format(inp_str))
        ea_start(delay=15)
        time_gui_closed = time.time()
        logger.info('gui closed now.')
        ea_close()
        time_process_ended = time.time()
        logger.info('process is ended now.')
        time_result = time_process_ended - time_gui_closed
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
        finally:
            logger.critical('Seconds to restart EA is {}'.format(time_result))

# server test
    def test_config_server(self):
        right_server = [
                '10.144.10.217:9443/qm',
                ]
        wrong_server = [
                'https://10.145.10.217:9443/qm',
                ]
        for ser in wrong_server:
            test_passed = self.restart_time_test('server address', ser, expect_result=False)
        for ser in right_server:
            test_passed = self.restart_time_test('server', ser)

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
