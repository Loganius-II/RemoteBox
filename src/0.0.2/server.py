
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
PORT = HOST_PORT_SET if HOST_PORT_SET != "auto" else 5900 #typical VNC port

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
            func(*args)
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
    while True:
        try:
            coords = server.client.recv(1024).decode()
            coords = coords.split()
            intention = coords[0]
            x = int(coords[1])
            y = int(coords[2])
            # x = x * (1680 / 800) # 4096
            # y = y * (1050 / 600) # 2160
            
            # Detect pixel resolution here
            resx, resy = get_res()

            x = x * (resx / 800)
            y = y * (resy / 600)
            x = math.ceil(x)
            y = math.ceil(y)

            if intention == 'coord':
                #click(int(x), int(y))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)

            elif intention == 'mouseup':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

            elif intention == 'mousemove':
                win32api.SetCursorPos((x,y))        
        except:
            continue
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
