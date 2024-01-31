#Imports stuff for code
from codrone_edu.drone import *
import multiprocessing
from pynput.keyboard import Key, Listener
import time


#Pairs the drone
bolRun = True
drone = Drone()
drone.pair()


#Method that runs a menu of functions
def RunFunctions():
   print("1: Detecting Colors")
   print("2: Move And Turn")
   print("3: Elevation Detection")
   strFunctionCheck = str(input("input number or numbers (separated by spaces): "))


#Globalizes the functions
   global bolDetect_color
   global bolKey_Listener
   global bolMoveAndTurn
   global bolElevationDetection


#Checks which function was selected
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


#Function that detects colors
def Detect_color():
   bolDetector = True
   with Listener(on_press=key_listener) as listener:
       while listener != 1:
           time.sleep(1)
           strColor = drone.get_colors()
           print(strColor)
           if strColor == "Yellow":
              print("yippee")




#Function that can land or stop the drone
def key_listener(key):
   if key == Key.space:
       drone.emergency_stop()
       global bolRun
       bolRun = False
       return 1
   if key == Key.tab:
       drone.land()
       quit()


#function that detects changes in elevation
def ElevationDetection():
#take off the drone
   drone.takeoff()
#gets the initial battery level and prints it
   battery = drone.get_battery()
   print("Battery: " + str(battery))
#allows time for stabilization after takeoff
   time.sleep(4)
#initialize variables for elevation tracking
   intTracker = 1
   initialE = drone.get_pos_z()
   currentE = initialE
#monitor the elevation until a significant change occurs
   while int(currentE) <= int(initialE) + 5 and int(currentE) >= int(initialE) - 5:
       time.sleep(1)
       currentE = drone.get_pos_z()
       print("Initial Elevation: " + str(int(initialE)))
       print("Current Elevation: " + str(int(currentE)))
#lands the drone when the loop exits
   drone.land()


#Function that moves and turns the drone
def MoveAndTurn():
#take off the drone
   drone.takeoff()
#gets the initial battery level and prints it
   battery = drone.get_battery()
   print("Battery: " + str(battery))
#allows time for stabilization before taking off
   time.sleep(2)
#user will enter number of turns before landing
   intUserChoice = input("Input number of times it turns before landing: ")
   if intUserChoice == str:
       intUserChoice = 0
#initialize variables for loop control and tracking
   intTracker = 1
   bolTest = True
#Main loop for moving and turning the drone
   while bolTest:
#checks if a wall is detected at a certain distance
       if drone.detect_wall(98):
#gets color data and prints it
           strColor = drone.get_color_data()
           print(strColor)
           drone.turn_left(90)
           print("wall detected")
#gets the front range distance and prints it
           distance = drone.get_front_range()
           print("DISTANCE: " + str(distance))
           print(battery)
#checks if the desired number of turns have been reached
           if intTracker == int(intUserChoice):
               bolTest = False
#increments the turn tracker
           intTracker = intTracker + 1


       drone.set_pitch(50)
       drone.move_forward(0.5)
#land the drone and exit
   drone.land()
   drone.close()
   global bolRun
   bolRun = False
   exit()


while bolRun:
   RunFunctions()
#sets up listeners for keyboard inputs
   with Listener(on_press=key_listener) as listener:
#checks and executes functions based on boolean flags
       if bolMoveAndTurn:
#starts separate process for moving and turning
           threadMoveTurn = multiprocessing.Process(target=MoveAndTurn())
           threadMoveTurn.start()
           threadMoveTurn.join()
       if bolDetect_color:
#starts separate process to detect color
           threadColor = multiprocessing.Process(target=Detect_color())
           threadColor.start()
           threadColor.join()
       if bolElevationDetection:
#starts separate process for elevation detection
           threadElevation = multiprocessing.Process(target=ElevationDetection())
           threadElevation.start()
           threadElevation.join()
       listener.join()
#emergency stop and exits
drone.emergency_stop()
drone.close()





