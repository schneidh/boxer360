from hid_gamepad import Gamepad
import usb_hid
import usb_cdc
import time
import supervisor

#
# CircuitPython script to receive gamepad events on the USB CDC port
# and send them as USB HID gamecontroller events to host.
#
serial = usb_cdc.data
gp = Gamepad(usb_hid.devices)

# Axis value tracking vars
x = 0
y = 0
z = 0
rx = 0
ry = 0
rz = 0
update_axis = False
while True:
    start = supervisor.ticks_ms()
    while serial.in_waiting > 0:
        pre = serial.read()[0]
        if (pre == 255):
            button = serial.read()[0]
            if (1 <= button <= 16):
                state = serial.read()[0]
                if (state == 1):
                    gp.press_buttons(button)
                elif (state == 0):
                    gp.release_buttons(button)
            elif (button == 20):
                # left x
                x = serial.read()[0] - 127
                update_axis = True
            elif (button == 21):
                # left y
                y = serial.read()[0] - 127
                update_axis = True
            elif (button == 22):
                # left trigger
                rx = serial.read()[0] - 127
                update_axis = True
            elif (button == 23):
                # right x
                z = serial.read()[0] - 127
                update_axis = True
            elif (button == 24):
                # right y
                rz = serial.read()[0] - 127
                update_axis = True
            elif (button == 25):
                # right trigger
                ry = serial.read()[0] - 127
                update_axis = True
    if update_axis:
        gp.move_joysticks(x, y, z, rx, ry, rz)
        update_axis = False
    # sleep for the time remaining of the 0.02 second tick
    # this prevents the axis events from flooding the host
    tick_remaining = supervisor.ticks_ms() - start
    time.sleep(0.02 - min(0.02, tick_remaining / 1000.0));
