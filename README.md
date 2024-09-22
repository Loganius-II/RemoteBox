# Welcome to RemoteBox!
![RemoteBox](https://github.com/Loganius-II/RemoteBox/blob/main/IMG_1877.jpeg)
## Overview:
#### *RemoteBox* is TCP based cloud computing software that allows you to access your at-home PC anywhere! Just run the server on the computer you want to be remotely accessed, and run the client on any computer you want to access your server with. Its that simple.

## DISCLAIMER

#### *RemoteBox* should be used with care and responsibility. I am not responsible for any **illegal** activities or use of this software. Use it at your own **risk**. This software is still in **BETA** stages so there is still much work to be done. Stay tuned in for updates. **Windows only compatibility** as of now (It uses pywin32). If you want to establish a not LAN connection you will have to use your public IP. At the moment there is no way of changing it unless you modify the server code to run via public IP. You will also have to enable *port forwarding*. This is a risky move that makes your home internet more vulnerable to attackers. Follow through at your own risk!

## Additional Info:

#### You can download the requirements to a virtual environment. While your venv is active do `pip install -r requirements.txt`

## Roadmap:
- Full HID support
  - I am thinking about using Auto Hot Key to implement HID with consistancy
  - Outputting the keys to the targetted application
  - Right clicking
  - Scrolling
  - HID bug fixes
- Faster response times
- FPS viewer
- Installation wizard
- Faster FPS
- Server-side GUI for maximum customization such as IP and Port changes, performance settings, etc.
- Bug fixes
- Performance improvments
- Argv initialization

## Patch Notes:

### [Version 0.0.1 - Beta](src/0.0.1/)
- Very basic proof of concept
- Rough and quickly put together; not thorough
- Features:
    - Basic screen resolution ratioing
    - Mouse movement and coordinate placement and ratio representation
    - Only left click
    - No other Human Interface Device (HID) registered

- Requirements:
   - pyautogui==0.9.54
   - pywin32==306
- Much, much more to come 
to come 

### [Version 0.0.2 - Beta](src/0.0.2/)
 - Testing AHK to see if I like that
 - Small improvements
 - Editable `Settings.json` file
 - HID inputs:
   - The target computer outputs abc...
   - *Special keys* such as space and shift type as 'Shift'
   - This will be fixed in the future

 - More updates in the works! Stay tuned!

 ### [Version 0.1.0 - Beta](src/0.1.0/)
 - Work in progress