# first is browser, second is code

# requires pip install pynput and opencv-python
# If pip is not recognized, but python is installed, probably just need to add the python Scripts folder to path
import time
import threading
from pynput.mouse import Button, Controller, Listener
import keyboard
import pyperclip
#import ImageGrab
#import opencv
import cv2
import numpy as np

from pynput.keyboard import KeyCode, Key #, ListenerListener
    
import pyautogui
import random




# seconds. Setting to 0 may crash things
delay = 4/10
button = Button.left
is_going = False;
start_stop_key = KeyCode(char='n')#Key.space
stop_key = KeyCode(char='m')
click_twice_key = Button.right
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
  
    #def start_clicking(self):
    #    self.running = True
  
    def stop_clicking(self):
        self.running = False
    def click_twice(self):
        self.remaining = 1
    def click_twice_stop(self):
        self.remaining = 0

    def test_offset(self):
        time.sleep(.05)
        #mouse.scroll(0, .01)
        # first number is the important one, x position of words
        im = pyautogui.screenshot(region=(1231, 237, 0, 400))
        
        image_np = np.array(im)
        print(image_np)
        #image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Save the image using OpenCV
        #cv2.imwrite(str(random.randint(0, 99999))+"_screenshot.png", image_cv)
        
    def exit(self):
        self.stop_clicking()
        self.click_twice_stop()
        self.program_running = False
        
# right click manually
# move -52, -264
# control c
# second icon 1138, 1055
# control v 
# enter
# first icon 1093, 1057
class CopySequence(Sequence):
    def run(self):
        while self.program_running:
            while self.remaining > 0:
                pos = mouse.position
                
                #time.sleep(1)
                time.sleep(.1)
                keyboard.press_and_release('q')
                #mouse.move(52, 264)
                #time.sleep(.2)
                #time.sleep(1)
                #mouse.click(Button.left)
                time.sleep(.3)
                #time.sleep(1)
                keyboard.press_and_release('control + c')
                time.sleep(.05)
                mouse.position = (1138, 1055)
                time.sleep(.05)
                #time.sleep(1)
                mouse.click(Button.left)
                
                pyperclip.copy(pyperclip.paste().replace("\n","") + "\n")
                
                time.sleep(.1)
                #time.sleep(1)
                mouse.position = (1731, 988)
                time.sleep(.05)
                #time.sleep(1)
                mouse.click(Button.left)
                time.sleep(.1)
                #time.sleep(1)
                keyboard.press_and_release('control + v')
                time.sleep(.05)
                #time.sleep(1)
                #keyboard.press_and_release('enter')
                #time.sleep(.1)
                #time.sleep(1)
                # back to webpage
                mouse.position = (1093, 1057)
                time.sleep(.05)
                #time.sleep(1)
                mouse.click(Button.left)
                #time.sleep(1)
                mouse.position = (pos)

                #.scroll(0, 5)
                self.remaining -=1

            time.sleep(0.1)
            
  
  
# instance of mouse controller is created
mouse = Controller()
click_thread = CopySequence(delay,button)#ClickMouse(delay, button)
click_thread.start()

def on_click(x, y, button, pressed):
    """
    Callback function for mouse click events.
    Args:
        x (int): X-coordinate of the mouse pointer.
        y (int): Y-coordinate of the mouse pointer.
        button (pynput.mouse.Button): The mouse button that was clicked.
        pressed (bool): True if the button was pressed, False if released.
    """
    
    if button == Button.right and not pressed:
        click_thread.click_twice()
    if button == Button.middle and pressed:
        click_thread.stop_clicking()
    if button == Button.left and pressed:
        click_thread.test_offset()
  
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
        
  
with Listener(on_click=on_click) as listener:
    listener.join()
  
#with Listener(on_press=on_press) as listener:
#    listener.join()