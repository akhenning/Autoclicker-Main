# Just constantly takes screenshots while running. Overwrites old ones.
import time
import pyautogui
import threading

file_name = "mizuki"
delay_sec = .04
count = 0

def write(screenshot):
    screenshot.save("screenshots/"+(file_name+str(count))+".png")

print("Starting")
while True:
    start = time.time()
    screenshot = pyautogui.screenshot(region=(800,120,300,290))
    x = threading.Thread(target=write, args=(screenshot,))
    x.start()
    count+=1
    dur = time.time() - start
    if (dur > delay_sec):
        dur = 0
    #print("took",(dur),"secs")
    time.sleep(delay_sec-dur)
    