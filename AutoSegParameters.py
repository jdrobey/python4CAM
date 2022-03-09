import time
import pyautogui
import win32api,win32con

caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
if caps_status==0:
    pass
else:
    pyautogui.typewrite(['capslock'])
time.sleep(2.5)


SegParam = pyautogui.getWindowsWithTitle("Set segment parameters")[0]
left = (SegParam.left+SegParam.right)/2
right = SegParam.top+20
Shift_x = (SegParam.right-SegParam.left)/8
apply_x = SegParam.right - Shift_x
apply_y = SegParam.top + 50
pyautogui.click(left,right)
pyautogui.typewrite(['tab','tab'])
pyautogui.typewrite(['S'])
pyautogui.typewrite(['tab','tab'])
pyautogui.typewrite(['O'])
pyautogui.typewrite(['tab'])
pyautogui.click(apply_x,apply_y)
