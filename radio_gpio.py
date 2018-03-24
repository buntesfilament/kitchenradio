#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import datetime
import subprocess
import os
import signal
from time import sleep

# TODO: is it actually necessary to cleanup??
def handleSIGTERM():
    GPIO.cleanup()

def getEnabledRadios():
    enabledRadioNums = []
    try:
        enabledRadioServices = os.listdir("/etc/systemd/system/default.target.wants")
        # try to find "radio@" in all filenames and extract the character after the @
        # which should be the radio number.
        for fileName in enabledRadioServices:
            searchStr = "radio@"
            numPos = fileName.find(searchStr)
            if(numPos != -1):
                radioNum = int(fileName[len(searchStr) + numPos])
                enabledRadioNums.append(radioNum)

    except Exception as e:
        print("couldnt parse filenames, return empty list of radios:\n", e)

    return enabledRadioNums

    

def main():
    MAXRADIOS = 4 #TODO: depend on radios.txt
    BUTTONPIN = 6 # Modify this variable to match your actual buttons GPIO pin
    enabledRadios = getEnabledRadios()
    print(enabledRadios)
    # if no radios enabled, enable and start radio@1
    if(len(enabledRadios) == 0):
        enabledRadios.append(1)
        subprocess.call(["sudo", "systemctl", "start", "radio@1"])
        subprocess.call(["sudo", "systemctl", "enable", "radio@1"])

    # if there is more than one radio enabled, stop and disable all,
    # but keep first in list enabled/started.
    elif(len(enabledRadios) > 1):
        for radio in enabledRadios[1:]:
            subprocess.call(["sudo", "systemctl", "stop", "radio@" + str(radio)])
            subprocess.call(["sudo", "systemctl", "disable", "radio@" + str(radio)])
        
    
    currentRadio = enabledRadios[0]

    
    def my_callback(channel):
        nonlocal currentRadio
        nonlocal MAXRADIOS
        nonlocal BUTTONPIN

        # When button is down again
        if GPIO.input(BUTTONPIN) == GPIO.LOW:
            prevRadio = currentRadio
            currentRadio = currentRadio = max(1, (currentRadio + 1) % (MAXRADIOS + 1));
            print(currentRadio)
            # start the next radio
            subprocess.call(["sudo", "systemctl", "start", "radio@" + str(currentRadio)])
            subprocess.call(["espeak", "radio " + str(currentRadio)])

            # stop previous radio service
            subprocess.call(["sudo", "systemctl", "stop", "radio@" + str(prevRadio)])

            # disable all radios (only one should be enabled though)
            # radio@ disables all radio services, radio@* doesnt work here
            subprocess.call(["sudo", "systemctl", "disable", "radio@"])
            # enable only the currently selected radio
            subprocess.call(["sudo", "systemctl", "enable", "radio@" + str(currentRadio)])


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(6, GPIO.BOTH, callback=my_callback, bouncetime=10)
    while True:
        sleep(1)




try:
    main()
except KeyboardInterrupt:
    print("exited by KeyboardInterrupt from user.\n")
except Exception as e:
    print("Error trying to run radio-gpio.py:\n" + e)
finally:
    print("\nquit radio-gpio. clean GPIO.\n")
    GPIO.cleanup() # this ensures a clean exit
