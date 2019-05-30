#!/usr/bin/env python3
"""
scan USB devices and disable input devices plugged in
"""
import base64
import subprocess


def scanusb():
    xinitbash = "sudo xinput list --id-only"
    xinitproc = subprocess.Popen(xinitbash.split(), stdout=subprocess.PIPE)
    procoutput, procerror = xinitproc.communicate()
    inputs = procoutput.decode('utf-8').split("\n")
    ipbashcommand = "sudo lsusb -vt"
    process = subprocess.Popen(ipbashcommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    formatted = output.decode('utf-8').split("/:")
    drivers = {"xinputs": inputs}
    for x in formatted:
        y = x.split("|__")
        for z in y:
            encoded = base64.encodebytes(z.encode('utf-8'))
            i = z.split(",")
            for j in i:
                if str(j).__contains__("=") and str(j).__contains__("Class"):
                    drivers[encoded] = str(j).replace("Class=", "").lstrip()
    return drivers


def profile():
    usbbefore = scanusb()
    return usbbefore


def getreport(baseline):
    usbafter = scanusb()
    todisable = list(set(usbafter['xinputs']) - set(baseline['xinputs']))

    for disable in todisable:
        subprocess.call(['sudo', 'notify-send', 'IPPI', 'Input Device #' + disable + " Disabled"])
        xinitbash = "sudo xinput float " + disable
        subprocess.Popen(xinitbash.split(), stdout=subprocess.PIPE)
    thekeys = list(set(usbafter.keys()) - set(baseline.keys()))
    output = []

    for keys in thekeys:
        output.append(usbafter[keys])
    return output


test = 0

if test == 1:
    before = profile()

    try:
        input("Press enter to continue")
    except SyntaxError:
        pass

    if input:
        print(report(before))
