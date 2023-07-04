#!/bin/zsh
socat TCP4:<raspberrypi_host>:23370 /dev/cu.usbmodem1103,raw,echo=0
