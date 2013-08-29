import os, os.path, sys
import win32process, win32event, win32api, win32con, win32com.client
import time

base_point = [1280,0]
TestStand_compatible_NO = [2426, 680]
EA_Connect = [2450, 630]
TestStand_login = [2189, 579]
#wait for start; wait for EA user interface; wait for TestStand login
wait_time_list1 = [1, 8, 1]

chrome_addr = [140, 100]
qm_run_menu = [822, 306]
qm_run = [847, 330]
qm_OK = [800, 815]
wait_time_list2 = [2, 20, 1]

# Mouse Click function
def mouse_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
def click_and_wait(points, wait_time_list):
    for i in range(0, len(points)):
        points[i][0] -= base_point[0]
        mouse_click(points[i][0], points[i][1])
        time.sleep(wait_time_list[i])
        
ea_path = r'C:\Program Files (x86)\National Instruments\Test Integration Adapter 1.0'
ea_name = 'Test Integration Adapter.exe'
handle = win32process.CreateProcess(
    os.path.join(ea_path, ea_name),
    '', None, None, 0,
    win32process.CREATE_NO_WINDOW,
    None,
    ea_path,
    win32process.STARTUPINFO())
time.sleep(2)
points = [TestStand_compatible_NO, EA_Connect, TestStand_login]
click_and_wait(points, wait_time_list1)
click_and_wait([chrome_addr], [1])
wsh = win32com.client.Dispatch("WScript.Shell")
wsh.SendKeys(r"https://10.144.10.217:9443/qm/web/console/QM Test Project#action=com.ibm.rqm.planning.home.actionDispatcher&subAction=viewTestCase&id=43")
wsh.SendKeys("{ENTER}")
time.sleep(10)
click_and_wait([qm_run_menu, qm_run, qm_OK], wait_time_list2)
