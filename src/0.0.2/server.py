
import socket
import pyautogui
import pygame
import threading
from time import sleep
import win32api, win32con
import math
import json
from typing import Callable


try:
    # Attempt to access settings
    with open('Settings.json', 'r') as s:
        settings = json.load(s)
except:
    # If there is no settings.json load defaults
    settings = {
        
    "host_addr": "auto",
    "port": {
        "port": "auto",
        "port_fwd": False
    
}
    }
    print('[INFO] "Settings.json" could not be found, default settings applied')

HOST_ADDR_SET = settings["host_addr"]
HOST_PORT_SET = settings["port"]["port"]
# Port forwarding has not been tested and will not be thorooughly implemented in this version

# Setting the IP the server is run on
SERVER = HOST_ADDR_SET if HOST_ADDR_SET != "auto" else socket.gethostbyname(socket.gethostname())
# Setting port
PORT = int(HOST_PORT_SET) if HOST_PORT_SET != "auto" else 5900 #typical VNC port

print(f"[INFO] {SERVER}:{PORT}")

class Server(socket.socket):
    def __init__(self, SERVER, PORT) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((SERVER, PORT))
        self.listen(1)
        print(f"Listening for connections on {SERVER}:{PORT}...")
        self.client, self.addr = self.accept()
        print(f'Connection accepted from {self.addr}!')
        self.running = True

    def send_image(self, data: bytes) -> None:

        if not self.running:
            return

        try:
            self.client.sendall(len(data).to_bytes(4, 'big'))  # Send the length of the data first
            self.client.sendall(data)  # Send the actual image data
        except Exception as e:
            self.err_protocol("Data not able to be sent", e)

    def err_protocol(self, reason: str, err) -> None:
        print(reason)
        print(f"Error:\n{err}")
        self.kill()

    def kill(self) -> None:
        self.running = False
        self.client.close()
        print("Socket closed")
        del(self)
        
def error_handle(func: Callable) -> Callable:
    def wrapper(*args):
        try:
            return func(*args)
        except Exception as e:
            print("[ERROR] Exception occured because of the following:\n")
            print(e)
        
    return wrapper

@error_handle
def capture_screen() -> bytes:
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize((800, 600))  # Ensure the size matches the client display
    screenshot_rgb = screenshot.convert("RGB")  # Ensure the image is in RGB format
    return screenshot_rgb.tobytes()  # Convert the image to bytes

@error_handle
def click(x: str | float, y: str | float) -> None:
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

@error_handle
def get_res() -> tuple[int, int]:
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)



@error_handle
def check_and_click() -> None:
    global server
    
    # Get the server's screen resolution
    resx, resy = get_res()
    
    while True:
        try:
            coords = server.client.recv(1024).decode().split()
            intention = coords[0]

            if intention == 'coord':
                x = int(coords[1])
                y = int(coords[2])
                
                # Scale the absolute position to match the server's screen size
                x = math.ceil(x * (resx / 800))
                y = math.ceil(y * (resy / 600))
                
                # Simulate the click
                print(f"Mouse Down at {x}, {y}")
                win32api.SetCursorPos((x, y))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

            elif intention == 'mouseup':
                x = int(coords[1])
                y = int(coords[2])
                
                # Scale the absolute position to match the server's screen size
                x = math.ceil(x * (resx / 800))
                y = math.ceil(y * (resy / 600))
                
                print(f"Mouse Up at {x}, {y}")
                win32api.SetCursorPos((x, y))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

            elif intention == 'mousemove':
                delta_x = int(coords[1])
                delta_y = int(coords[2])
                x = int(coords[3])
                y = int(coords[4])
                # Scale the deltas proportionally
                scaled_delta_x = math.ceil(delta_x * (resx / 800))
                scaled_delta_y = math.ceil(delta_y * (resy / 600))
                scaled_x = math.ceil(x * (resx / 800))
                scaled_y = math.ceil(y * (resy / 600))
                win32api.SetCursorPos((scaled_x, scaled_y))
                # Apply the relative movement
                print(f"Moving mouse by delta: {scaled_delta_x}, {scaled_delta_y}")
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, scaled_delta_x, scaled_delta_y, 0, 0)

        except Exception as e:
            print(f"[ERROR] Exception occurred in check_and_click: {e}")
            continue


'''def check_and_click() -> None:
    global server
    # Declare previous_x and previous_y to track last mouse positions
    previous_x, previous_y = None, None
    
    while True:
        try:
            coords = server.client.recv(1024).decode()
            coords = coords.split()
            intention = coords[0]
            x = int(coords[1])
            y = int(coords[2])
            
            resx, resy = get_res()

            x = x * (resx / 800)
            y = y * (resy / 600)
            x = math.ceil(x)
            y = math.ceil(y)

            if intention == 'coord':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)

            elif intention == 'mouseup':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
                print("mouse is now up")

            elif intention == 'mousemove':
                # Calculate relative movement based on previous position
                if previous_x is not None and previous_y is not None:
                    delta_x = x - previous_x
                    delta_y = y - previous_y

                    # Simulate relative movement with mouse_event
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, delta_x, delta_y, 0, 0)

                # Update previous position
                previous_x, previous_y = x, y

        except Exception as e:
            print(f"[ERROR] Exception occurred in check_and_click: {e}")
            continue'''


'''        coords = coords.split()
        x = int(coords[1])
        y = int(coords[2])
        x = x * (4096 / 800)
        y = y * (2160 / 600)
        x = math.ceil(x)
        y = math.ceil(y)
        click(int(x), int(y))
    '''

@error_handle
def main():
    global server
    server = Server(SERVER, PORT)
    click_thread = threading.Thread(target=check_and_click)
    click_thread.start()
    while True:
        sleep(0.001)
        screen_bytes = capture_screen()

        server.send_image(screen_bytes)

if __name__ == '__main__':
    main()
