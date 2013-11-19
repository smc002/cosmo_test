import unittest, time, logging, ctypes
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, os.path, sys
from constant_utility import removeall
import ea_auto
from ts_auto import ts_test_case_1

def run_normal_test():
    logger = logging.getLogger("COSMO.browser")
# Selenium can't deployed by cx_freeze, so failed this part.
    logger.critical('Browser Automation Failed!')
    return False
    for i in range(1,10):
        try:
            driver = webdriver.Firefox()
            Failed = False
            logger.critical('Browser Automation begin.')
            driver.implicitly_wait(30)     
            driver.get("https://10.144.10.217:9443/qm/") # Load page
            elem = driver.find_element_by_name("j_username")
            elem.send_keys("test")        
            elem = driver.find_element_by_name("j_password") # Find the query box
            elem.send_keys("test" + Keys.ENTER)
            wait = WebDriverWait(driver, 30)
            elem = wait.until(EC.presence_of_element_located((By.ID,"jazz_ui_toolbar_Button_1")))
            # driver.get("https://10.144.10.217:9443/qm/web/console/QM%20Test%20Project#action=com.ibm.rqm.planning.home.actionDispatcher&subAction=viewTestCase&id=43") # Load page      
            driver.get("https://10.144.10.217:9443/qm/web/console/autotest%20project#action=com.ibm.rqm.planning.home.actionDispatcher&subAction=viewTestCase&id=81") # Load page      
            elem = wait.until(EC.presence_of_element_located((By.ID,"widget_com_ibm_asq_common_web_ui_internal_widgets_layout_ASQValidateTextBox_0")))
            elem = driver.find_element_by_css_selector('div.execute-icon-image.button-img')
            elem.click()
            elem = driver.find_element_by_css_selector('td.dijitReset.dijitMenuItemIconCell')
            elem.click()
            elem = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='actions-container']/span[3]/span[@class='button-div'][1]/button")))
            elem.click()
        except:
            Failed = True
            logger.critical('Browser Automation Failed!')
        else:
            logger.critical('Browser Automation Succeed!')
            Failed = False
            break
        finally:
            driver.close()
    ts_test_case_1() # handle the click operation needed for C:\Users\Public\Documents\National Instruments\TestStand 2012\Examples\Demo\C\computer.seq
    return not Failed
    # assert(Failed, 'Browser Automation Failed!')

if __name__ == "__main__":
    ea_auto.ea_start()
    run_normal_test()
