from pynput import mouse

global last_x
global last_y
last_x = -99999
last_y = -99999

def on_click(x, y, button, pressed):
    """
    Callback function for mouse click events.
    Args:
        x (int): X-coordinate of the mouse pointer.
        y (int): Y-coordinate of the mouse pointer.
        button (pynput.mouse.Button): The mouse button that was clicked.
        pressed (bool): True if the button was pressed, False if released.
    """
    
    global last_x
    global last_y
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
        if last_x != -99999:
            print(f"Distance from last click: ({last_x-x}, {last_y-y})")
        last_x = x
        last_y = y
    # To stop the listener, you can return False or raise StopException
    # if button == mouse.Button.right:
    #     return False

# Create and start the listener
with mouse.Listener(on_click=on_click) as listener:
    listener.join()


# right click manually
# move -52, -264
# control c
# second icon 1138, 1055
# control v 
# enter
# first icon 1093, 1057