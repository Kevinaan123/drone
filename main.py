from codrone_edu.drone import *
import multiprocessing
from pynput.keyboard import Key, Listener
import time
bolRun = True
drone = Drone()
drone.pair()
def RunFunctions():
    print("1: Detecting Colors")
    print("2: Move And Turn")
    print("3: Elevation Detection")
    print("4: Environment Detection")
    print("5: Drone Flip")
    print("6: Set Path")
    strFunctionCheck = str(input("input number or numbers (separated by spaces): "))
    global bolDetect_color
    global bolKey_Listener
    global bolMoveAndTurn
    global bolElevationDetection
    global bolEnvironmentDetection
    global bolDroneFlip
    global bolSetPath
    if "1" in strFunctionCheck:
        bolDetect_color = True
    else:
        bolDetect_color = False
    if "2" in strFunctionCheck:
        bolMoveAndTurn = True
    else:
        bolMoveAndTurn = False
    if "3" in strFunctionCheck:
        bolElevationDetection = True
    else:
        bolElevationDetection = False
    if "4" in strFunctionCheck:
        bolEnvironmentDetection = True
    else:
        bolEnvironmentDetection = False
    if "5" in strFunctionCheck:
        bolDroneFlip = True
    else:
        bolDroneFlip = False
    if "6" in strFunctionCheck:
        bolSetPath = True
    else:
        bolSetPath = False
def Detect_color():
    bolDetector = True
    with Listener(on_press=key_listener) as listener:
        while listener != 1:
            time.sleep(1)
            strColor = drone.get_colors()
            print(strColor)
            if strColor == "Yellow":
               print("yippee")

def SetPath():
    bolNotSet = True
    i = 0
    listDirection = []
    listDistance = []
    listFlip = []
    while bolNotSet:
        print("Left " + "\n" + "Right" + "\n" + "Forward" + "\n" + "Backward" + "\n")
        strDirection = input("Choose Direction: ")
        intDistance = int(input("Input Distance (cm): "))
        listDirection.append(strDirection)
        listDistance.append(intDistance)
        i = i + 1
        if str(input("Ready to run? If so input yes: ")) == "true":
            bolNotSet = False
        if str(input("Flip?")) == "Yes" or "yes":
            listFlip[i] = True
    print("\n" + "Running")
    j = 0
    drone.takeoff()
    while j <= i:
        if listDirection[j] == "left" or listDirection[j] == "Left":
            drone.move_left(listDistance[j])
        if listDirection[j] == "right" or listDirection[j] == "Right":
            drone.move_right(listDistance[j])
        if listDirection[j] == "forward" or listDirection[j] == "Forward":
            drone.move_forward(listDistance[j])
        if listDirection[j] == "backward" or listDirection[j] == "Backward":
            drone.move_backward(listDistance[j])
        if listFlip[j]:
            drone.flip()
        j = j + 1
    drone.land()
    drone.close()

def key_listener(key):
    if key == Key.space:
        drone.emergency_stop()
        global bolRun
        bolRun = False
        return 1
    if key == Key.tab:
        drone.land()
        quit()
def Flip():
    drone.flip()
def ElevationDetection():
    drone.takeoff()
    battery = drone.get_battery()
    print("Battery: " + str(battery))
    time.sleep(4)
    intTracker = 1
    initialE = drone.get_pos_z()
    currentE = initialE
    while int(currentE) <= int(initialE) + 5 and int(currentE) >= int(initialE) - 5:
        time.sleep(1)
        currentE = drone.get_pos_z()
        print("Initial Elevation: " + str(int(initialE)))
        print("Current Elevation: " + str(int(currentE)))
    drone.land()

def EnvironmentDetection():
    pressure = drone.get_pressure() # unit: Pascals
    temp = drone.get_temperature()  # unit: Celsius
    battery = drone.get_battery()   # unit: percentage
    print("Air Pressure: " + str(pressure) + " Pascals  ( " + str(pressure / 101325) + " atm )" + "\n"
          "Temperature: " + str(temp) + " Celsius  ( " + str(drone.get_temperature("F")) + " F )" + "\n"
          "Battery: " + str(battery) + "%")
def MoveAndTurn():
    drone.takeoff()
    battery = drone.get_battery()
    print("Battery: " + str(battery))
    time.sleep(2)
    intUserChoice = input("Input number of times it turns before landing: ")
    if intUserChoice == str:
        intUserChoice = 0
    intTracker = 1
    bolTest = True
    while bolTest:
        if drone.detect_wall(98):
            strColor = drone.get_color_data()
            print(strColor)
            drone.turn_left(90)
            print("wall detected")
            distance = drone.get_front_range()
            print("DISTANCE: " + str(distance))
            print(battery)
            if intTracker == int(intUserChoice):
                bolTest = False
            intTracker = intTracker + 1

        drone.set_pitch(50)
        drone.move_forward(0.5)
    drone.land()
    drone.close()
    global bolRun
    bolRun = False
    exit()

while bolRun:
    RunFunctions()
    with Listener(on_press=key_listener) as listener:
        if bolMoveAndTurn:
            threadMoveTurn = multiprocessing.Process(target=MoveAndTurn())
            threadMoveTurn.start()
            threadMoveTurn.join()
        if bolDetect_color:
            threadColor = multiprocessing.Process(target=Detect_color())
            threadColor.start()
            threadColor.join()
        if bolElevationDetection:
            threadElevation = multiprocessing.Process(target=ElevationDetection())
            threadElevation.start()
            threadElevation.join()
        if bolEnvironmentDetection:
            threadEnviro = multiprocessing.Process(target=EnvironmentDetection())
            threadEnviro.start()
            threadEnviro.join()
        if bolDroneFlip:
            threadDroneFlip = multiprocessing.Process(target=Flip())
            threadDroneFlip.start()
            threadDroneFlip.join()
        if bolSetPath:
            threadSetPath = multiprocessing.Process(target=SetPath())
            threadSetPath.start()
            threadSetPath.join()
        listener.join()
drone.emergency_stop()
drone.close()
