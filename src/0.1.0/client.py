
import socket
import pygame
import io
from time import sleep
import keyboard

SERVER = '192.168.1.101'  # Your server's IP address
PORT = 6000

pygame.init()


key_mapping = {
    pygame.K_a: 'A',
    pygame.K_b: 'B',
    pygame.K_c: 'C',
    pygame.K_d: 'D',
    pygame.K_e: 'E',
    pygame.K_f: 'F',
    pygame.K_g: 'G',
    pygame.K_h: 'H',
    pygame.K_i: 'I',
    pygame.K_j: 'J',
    pygame.K_k: 'K',
    pygame.K_l: 'L',
    pygame.K_m: 'M',
    pygame.K_n: 'N',
    pygame.K_o: 'O',
    pygame.K_p: 'P',
    pygame.K_q: 'Q',
    pygame.K_r: 'R',
    pygame.K_s: 'S',
    pygame.K_t: 'T',
    pygame.K_u: 'U',
    pygame.K_v: 'V',
    pygame.K_w: 'W',
    pygame.K_x: 'X',
    pygame.K_y: 'Y',
    pygame.K_z: 'Z',
    pygame.K_0: '0',
    pygame.K_1: '1',
    pygame.K_2: '2',
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_5: '5',
    pygame.K_6: '6',
    pygame.K_7: '7',
    pygame.K_8: '8',
    pygame.K_9: '9',
    pygame.K_SPACE: 'Space',
    pygame.K_RETURN: 'Enter',
    pygame.K_BACKSPACE: 'Backspace',
    pygame.K_TAB: 'Tab',
    pygame.K_ESCAPE: 'Escape',
    pygame.K_LSHIFT: 'LShift',
    pygame.K_RSHIFT: 'RShift',
    pygame.K_LCTRL: 'LCtrl',
    pygame.K_RCTRL: 'RCtrl',
    pygame.K_LALT: 'LAlt',
    pygame.K_RALT: 'RAlt',
    pygame.K_UP: 'Up',
    pygame.K_DOWN: 'Down',
    pygame.K_LEFT: 'Left',
    pygame.K_RIGHT: 'Right',
    pygame.K_CAPSLOCK: 'CapsLock',
    pygame.K_DELETE: 'Delete',
    pygame.K_HOME: 'Home',
    pygame.K_END: 'End',
    pygame.K_PAGEUP: 'PgUp',
    pygame.K_PAGEDOWN: 'PgDn',
    pygame.K_PRINTSCREEN: 'PrintScreen',
    pygame.K_INSERT: 'Insert',
    pygame.K_PAUSE: 'Pause',
    pygame.K_F1: 'F1',
    pygame.K_F2: 'F2',
    pygame.K_F3: 'F3',
    pygame.K_F4: 'F4',
    pygame.K_F5: 'F5',
    pygame.K_F6: 'F6',
    pygame.K_F7: 'F7',
    pygame.K_F8: 'F8',
    pygame.K_F9: 'F9',
    pygame.K_F10: 'F10',
    pygame.K_F11: 'F11',
    pygame.K_F12: 'F12',
    pygame.K_MINUS: '-',
    pygame.K_EQUALS: '=',
    pygame.K_LEFTBRACKET: '[',
    pygame.K_RIGHTBRACKET: ']',
    pygame.K_BACKSLASH: '\\',
    pygame.K_SEMICOLON: ';',
    pygame.K_QUOTE: '\'',
    pygame.K_COMMA: ',',
    pygame.K_PERIOD: '.',
    pygame.K_SLASH: '/',
    pygame.KSCAN_GRAVE: '`'
}

# Set up the display (Ensure this matches the resolution used by the server)
screen = pygame.display.set_mode((800, 600))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER, PORT))

'''def receive_image(sock, width, height) -> pygame.Surface:
    # Receive the size of the incoming image
    img_size = int.from_bytes(sock.recv(4), 'big')

    # Now receive the image data itself
    img_data = b''
    sleep(1)
    while len(img_data) < img_size:
        packet = sock.recv(4096)  # Adjust buffer size as needed
        if not packet:
            break
        img_data += packet

    # Convert the received bytes back into an image
    return pygame.image.fromstring(img_data, (width, height), 'RGB')
'''

def receive_image(sock, width, height) -> pygame.Surface:
    # Receive the size of the incoming image
    img_size = int.from_bytes(sock.recv(4), 'big')

    # Now receive the image data itself
    img_data = b''
    while len(img_data) < img_size:
        packet = sock.recv(min(4096, img_size - len(img_data)))  # Adjust buffer size as needed
        if not packet:
            break
        img_data += packet

    # Check if received data matches the expected size
    if len(img_data) != img_size:
        raise ValueError(f"Received {len(img_data)} bytes, expected {img_size} bytes")

    # Convert the received bytes back into an image
    return pygame.image.fromstring(img_data, (width, height), 'RGB')

previous_x, previous_y = None, None

def calculate_delta(x, y, prev_x, prev_y):
    if prev_x is None or prev_y is None:
        return 0, 0
    return x - prev_x, y - prev_y

while True:
    sleep(0.001)
    
    # Receive the image data from the server and render it
    image = receive_image(s, 800, 600)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            s.close()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            s.send(f'coord {x} {y}'.encode())

        if event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            s.send(f'mouseup {x} {y}'.encode())

        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            delta_x, delta_y = calculate_delta(x, y, previous_x, previous_y)
            
            # Update previous position
            previous_x, previous_y = x, y
            s.send(f'mousemove {delta_x} {delta_y} {x} {y}'.encode())

        if event.type == pygame.KEYDOWN:
            s.send(f'keydown {key_mapping[event.key]}'.encode())
        
        if event.type == pygame.KEYUP:
            s.send(f'keyup {key_mapping[event.key]}'.encode())

    screen.blit(image, (0, 0))
    pygame.display.flip()
