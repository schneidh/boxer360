import usb_hid
import usb_cdc
import time
import supervisor
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

#
# CircuitPython script to receive gamepad events on the USB CDC port
# and send them as USB HID gamecontroller events to host.
#
serial = usb_cdc.data
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
tick_duration = 0.01

mx = 0
my = 0
button_map = (
    Keycode.SPACE, Keycode.E, Keycode.SPACE, Keycode.SPACE, # a, b, x, y
    Keycode.SPACE, Keycode.SHIFT, Keycode.SPACE, Keycode.SHIFT, # left/right shoulder
    Keycode.SPACE, Keycode.E, Keycode.SPACE, # select, start, blank
    Keycode.UP_ARROW, Keycode.DOWN_ARROW, Keycode.LEFT_ARROW, Keycode.RIGHT_ARROW) # d-pad
left_stick_map = (Keycode.W, Keycode.S, Keycode.A, Keycode.D)

def toMouseMove(raw):
    if -95 > raw > 95:
        return raw // 6
    elif -45 >  raw > 45:
        return raw // 12
    return raw // 16

def mk_mode():
    global mx, my, mode
    while serial.in_waiting > 0:
        pre = serial.read()[0]
        if (pre == 255):
            button = serial.read()[0]
            if 1 <= button <= 15:
                state = serial.read()[0]
                if (state == 0):
                    keyboard.release(button_map[button - 1])
                elif (state == 1):
                    keyboard.press(button_map[button - 1])
            elif button == 20:
                value = serial.read()[0] - 127
                if value > 95:
                    keyboard.press(left_stick_map[3])
                elif value < -95:
                    keyboard.press(left_stick_map[2])
                else:
                    keyboard.release(left_stick_map[3])
                    keyboard.release(left_stick_map[2])
            elif button == 21:
                value = serial.read()[0] - 127
                if value > 95:
                    keyboard.press(left_stick_map[1])
                elif value < -95:
                    keyboard.press(left_stick_map[0])
                else:
                    keyboard.release(left_stick_map[1])
                    keyboard.release(left_stick_map[0])
            elif button == 22:
                value = serial.read()[0] - 127
                if value > 0:
                    mouse.press(Mouse.RIGHT_BUTTON)
                else:
                    mouse.release(Mouse.RIGHT_BUTTON)
            elif button == 23:
                mx = serial.read()[0] - 127
                if -30 < mx < 30:
                    mx = 0
            elif button == 24:
                my = serial.read()[0] - 127
                if -30 < my < 30:
                    my = 0
            elif button == 25:
                value = serial.read()[0] - 127
                if value > 0:
                    mouse.press(Mouse.LEFT_BUTTON)
                else:
                    mouse.release(Mouse.LEFT_BUTTON)

while True:
    start = supervisor.ticks_ms()
    mk_mode()
    mouse.move(toMouseMove(mx), toMouseMove(my))
    # sleep for the time remaining of the 0.02 second tick
    # this prevents the axis events from flooding the host
    tick_remaining = supervisor.ticks_ms() - start
    time.sleep(tick_duration - min(tick_duration, tick_remaining / 1000.0))

