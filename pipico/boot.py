import usb_hid
import usb_cdc

usb_cdc.enable(console=True, data=True)
usb_hid.enable((usb_hid.Device.MOUSE, usb_hid.Device.KEYBOARD,))