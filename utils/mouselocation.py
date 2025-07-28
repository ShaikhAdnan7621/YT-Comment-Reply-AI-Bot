import pyautogui
import pynput
from pynput import mouse

# Get Screen Width and Height
screen_width, screen_height = pyautogui.size()
print(f"Screen Width: {screen_width}")
print(f"Screen Height: {screen_height}")

# Function to capture mouse click position
def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at X={x}, Y={y}")

# Start listening to mouse clicks
print("Listening... Click anywhere to get coordinates. Press CTRL+C to stop.")


with mouse.Listener(on_click=on_click) as listener:
    listener.join()
