
import DobotDll.DobotDllType as dType

isQueued = 0
# Same coordinates as Dobot home
def goHome():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 172, -120, 50, 0, isQueued)


# Physical instructions to create an 'X' in each individual cell
def draw02():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][0] - yOS[0], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][1] + yOS[0], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][1] + yOS[0], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][0] - yOS[0], zCoor, 0, isQueued)

    goHome()


def draw12():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][1] - yOS[0], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][2] + yOS[0], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][2] + yOS[0], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][1] - yOS[0], zCoor, 0, isQueued)

    goHome()


def draw22():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][2] - yOS[0], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][3] + yOS[0], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[0] - xOS, y2DArr[0][3] + yOS[0], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[1] + xOS, y2DArr[1][2] - yOS[0], zCoor, 0, isQueued)
    goHome()


def draw01():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][0] - yOS[1], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][1] + yOS[1], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][1] + yOS[1], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][0] - yOS[1], zCoor, 0, isQueued)
    goHome()


def draw11():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][1] - yOS[1], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][2] + yOS[1], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][2] + yOS[1], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][1] - yOS[1], zCoor, 0, isQueued)
    goHome()


def draw21():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][2] - yOS[1], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][3] + yOS[1], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[1] - xOS, y2DArr[1][3] + yOS[1], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[2] + xOS, y2DArr[2][2] - yOS[1], zCoor, 0, isQueued)
    goHome()


def draw00():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][0] - yOS[2], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][1] + yOS[2], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][1] + yOS[2], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][0] - yOS[2], zCoor, 0, isQueued)
    goHome()


def draw10():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][1] - yOS[2], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][2] + yOS[2], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][2] + yOS[2], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][1] - yOS[2], zCoor, 0, isQueued)
    goHome()


def draw20():

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][2] - yOS[2], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][3] + yOS[2], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, xArr[2] - xOS, y2DArr[2][3] + yOS[2], zCoor, 0, isQueued)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xArr[3] + xOS, y2DArr[3][2] - yOS[2], zCoor, 0, isQueued)
    goHome()


# Start game code for TTT
def drawMove(x, y):
    if x == 0 and y == 0:
        draw00()
    elif x == 0 and y == 1:
        draw01()
    elif x == 0 and y == 2:
        draw02()
    elif x == 1 and y == 0:
        draw10()
    elif x == 1 and y == 1:
        draw11()
    elif x == 1 and y == 2:
        draw12()
    elif x == 2 and y == 0:
        draw20()
    elif x == 2 and y == 1:
        draw21()
    elif x == 2 and y == 2:
        draw22()


CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

# Load Dll
api = dType.load()

# Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:", CON_STR[state])

if state == dType.DobotConnect.DobotConnect_NoError:

    # Clean Command Queued
    dType.SetQueuedCmdClear(api)

    # Async Motion Params Setting
    dType.SetHOMEParams(api, 172, -120, 50, 0, isQueued=1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued=1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued=1)
    dType.SetPTPJumpParams(api, 10, 100, isQueued=1)

    # Async Home
    dType.SetHOMECmd(api, temp=0, isQueued=1)

    # rough estimates of the Game Board Corner Coordinates based on 4.5 inches away from dobot side
    xMax = 308
    xMin = 195
    yArr = [56.86, -56.93, -58.09, 54.73]
    zCoor = -59
    _OS = 12  # number of divisions per side of GB to find offset for 'X'

    # Calculating/storing x-values
    xArr = [xMax, 0, 0, xMin]
    xDiff = xMax - xMin
    xStep = xDiff / 3
    xOS = xDiff / _OS  # for the markings of the x-offset from each gridline
    xTemp = xMax - xStep
    for x in range(1, 4):
        xArr[x] = xTemp
        xTemp -= xStep

    # Recording each y-coord vertex(16) in a 2DList
    y2DArr = [[56.86, 0, 0, -56.93], [0, 0, 0, 0], [0, 0, 0, 0], [54.73, 0, 0, -58.09]]

    # A->D and B->C y-values
    for i in range(0, 2):
        first = None
        last = None
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

    # Fills out the interior of the board, by each x-level
    yOS = [0, 0, 0, 0]  # for the markings of the y-offset from each gridline
    for x in range(0, 4):
        yfirst = y2DArr[x][0]
        yDiff = yfirst - y2DArr[x][3]
        yStep = yDiff / 3
        yOS[x] = yDiff / _OS
        yTemp = yfirst - yStep
        for y in range(1, 4):
            y2DArr[x][y] = yTemp
            yTemp -= yStep

# Disconnect Dobot
dType.DisconnectDobot(api)
