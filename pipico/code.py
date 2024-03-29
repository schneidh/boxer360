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
dirty = False

# whether to emulate buttons for left/right trigger
emulateTriggerButtons = True
leftTriggerButton = 7
rightTriggerButton = 8

while True:
    start = supervisor.ticks_ms()
    while serial.in_waiting > 0:
        pre = serial.read()[0]
        if (pre == 255):
            button = serial.read()[0]
            if (button <= 16):
                state = serial.read()[0]
                if (state == 1):
                    gp.press_buttons(button)
                elif (state == 0):
                    gp.release_buttons(button)
            elif (button == 20):
                x = serial.read()[0] - 127
                dirty = True
            elif (button == 21):
                y = serial.read()[0] - 127
                dirty = True
            elif (button == 22):
                value = serial.read()[0] - 127
                if (emulateTriggerButtons and value > 0):
                    gp.press_buttons(leftTriggerButton)
                elif (emulateTriggerButtons and value <= 0):
                    gp.release_buttons(leftTriggerButton)
                else:
                    z = value
                    dirty = True
            elif (button == 23):
                rx = serial.read()[0] - 127
                dirty = True
            elif (button == 24):
                ry = serial.read()[0] - 127
                dirty = True
            elif (button == 25):
                value = serial.read()[0] - 127
                if (emulateTriggerButtons and value > 0):
                    gp.press_buttons(rightTriggerButton)
                elif (emulateTriggerButtons and value <= 0):
                    gp.release_buttons(rightTriggerButton)
                else:
                    rz = value
                    dirty = True
    if dirty:
        gp.move_joysticks(x, y, z, rx, ry, rz)
        dirty = False
    # sleep for the time remaining of the 0.02 second tick
    # this prevents the axis events from flooding the host
    tick_remaining = supervisor.ticks_ms() - start
    time.sleep(0.02 - min(0.02, tick_remaining / 1000.0));

