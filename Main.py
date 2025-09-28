# requires pip install pynput
# If pip is not recognized, but python is installed, probably just need to add the python Scripts folder to path
import time
import threading
from pynput.mouse import Button, Controller
import keyboard

from pynput.keyboard import Listener, KeyCode, Key

import pyautogui

# seconds. Setting to 0 may crash things
delay = 4/10
button = Button.left
is_going = False;
start_stop_key = KeyCode(char='n')#Key.space
stop_key = KeyCode(char='m')
click_twice_key = KeyCode(char='y')
test_key = KeyCode(char='z')



# I believe offset is only used in double click
offset = (-50,0)

# LOOK HERE OR ABOVE FOR CURRENT SETTINGS
print("Starting program! Currently set to click every ",delay," seconds.")
print("Current offset is:",offset)
print("Start toggle key is:",start_stop_key)
print("Exit/emergency stop key is:",str(stop_key)+". Escape also always works to cancel. (Assuming that isn't disabled.)")
print("Double click adjust once key is:",click_twice_key)
# threading.Thread is used 
# to control clicks mm


            
class Sequence(threading.Thread):

  # delay and button is passed in class 
  # to check execution of auto-clicker
    def __init__(self, delay, button):
        super(Sequence, self).__init__()
        #super().__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True
        self.remaining = 0;
  
    def start_clicking(self):
        self.running = True
  
    def stop_clicking(self):
        self.running = False
    def click_twice(self):
        self.remaining = 251
    def click_twice_stop(self):
        self.remaining = 0

    def test_offset(self):
        mouse.move(offset[0],offset[1])
        
    def exit(self):
        self.stop_clicking()
        self.click_twice_stop()
        self.program_running = False

class ClickMouse(Sequence):
    #def __init__(self, delay, button):
    #    super().__init__(delay, button)
    
    # method to check and run loop until 
    # it is true another loop will check 
    # if it is set to true or not, 
    # for mouse click it set to button 
    # and delay.
    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                if (self.delay != 0):
                    time.sleep(self.delay)
            while self.remaining > 0:
                # Currently: clicks, waits, clicks, moves by offset, clicks, waits, moves back, waits. NOT GENERAL SOLUTION but easy to adjust
                mouse.click(self.button)
                time.sleep(self.delay)
                mouse.click(self.button)
                time.sleep(0.1)

                mouse.move(offset[0],offset[1])
                mouse.click(self.button)
                time.sleep(0.1)
                mouse.move(-offset[0],-offset[1])

            time.sleep(0.1)
            
class PressSequence(Sequence):
    def run(self):
        while self.program_running:
            while self.remaining > 0:
                # Currently: clicks, waits, clicks, moves by offset, clicks, waits, moves back, waits. NOT GENERAL SOLUTION but easy to adjust
                keyboard.press_and_release('control + f')
                time.sleep(.4)
                keyboard.press_and_release('page down')
                time.sleep(.1)
                self.remaining -=1

            time.sleep(0.1)
            

class MultiDeleteSequence(Sequence):
    def run(self):
        while self.program_running:
            while self.remaining > 0:
                mouse.click(self.button)
                for i in range(9): #------------------
                    time.sleep(.1)
                    keyboard.press_and_release('delete')
                time.sleep(.1)
                keyboard.press_and_release('page down')
                self.remaining -=1

            time.sleep(0.1)
  
  
class ClickSequence(Sequence):
    def run(self):
        while self.program_running:
            while self.remaining > 0:
                mouse.click(self.button)
                time.sleep(.1)
                keyboard.press_and_release('page down')
                self.remaining -=1

            time.sleep(0.1)


class ClickDeleteSequence(Sequence):
    def run(self):
        while self.program_running:
            while self.remaining > 0:
                mouse.click(self.button)
                time.sleep(.05)
                keyboard.press_and_release('delete')
                time.sleep(.05)
                keyboard.press_and_release('page down')
                self.remaining -=1

            time.sleep(0.05)

class DeleteSequence(Sequence):
    def run(self):
        while self.program_running:
            while self.remaining > 0:
                keyboard.press_and_release('delete')
                time.sleep(.05)
                keyboard.press_and_release('page down')
                self.remaining -=1

            time.sleep(0.05)
  
  
# instance of mouse controller is created
mouse = Controller()
click_thread = MultiDeleteSequence(delay,button)#ClickMouse(delay, button)
click_thread.start()

  
# on_press method takes 
# key as argument
def on_press(key):
    
  # start_stop_key will stop clicking 
  # if running flag is set to true
    if key == start_stop_key:
        if click_thread.running:
            print("Deactivating.")
            click_thread.stop_clicking()
        else:
            print("Activating.")
            click_thread.start_clicking()
    if key == click_twice_key:
        if click_thread.remaining == 0:
            print("Starting clicking twice loop.")
            click_thread.click_twice()
        else:
            print("Ending clicking twice loop.")
            click_thread.click_twice_stop()
    if key == test_key:
        print("Test offset.")
        click_thread.test_offset()
              
    # here exit method is called and when 
    # key is pressed it terminates auto clicker
    elif key == stop_key or key == Key.esc:
        print("Turning off.")
        click_thread.exit()
        listener.stop()
  
  
with Listener(on_press=on_press) as listener:
    listener.join()
    
    
    
    