import usb_hid
import usb_cdc

GAMEPAD_MODE = 1
KB_MOUSE_MODE = 2
# mode is either GAMEPAD_MODE or KB_MOUSE_MODE
mode = GAMEPAD_MODE

#
# CircuitPython boot script to enable USB HID gamecontroller support.
#
GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x04,  #   Report ID (4)
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (Button 1)
    0x29, 0x10,  #   Usage Maximum (Button 16)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x10,  #   Report Count (16)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls, Left and Right Sticks)
    0x15, 0x81,  #   Logical Minimum (-127)
    0x25, 0x7F,  #   Logical Maximum (127)
    0x09, 0x30,  #   Usage (X)
    0x09, 0x31,  #   Usage (Y)
    0x09, 0x32,  #   Usage (Z)
    0x09, 0x33,  #   Usage (Rx)
    0x09, 0x34,  #   Usage (Ry)
    0x09, 0x35,  #   Usage (Rz)
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x06,  #   Report Count (6)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,        # End Collection
))

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(4,),           # Descriptor uses report ID 4.
    in_report_lengths=(8,),    # This gamepad sends 8 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_cdc.enable(console=True, data=True)
if mode == GAMEPAD_MODE:
  usb_hid.enable((gamepad,))
else:
  usb_hid.enable((usb_hid.Device.MOUSE, usb_hid.Device.KEYBOARD,))