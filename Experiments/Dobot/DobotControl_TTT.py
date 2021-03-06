import threading
import DobotDll.DobotDllType as dType
import random
from pynput import keyboard
from pynput.keyboard import KeyCode

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 172, -120, 50, 0, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dType.SetPTPJumpParams(api, 10, 100, isQueued = 1)

    #Async Home
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    #Async PTP Motion
    #(default DobotControl action)
    #for i in range(0, 6):
    #    if i % 2 == 0:
    #        offset = 50
    #    else:
    #        offset = -50
    #    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 200 + offset, offset, offset, offset, isQueued = 1)[0]


    #rough estimates of the Game Board Corner Coordinates based on 4.5 inches away from dobot side
    xMax = 308
    xMin = 195
    yArr = [56.86, -56.93, -58.09, 54.73]
    zCoor = -59
    _OS = 12 #number of divisions per side of GB to find offset for 'X'
    
    #Calculating/storing x-values
    xArr = [xMax, 0, 0, xMin]
    xDiff = xMax - xMin
    xStep = xDiff / 3
    xOS = xDiff / _OS #for the markings of the x-offset from each gridline
    xTemp = xMax - xStep
    for x in range(1, 4):
        xArr[x] = xTemp
        xTemp -= xStep
    
    #Recording each y-coord vertex(16) in a 2DList
    y2DArr = [ [56.86, 0, 0, -56.93], [0, 0, 0, 0], [0, 0, 0, 0], [54.73, 0, 0, -58.09] ]
    
    #A->D and B->C y-values
    for i in range(0, 2):
        if i == 0:
            first = yArr[0]
            last = yArr[3]
        if i == 1:
            first = yArr[1]
            last = yArr[2]
        yDiff = first - last
        yStep = yDiff / 3
        yTemp = first - yStep
        for x in range(1, 3):
            if i == 0:
                y2DArr[x][0] = yTemp
            if i == 1:
                y2DArr[x][3] = yTemp
            yTemp -= yStep

    #Fills out the interior of the board, by each x-level
    yOS = [0, 0, 0, 0] #for the markings of the y-offset from each gridline
    for x in range(0, 4):
        yfirst = y2DArr[x][0]
        yDiff = yfirst - y2DArr[x][3]
        yStep = yDiff / 3
        yOS[x] = yDiff / _OS
        yTemp = yfirst - yStep
        for y in range(1, 4):
            y2DArr[x][y] = yTemp
            yTemp -= yStep
            
    #Same coordinates as Dobot home
    def goHome():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 172, -120, 50, 0, isQueued = 1)[0]

    #Physical instructions to create an 'X' in each individual cell
    def draw02():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][0] - yOS[0], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][1] + yOS[0], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][1] + yOS[0], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][0] - yOS[0], zCoor, 0, isQueued = 1)[0]
        goHome()

    def draw12():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][1] - yOS[0], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][2] + yOS[0], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][2] + yOS[0], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][1] - yOS[0], zCoor, 0, isQueued = 1)[0]
        goHome()

    def draw22():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][2] - yOS[0], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][3] + yOS[0], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][3] + yOS[0], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][2] - yOS[0], zCoor, 0, isQueued = 1)[0]
        goHome()

    def draw01():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][0] - yOS[1], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][1] + yOS[1], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][1] + yOS[1], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][0] - yOS[1], zCoor, 0, isQueued = 1)[0]
        goHome()

    def draw11():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][1] - yOS[1], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][2] + yOS[1], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][2] + yOS[1], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][1] - yOS[1], zCoor, 0, isQueued = 1)[0]
        goHome()

    def draw21():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][2] - yOS[1], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][3] + yOS[1], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][3] + yOS[1], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][2] - yOS[1], zCoor, 0, isQueued = 1)[0]
        goHome()

    def draw00():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][0] - yOS[2], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][1] + yOS[2], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][1] + yOS[2], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][0] - yOS[2], zCoor, 0, isQueued = 1)[0]
        goHome()

    def draw10():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][1] - yOS[2], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][2] + yOS[2], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][2] + yOS[2], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][1] - yOS[2], zCoor, 0, isQueued = 1)[0]
        goHome()

    def draw20():
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][2] - yOS[2], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][3] + yOS[2], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][3] + yOS[2], zCoor, 0, isQueued = 1)[0]
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][2] - yOS[2], zCoor, 0, isQueued = 1)[0]
        goHome()

    #Code to setup keyboard input for key(event)-binding
    #def on_press(key):
    #    if(key == KeyCode.from_char('q')):
    #       draw00()
    #    elif(key == KeyCode.from_char('w')):
    #       draw01()
    #    elif(key == KeyCode.from_char('e')):
    #       draw02()
    #    elif(key == KeyCode.from_char('a')):
    #       draw10()
    #    elif(key == KeyCode.from_char('s')):
    #       draw11()
    #    elif(key == KeyCode.from_char('d')):
    #       draw12()
    #    elif(key == KeyCode.from_char('z')):
    #       draw20()
    #    elif(key == KeyCode.from_char('x')):
    #       draw21()
    #    elif(key == KeyCode.from_char('c')):
    #       draw22()
        

    #def on_release(key):
    #    if key == keyboard.Key.esc:
    #       return False #Triggers Listener to stop listening

    #with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #       listener.join()

    #Start game code for TTT
    def drawMove(x, y):
        if(x == 0 and y == 0):
            draw00()
        elif(x == 0 and y == 1):
            draw01()
        elif(x == 0 and y == 2):
            draw02()
        elif(x == 1 and y == 0):
            draw10()
        elif(x == 1 and y == 1):
            draw11()
        elif(x == 1 and y == 2):
            draw12()
        elif(x == 2 and y == 3):
            draw20()
        elif(x == 2 and y == 3):
            draw21()
        elif(x == 2 and y == 3):
            draw22()


    #Plot lastIndex for every point for testing
    #for x in range(0, 4):
    #    print(xArr[x])
    #    for y in range(0, 4):
    #        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[x], y2DArr[x][y], zCoor, 0, isQueued = 1)[0]
    #        print(y2DArr[x][y])

    #Draws an 'X' in each grid space, uses offset value
    #Moves from UL to BR, jumps to UR, then moves from UR to BL
    #for x in range(0, 3):
    #    for y in range(0, 3):
    #        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[x] - xOS, y2DArr[x][y] - yOS[x], zCoor, 0, isQueued = 1)[0]
    #        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[x + 1] + xOS, y2DArr[x + 1][y + 1] + yOS[x], zCoor, 0, isQueued = 1)[0]
    #        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[x] - xOS, y2DArr[x][y + 1] + yOS[x], zCoor, 0, isQueued = 1)[0]
    #        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[x + 1] + xOS, y2DArr[x + 1][y] - yOS[x], zCoor, 0, isQueued = 1)[0]


    #lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xMax, yArr[0], zCoor, 0, isQueued = 1)[0] #A coords
    #lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xMax, yArr[1], zCoor, 0, isQueued = 1)[0] #B coords
    #lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xMin, yArr[2], zCoor, 0, isQueued = 1)[0] #C coords
    #lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xMin, yArr[3], zCoor, 0, isQueued = 1)[0] #D coords

    
    
    #Start to Execute Command Queued
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)

    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)

#Disconnect Dobot
dType.DisconnectDobot(api)
