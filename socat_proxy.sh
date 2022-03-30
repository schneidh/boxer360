#!/bin/zsh
socat TCP4-LISTEN:13370 /dev/cu.usbmodem1103,raw,echo=0
