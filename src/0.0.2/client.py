
import socket
import pygame
import io
from time import sleep

SERVER = '192.168.1.101'  # Your server's IP address
PORT = 6000

pygame.init()

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
    screen.blit(image, (0, 0))
    pygame.display.flip()
