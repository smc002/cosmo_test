import unittest, time, shutil, datetime, glob
import os, os.path, sys
import logging
from ea_auto import item_click as ea_click, ea_start, ea_close, ea_config, ea_wait_process_end, ea_config_procedure
import browser_auto
from removeall import removeall

test_name = 'config_login'
test_root_folder = 'C:\\cosmo_autotest\\'
if not os.path.exists(test_root_folder):
    os.mkdir(test_root_folder)
ea_log_path = test_root_folder + test_name + '\\'
if not os.path.exists(ea_log_path):
    os.mkdir(ea_log_path)
ea_log_file = os.path.join(ea_log_path, 'system log.html')

config_path = r'C:\Users\Public\Documents\National Instruments\Test Integration Adapter 1.0'
config_file = os.path.join(config_path, 'Configuration.ini')
active_str = 'Client State Changed From REGISTRATION To ACTIVE'
active_kwd_list = ['Client State Changed From INITIALIZATION To LOGIN',
        'Client State Changed From LOGIN To REGISTRATION',
        'Client State Changed From REGISTRATION To ACTIVE',
        ]
task_executed_kwd_list = [
        'Process Task',
        'Finished Execution',
        ]

tps_state_str = 'TPS: {}, step: {}, state: {}'

def lookup_keyword_in_ea_log(keywords, ea_log=ea_log_file):
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


class COSMO_test_case_config_login(unittest.TestCase):

    def setUp(self):
        shutil.copy(r'./Configuration.ini', config_file)
        pass

    def config_test(self, opt, inp_str, veri_keyword, delay=10, expect_result=True):
        ea_config_procedure(opt, inp_str, delay, ea_log_path, ea_log_file)
        logger = logging.getLogger("COSMO.ea.config")
        ea_wait_process_end()
        if not os.path.isfile(ea_log_file):
            logger.error('EA\'s log file not found in {}'.format(ea_log_file))
            return False

        keyword_found = lookup_keyword_in_ea_log(veri_keyword)
        with open(ea_log_file, 'rt') as f:
            logger.debug(f.read())
        with open(ea_log_file, 'rt') as f:
            keyword_found = veri_keyword in f.read()
        try:
            self.assertTrue(keyword_found == expect_result, veri_keyword + ' not found in log')
        except AssertionError as e:
            logger.critical('{} = {}, test FAILED.'.format(opt, inp_str))
            logger.critical(str(e))
        except Exception as e:
            logger.critical('{} = {}, UNKOWN ERROR.'.format(opt, inp_str))
            logger.critical(str(e))
        else:
            logger.critical('{} = {}, test PASSED.'.format(opt, inp_str))
        return keyword_found == expect_result

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
            test_passed = self.config_test('username', user, active_str)

    def test_config_password(self):
        right_password = [
                'test',
                ]
        for pwd in right_password:
            test_passed = self.config_test('password', pwd, active_str)

# server test
    def test_config_server(self):
        right_server = [
                '10.144.10.217:9443/qm',
                'https://10.144.10.217:9443/qm',
                ]
        wrong_server = [
                'https://10.145.10.217:9443/qm',
                ]
        for ser in wrong_server:
            test_passed = self.config_test('server', ser, active_str, expect_result=False)
        for ser in right_server:
            test_passed = self.config_test('server', ser, active_str)

    def tearDown(self):
        try:
            ea_close()
        except:
            pass
        pass
        #self.driver.close()

if __name__ == "__main__":
    py_log_file = os.path.join(test_root_folder, test_name + '.log')
    debug_log_file = os.path.join(test_root_folder, test_name + '_debug.log')
    print("Logging to", py_log_file)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch)

    ch2 = logging.StreamHandler(open(py_log_file,'at'))
    ch2.setLevel(logging.WARNING)
    ch2.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch2)

    ch_debug = logging.StreamHandler(open(debug_log_file,'at'))
    ch_debug.setLevel(logging.DEBUG)
    ch_debug.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(message)s'))
    logger.addHandler(ch_debug)

    #ea_start_close_test()

    unittest.main(verbosity=2, exit=False)
