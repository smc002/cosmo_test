import unittest, time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, os.path, sys
import win32process, win32event, win32api, win32con, win32com.client
import logging
from removeall import removeall

def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)
        return callHelper
    return repeatHelper

class COSMO_test_case_1(unittest.TestCase):

    def setUp(self):
        ea_path = r'C:\Program Files (x86)\National Instruments\Test Integration Adapter 1.0'
        ea_name = 'Test Integration Adapter.exe'
        handle = win32process.CreateProcess(
            os.path.join(ea_path, ea_name),
            '', None, None, 0,
            win32process.CREATE_NO_WINDOW,
            None,
            ea_path,
            win32process.STARTUPINFO())
        #self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(10)

    #@repeat(100)
    def test_normal_test(self):
        log = logging.getLogger("COSMO.normal")
        self.driver = webdriver.Firefox()
        Failed = False
        try:
            self.driver.implicitly_wait(10)     
            self.driver.get("https://10.144.10.217:9443/qm/") # Load page
            elem = self.driver.find_element_by_name("j_username")
            elem.send_keys("test")        
            elem = self.driver.find_element_by_name("j_password") # Find the query box
            elem.send_keys("test" + Keys.ENTER)
            wait = WebDriverWait(self.driver, 20)
            elem = wait.until(EC.presence_of_element_located((By.ID,"jazz_ui_toolbar_Button_1")))
            self.driver.get("https://10.144.10.217:9443/qm/web/console/QM%20Test%20Project#action=com.ibm.rqm.planning.home.actionDispatcher&subAction=viewTestCase&id=43") # Load page      
            elem = wait.until(EC.presence_of_element_located((By.ID,"widget_com_ibm_asq_common_web_ui_internal_widgets_layout_ASQValidateTextBox_0")))
            elem = self.driver.find_element_by_css_selector('div.execute-icon-image.button-img')
            elem.click()
            elem = self.driver.find_element_by_css_selector('td.dijitReset.dijitMenuItemIconCell')
            elem.click()
            elem = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='actions-container']/span[3]/span[@class='button-div'][1]/button")))
            elem.click()
        except:
            Failed = True
            log.warning('Browser Automation Failed!')
        else:
            log.info('So happy everything works fine here')
        finally:
            self.driver.close()
        self.assertFalse(Failed, 'Browser Automation Failed!')

    def tearDown(self):
        pass
        #self.driver.close()

if __name__ == "__main__":
    cnt = 0
    logging_file = os.path.join(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'), 'normal_test.log')
    print("Logging to", logging_file)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        filename = logging_file,
        filemode = 'w',
        )
    log = logging.getLogger("COSMO.normal")
    while True:
        cnt += 1
        log.info("Normal Test No.{} begin.".format(cnt))
        try:
            unittest.main(verbosity=2, exit=False)
        except:
            log.error("An unexpected exception is detected.")
        if cnt%100 == 0:
            time.sleep(2)  #delete temp file too hurry might prevent firefox from closing
            removeall(r'C:\Users\msun\AppData\Local\temp')  #the files here could be too large, if running for hours
    
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
