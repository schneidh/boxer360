# Boxer 360
Boxer 360 is a set of python and circuitpython scripts to allow an XBox 360
controller to be used with a M1 Mac.  (Tested on a base model M1 Macbook Air)

In addition to the mac, it also requires a Raspberry Pi and a Pi Pico or equivilent RP2040.
I tested with an [Adafruit KB2040](https://www.adafruit.com/product/5302) and [PI Pico W](https://www.adafruit.com/product/5526).  I also used their circuitpython gamepad code as a starting point for the Pico code.

## Background
I recently purchased a M1 Macbook Air, but found that my XBox 360 controller
(with USB wireless adapter) did not work with the new setup.  This setup worked
perfectly fine with my previous linux laptop.  So to work around this, I came up
with a new setup.

This is the new setup:
XBox 360 Controller -> Raspberry Pi -> M1 Macbook <-> Pi Pico

When you plug the XBox 360 controller into the Raspberry PI, it will show up in evdev,
which the `boxer_server.py` script reads and provides a server socket running on the raspberrypi.
The socat connects to the socket on the raspbery pi and forwards the events to
the USB CDC serial port exposed by the Pi Pico.  Finally, the Pi Pico reads the events from
the USB CDC serial port and sends game controller HID events to the host mac.  The virtual
USB HID game controller of the Pi Pico is recognized by Steam and a gamepad testing website
that I use.  I was also able to get Moonlight QT to recognize it and forward to a cloud gaming VM.  (This was my main use case since I use [Maximum Settings](https://maximumsettings.com/) for gaming)

## Prerequisites
On the Raspberry Pi, you will need to install the evdev python library and copy [boxer_server.py](raspberrypi/boxer_client.py) to your Pi.

On the Pi Pico, you will need to install CircuitPython along with Adafruits [CircuitPython HID Library](https://github.com/adafruit/Adafruit_CircuitPython_HID).  Then copy [boot.py](pipico/boot.py), [code.py](pipico/code.py), [hid_gamepad.py](pipico/hid_gamepad.py) to the Pi Pico.

On your mac, you will need to run the socat command from [socat_proxy.sh](socat_proxy.sh).  You may need to change the target USB serial port device.  It will vary depending on which USB port you use.

## Startup
To start, first plugin your Pi Pico into your mac.  Then
run `boxer_server.py` on the Raspberry pi.   Then update the raspberrypi_host in `socat_proxy.sh` and start the socat proxy on the mac. If everything
works, you should see the controller show up in a web browser if you visit [https://gamepad-tester.com/](https://gamepad-tester.com/).
