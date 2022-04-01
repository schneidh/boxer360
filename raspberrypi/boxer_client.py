import evdev
import socket
import time
import sys

#
# Script to read XBox 360 events from evdev and forward to a remote socket
# on port 13370.  The data is sent as a 3 byte packet.  The first byte is a
# marker byte of 255 followed by a byte that contains the button or joystick 
# axis number followed by a byte of the button/axis state.  For buttons, a
# value of 0 indicates a unpressed button and a value of 1 indicates a pressed
# button.  For axis, the value 
#
if len(sys.argv) < 2:
    print("Target IP or host is required, example: python3 boxer_client.py <target_ip>")
    exit(1)

host = sys.argv[1]
port = 13370

device = None
while device is None:
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if "Xbox 360" in device.name:
            device = evdev.InputDevice(device.path)
            print("Found device", device.name, device.path)
    if device is None:
        print("No game controller device found...")
        time.sleep(10)

button_lookup = dict([
  (315, 1), # start button
  (314, 2), # back button
  (304, 3), # a button
  (305, 4), # b button
  (307, 5), # x button
  (308, 6), # y button
  (706, 7), # dpad up button
  (707, 8), # dpad down button
  (704, 9), # dpad left button
  (705, 10), # dpad right button
  (310, 11), # left shoulder button
  (311, 12), # right shoulder button
  (317, 13), # left stick button
  (318, 14) # right stick button
])

axis_lookup = dict([
    (3, 20), # left stick x axis
    (4, 21), # left stick y axis
    (0, 22), # right stick x axis
    (1, 23), # right stick y axis
    (2, 24), # left trigger
    (5, 25), # right trigger
])

frame = bytearray(3)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            try:
                s.connect((host, port))
                for event in device.read_loop():
                    if event.type == evdev.ecodes.EV_KEY and event.code in button_lookup:
                        frame[0] = 255
                        frame[1] = button_lookup[event.code]
                        frame[2] = event.value
                        s.sendall(frame)
                    elif event.type == evdev.ecodes.EV_ABS and 0 <= event.code <= 5 :
                        frame[0] = 255
                        frame[1] = axis_lookup[event.code]
                        if event.code == 0 or event.code == 1 or event.code == 3 or event.code == 4:
                            # divide by 256, add 128 to fit within 0-254
                            frame[2] = min(int(event.value / 256 + 128), 254)
                        elif event.code == 2 or event.code == 5:
                            frame[2] = min(int(event.value), 254)
                        s.sendall(frame)
            except ConnectionRefusedError:
                print("Connection refused for", host, "port", port)
                time.sleep(10)
except KeyboardInterrupt:
    device.close()
    print("Exiting...")