import time
import sys
import pyautogui
time.sleep(5)
pyautogui.PAUSE = 0.5
#Getting the System Arguments sent from OpenMind
args = sys.argv
V = float(args[1])
S = float(args[2])
O = float(args[3])

#Calculating Snap Coordinate Values
R1 = '520'
R2 = '150'
left_select  = str(180+(S/2)-V-O)
right_select = str(180-(S/2)+V-O)

#Calculating Input Positions
SnapCoord = pyautogui.getWindowsWithTitle("Coordinates")[0]
SnapWindow = [SnapCoord.left, SnapCoord.top]

RHO   = [SnapWindow[0]+75,SnapWindow[1]+160]
THETA = [SnapWindow[0]+180,SnapWindow[1]+160]
PHI   = [SnapWindow[0]+265,SnapWindow[1]+160]

apply  = [SnapWindow[0]+190,SnapWindow[1]+50]
Finish = [SnapWindow[0]+340,SnapWindow[1]+65]

#Pyautogui Sequence
## Select Centre Point
pyautogui.doubleClick(RHO[0],RHO[1])    #Double-Click on the RHO box
pyautogui.typewrite('0')                #Type zero into box  
pyautogui.typewrite(['tab'])            #Tab to Theta Box
pyautogui.typewrite('0')                #Type zero into box
pyautogui.typewrite(['tab'])            #Tab to PHI box
pyautogui.click(apply[0],apply[1])      #Click on apply to select coordinate
## Select Left Vertice
pyautogui.doubleClick(RHO[0],RHO[1])    #Double-Click on the RHO box
pyautogui.typewrite(R1)                 #Type R1 value into box  
pyautogui.typewrite(['tab'])            #Tab to Theta Box
pyautogui.typewrite(left_select)        #Type left select value into box
pyautogui.typewrite(['tab'])            #Tab to PHI box
pyautogui.click(apply[0],apply[1])      #Click on apply to select coordinate
## Select Right Vertice
pyautogui.doubleClick(RHO[0],RHO[1])    #Double-Click on the RHO box
pyautogui.typewrite(R2)                 #Type R2 value into box  
pyautogui.typewrite(['tab'])            #Tab to Theta Box
pyautogui.typewrite(right_select)       #Type right select value into box
pyautogui.typewrite(['tab'])            #Tab to PHI box
pyautogui.click(apply[0],apply[1])      #Click on apply to select coordinate
pyautogui.click(Finish[0],Finish[1])    #Click on apply and exit to complete selection

pyautogui.keyDown("alt")
pyautogui.press("i")
pyautogui.keyUp("alt")

pyautogui.press('del')
time.sleep(2)
