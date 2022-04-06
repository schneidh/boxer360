import usb_hid
import usb_cdc

#
# CircuitPython boot script to enable USB HID gamecontroller support.
#
GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x04,  #   Report ID (4)
    # 15 buttons
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (Button 1)
    0x29, 0x10,  #   Usage Maximum (Button 16)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x10,  #   Report Count (16)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    # 6 axises -> 2 thumbsticks and 2 triggers
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls, Left and Right Sticks)
    0x15, 0x81,  #   Logical Minimum (-127)
    0x25, 0x7F,  #   Logical Maximum (127)
    0x09, 0x30,  #   Usage (X)
    0x09, 0x31,  #   Usage (Y)
    0x09, 0x32,  #   Usage (Z)
    0x09, 0x35,  #   Usage (Rz)
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x04,  #   Report Count (4)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x02,  #   Usage Page (Simulation Controls) 
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x02,  #   Report Count (2)
    0x15, 0x81,  #   Logical Minimum (-127)
    0x25, 0x7F,  #   Logical Maximum (127)
    0x09, 0xC5,  #   Usage (Break)
    0x09, 0xC4,  #   Usage (Accelerator)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls, Left and Right Sticks)
    0x09, 0x39,  #   Usage (Hat Switch)
    0x15, 0x01,  #   Logical Minimum (1) 
    0x25, 0x08,  #   Logical Maximum (8)  
    0x35, 0x00,  #        (GLOBAL) PHYSICAL_MINIMUM   0x00 (0)  <-- Info: Consider replacing 35 00 with 34
    0x46, 0x3B, 0x01,  #      (GLOBAL) PHYSICAL_MAXIMUM   0x013B (315)  
    0x66, 0x14, 0x00,  #      (GLOBAL) UNIT               0x0014 Rotation in degrees [1° units] (4=System=English Rotation, 1=Rotation=Degrees)  <-- Info: Consider replacing 66 1400 with 65 14
    0x75, 0x04,  #        (GLOBAL) REPORT_SIZE        0x04 (4) Number of bits per field  
    0x95, 0x01,  #        (GLOBAL) REPORT_COUNT       0x01 (1) Number of fields <-- Redundant: REPORT_COUNT is already 1 
    0x81, 0x42,  #        (MAIN)   INPUT              0x00000042 (1 field x 4 bits) 0=Data 1=Variable 0=Absolute 0=NoWrap 0=Linear 0=PrefState 1=Null 0=NonVolatile 0=Bitmap 
    0x15, 0x00,  #        (GLOBAL) LOGICAL_MINIMUM    0x00 (0)  <-- Info: Consider replacing 15 00 with 14
    0x25, 0x00,  #        (GLOBAL) LOGICAL_MAXIMUM    0x00 (0)  <-- Info: Consider replacing 25 00 with 24
    0x35, 0x00,  #        (GLOBAL) PHYSICAL_MINIMUM   0x00 (0) <-- Redundant: PHYSICAL_MINIMUM is already 0 <-- Info: Consider replacing 35 00 with 34
    0x45, 0x00,  #        (GLOBAL) PHYSICAL_MAXIMUM   0x00 (0)  <-- Info: Consider replacing 45 00 with 44, 
    0x65, 0x00,  #        (GLOBAL) UNIT               0x00 No unit (0=None)  <-- Info: Consider replacing 65 00 with 64
    0x75, 0x04,  #        (GLOBAL) REPORT_SIZE        0x04 (4) Number of bits per field <-- Redundant: REPORT_SIZE is already 4 
    0x95, 0x01,  #        (GLOBAL) REPORT_COUNT       0x01 (1) Number of fields <-- Redundant: REPORT_COUNT is already 1 
    0x81, 0x03,  #        (MAIN)   INPUT              0x00000003 (1 field x 4 bits) 1=Constant 1=Variable 0=Absolute 0=NoWrap 0=Linear 0=PrefState 0=NoNull 0=NonVolatile 0=Bitmap 
    0xC0,        # End Collection
))


# Example Stadia button usage example:

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(4,),           # Descriptor uses report ID 4.
    in_report_lengths=(9,),    # This gamepad sends 9 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_cdc.enable(console=True, data=True)
usb_hid.enable((gamepad,))