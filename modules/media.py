#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils.utils import *
import adbutils
import os
import time


def get_screenshot(device, path):

    try:
        if device == None:
            raise Exception("No devices connected")
        if not os.path.exists(path):
            raise Exception("Path not found")

        abspath = get_timestamp_filename(path, ".png")

        device = adbutils.adb.device(device)

        if os.path.exists(abspath):
            os.remove(abspath)

        image = device.screenshot()
        image.save(abspath, format="PNG")

        return True, abspath

    except Exception as e:
        printError(e)
        return False, ""


def get_screenrecord(device, path):

    try:
        if device == None:
            raise Exception("No devices connected")
        if not os.path.exists(path):
            raise Exception("Path not found")

        abspath = get_timestamp_filename(path, ".mp4")
        abspath_dev = (f"/sdcard/{os.path.basename(abspath)}")
        device = adbutils.adb.device(device)

        if os.path.exists(abspath):
            os.remove(abspath)

        _ = device.shell(f"screenrecord {abspath_dev}", stream=True)

        pid = get_process_pid(device.serial, f"screenrecord")
        print(pid, "aaaa")
        
        if pid == "":
            raise Exception("Screenrecord PID not found")


        printInfo("Press Enter to stop recording...")
        input()

        print(device.shell(f"kill -2 {' '.join(pid)}"))
        if not device.sync.exists(abspath_dev):
            raise Exception("Screenrecord file not found")

        device.shell(
            f"ffplay -framerate 60 -framedrop -bufsize 16M {abspath_dev}", stream=True)

        device.sync.pull(abspath_dev, abspath)
        device.remove(abspath_dev)

        return True, abspath

    except Exception as e:
        printError(e)
        return False, ""
