from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def try_find_elem(find_func, clue):
    i = 0
    while 1:
        try:
            elem = find_func(clue)
        except:
            time.sleep(1)
            i = i+1
            if i>10:
                raise Exception("Time out to find an element. Clue is " + clue)
        else:
            print("Found! i is " + str(i) + ", the clue is " + clue)
            break
    return elem
    

browser = webdriver.Firefox() # Get local session of firefox
browser.implicitly_wait(10)
browser.get("https://10.144.10.217:9443/qm/") # Load page
elem = browser.find_element_by_name("j_username")
elem.send_keys("test")        
elem = browser.find_element_by_name("j_password") # Find the query box
elem.send_keys("test" + Keys.ENTER)
time.sleep(1)
browser.get("https://10.144.10.217:9443/qm/web/console/QM%20Test%20Project#action=com.ibm.rqm.planning.home.actionDispatcher&subAction=viewTestCase&id=43") # Load page
time.sleep(3)
elem = browser.find_element_by_css_selector('div.execute-icon-image.button-img')
elem.click()
elem = browser.find_element_by_css_selector('td.dijitReset.dijitMenuItemIconCell')
elem.click()

wait = WebDriverWait(browser, 10)
elem = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='actions-container']/span[3]/span[@class='button-div'][1]/button")))
#elem = try_find_elem(browser.find_element_by_xpath,"//div[@class='actions-container']/span[3]/span[@class='button-div'][1]/button")
elem.click()
browser.close()
exit()
#time.sleep(0.2) # Let the page load, will be added to the API
#try:
#    browser.find_element_by_xpath("//a[contains(@href,'http://seleniumhq.org')]")
#except NoSuchElementException:
#    assert 0, "can't find seleniumhq"
#browser.close()

