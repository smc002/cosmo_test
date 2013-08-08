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

    @repeat(10)
    def test_normal_test(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        
        browser = self.driver
        browser.get("https://10.144.10.217:9443/qm/") # Load page
        elem = browser.find_element_by_name("j_username")
        elem.send_keys("test")        
        elem = browser.find_element_by_name("j_password") # Find the query box
        elem.send_keys("test" + Keys.ENTER)
        time.sleep(2)
        browser.get("https://10.144.10.217:9443/qm/web/console/QM%20Test%20Project#action=com.ibm.rqm.planning.home.actionDispatcher&subAction=viewTestCase&id=43") # Load page      
        wait = WebDriverWait(browser, 20)
        elem = wait.until(EC.presence_of_element_located((By.ID,"widget_com_ibm_asq_common_web_ui_internal_widgets_layout_ASQValidateTextBox_0")))
        elem = browser.find_element_by_css_selector('div.execute-icon-image.button-img')
        elem.click()
        elem = browser.find_element_by_css_selector('td.dijitReset.dijitMenuItemIconCell')
        elem.click()
        elem = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='actions-container']/span[3]/span[@class='button-div'][1]/button")))
        elem.click()
            
        
        self.driver.close()      

    def tearDown(self):
        pass
        #self.driver.close()

if __name__ == "__main__":
    suc_cnt = 0
    logging_file = os.path.join(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'), 'normal_test.log')
    print("Logging to", logging_file)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        filename = logging_file,
        filemode = 'w',
        )
    
    while 1:
        try:
            unittest.main(verbosity=2,exit=False)
        except:
            print("An exception is detected.")
            logging.warning("An exception is detected.")
            continue
        else:
            suc_cnt += 1
            print("Test {} successed.".format(suc_cnt))
            logging.info("Test {} successed.".format(suc_cnt))
