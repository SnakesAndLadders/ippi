#!/usr/bin/env python3
"""
Things to get done:
Run lldp and CDP discovery in a separate startup script that dumps the data to a text file with toaster alert
Run wireshark capture in background and pop up toaster when done
Clean up code
"""

from appJar import gui
from netaddr import *
from getipinfo import ipscan
from usbscan import profile, getreport
import connections

# Gather Basic Network Info

usbprofile = profile()
report = {}


def press(button):
    """
    Button Actions are defined here
    :param button:
    :return: no return
    """
    app.clearTextArea("Output")
    ipinfo = ipscan()

    if button == "IP Info":
        # Add info about DHCP server
        try:
            mydomain = ipinfo["domain"]
        except KeyError:
            mydomain = "None"

        try:
            dns2 = ipinfo["dns2"]
        except KeyError:
            dns2 = "None"

        try:
            ipoutput = "IP Address: " + ipinfo["ipaddress"] + "\nDefault Gateway: " + ipinfo["gateway"] + \
                       "\nDomain: " + mydomain + "\nDNS 1: " + ipinfo["dns1"] + "\nDNS 2: " + dns2
            ipinfohtml = "<table>"
            for item in ipinfo:
                ipinfohtml = ipinfohtml + "<tr><th>" + item + ": </th><td>" + ipinfo[item] + "</td></tr>"
            ipinfohtml = ipinfohtml + "</table>"
            report["ipinfo"] = ipinfohtml
            app.setTextArea("Output", ipoutput + "\n")
        except KeyError:
            app.setTextArea("Output", "You are not connected to a network\n")
    elif button == "Ping":
        import subprocess
        try:
            if ipinfo["ipaddress"]:
                output = connections.ping(ipinfo["ipaddress"])
                app.clearTextArea("Output")
                app.setTextArea("Output", output.decode("utf-8") + "\n")
                report["ping"] = "<p>" + output.decode("utf-8").replace("\n", "<br>")
        except KeyError:
            app.setTextArea("Output", "You are not connected to a network\n")
    elif button == "Traceroute":
        app.clearTextArea("Output")
        import subprocess

        try:
            if ipinfo["ipaddress"]:
                output = connections.traceroute(ipinfo["ipaddress"])
                app.clearTextArea("Output")
                app.setTextArea("Output", output.decode("utf-8") + "\n")
                report["traceroute"] = "<br><p>" + output.decode("utf-8").replace("\n", "<br>") + "</p><br>"
        except KeyError:
            app.setTextArea("Output", "You are not connected to a network\n")
    elif button == "Exit":
        app.clearTextArea("Output")
        confirm = app.yesNoBox("Shut Down", "Are you sure you want to shut down?", parent=None)
        if confirm:
            import os
            import subprocess
            os.system("shutdown now -h")
            app.setTextArea("Output", "Shutdown Started\n")
        else:
            app.setTextArea("Output", "Shutdown Aborted\n")
    elif button == "SpeedTest":

        app.clearTextArea("Output")
        import subprocess
        try:
            if ipinfo["ipaddress"]:
                data = connections.speedtest()
                ping = data[0]
                download = data[1]
                upload = data[2]
                output = "Ping = " + str(ping) + " ms\nDownload = " + str(int(download)) + " Mbps\nUpload = " + \
                         str(int(upload)) + " Mbps\n"
                app.setTextArea("Output", output + "\n")
                report["speedtest"] = "<p><b>Ping</b> = " + str(ping) + " ms<br><b>Download</b> = " + \
                                      str(int(download)) + " Mbps<br><b>Upload</b> = " + str(int(upload)) + \
                                      " Mbps<br></p>"
        except KeyError:
            app.setTextArea("Output", "You are not connected to a network\n")
    elif button == "Test USB":
        app.clearTextArea("Output")
        usboutput = "You recently plugged in a device that is a:\n"
        thereport = getreport(usbprofile)
        for usb in thereport:
            usboutput = usboutput + str(usb) + "\n"

        app.setTextArea("Output", usboutput + "\n")
    elif button == "WireShark":
        app.setTextArea("Output", button + "\n")
        try:
            if ipinfo["ipaddress"]:
                print("This feature still in development")
        except KeyError:
            app.setTextArea("Output", "You are not connected to a network\n")
    elif button == "NMap":

        app.clearTextArea("Output")
        import subprocess
        try:
            if ipinfo["ipaddress"]:
                data = connections.nmap(ipinfo["ipaddress"])
                output = data[0]
                html = data[1]
                app.setTextArea("Output", output + "\n")
                report["nmap"] = html
        except AttributeError:
            app.setTextArea("Output", "You are not connected to a network\n")
    elif button == "Send":
        import datetime
        app.clearTextArea("Output")
        import subprocess
        finalreport = "<html<head><title>Report for " + str(ip.IPAddress) + "</title></head><body>"
        try:
            finalreport = finalreport + "<H1> IP Address Information</H1><br>" + report["ipinfo"] + "<br><br>"
        except KeyError:
            pass
        try:
            finalreport = finalreport + "<H1> Ping Information</H1><br>" + report["ping"] + "<br><br>"
        except KeyError:
            pass
        try:
            finalreport = finalreport + "<H1> Traceroute Information</H1><br>" + report["traceroute"] + "<br><br>"
        except KeyError:
            pass
        try:
            finalreport = finalreport + "<H1> Speed Test Information</H1><br>" + report["speedtest"] + "<br><br>"
        except KeyError:
            pass
        try:
            finalreport = finalreport + "<H1> CDP Information</H1><br>" + report["cdpinfo"] + "<br><br>"
        except KeyError:
            pass
        try:
            finalreport = finalreport + "<H1> NMap Information</H1><br>" + report["nmap"] + "<br><br>"
        except KeyError:
            pass

        finalreport = finalreport + "</body></html>"
        sourcefile = "./reports/" + str(ipinfo["ipaddress"].replace("/", "")) + "-" + str(datetime.datetime.now().strftime("%y-%m-%d")) + ".html"
        p = open(sourcefile, "w")
        p.write(finalreport)
        # subprocess.call(['python', 'transfer_file.py', sourcefile])
        app.setTextArea("Output", "Report Written to\n" + sourcefile)


# create a GUI variable called app
app = gui("Network Tools", "480x320")
# app.setSize("fullscreen")
app.setBg("#003366", override=True)
app.setFont(16)
app.setSticky("nesw")
app.setPadding([2,2])

# link the buttons to the function press()
# Row 1
app.addButton("IP Info", press, 0, 0)
app.addButton("Ping", press, 0, 1)
app.addButton("Traceroute", press, 0, 2)

# Row 2
app.addButton("WireShark", press, 1, 0)
app.addButton("NMap", press, 1, 1)
app.addButton("SpeedTest", press, 1, 2)

# Row 3
app.addButton("Test USB", press, 2, 0)
app.addButton("Send", press, 2, 1)
app.addButton("Exit", press, 2, 2)

# Row 4
app.addTextArea("Output", 4, 0, 3)

# Set Button Sizes
# app.setButtonWidth("IP Info", 10)
# app.setButtonWidth("Ping", 10)
# app.setButtonWidth("Traceroute", 10)
# app.setButtonWidth("WireShark", 10)
# app.setButtonWidth("NMap", 10)
# app.setButtonWidth("SpeedTest", 10)
# app.setButtonWidth("Test USB", 10)
# app.setButtonWidth("Send", 10)
# app.setButtonWidth("Exit", 10)

# Set Control Colours
app.setButtonBg("IP Info", "#003366")
app.setButtonFg("IP Info", "#FFFFFF")
app.setButtonBg("Ping", "#003366")
app.setButtonFg("Ping", "#FFFFFF")
app.setButtonBg("Traceroute", "#003366")
app.setButtonFg("Traceroute", "#FFFFFF")
app.setButtonBg("WireShark", "#003366")
app.setButtonFg("WireShark", "#FFFFFF")
app.setButtonBg("NMap", "#003366")
app.setButtonFg("NMap", "#FFFFFF")
app.setButtonBg("SpeedTest", "#003366")
app.setButtonFg("SpeedTest", "#FFFFFF")
app.setButtonBg("Test USB", "#003366")
app.setButtonFg("Test USB", "#FFFFFF")
app.setButtonBg("Send", "#003366")
app.setButtonFg("Send", "#FFFFFF")
app.setButtonBg("Exit", "#003366")
app.setButtonFg("Exit", "#FFFFFF")

app.setTextAreaBg("Output", "#003366")
app.setTextAreaFg("Output", "#FFFFFF")
app.setTextAreaFont("Output", size=10)

# start the GUI
app.go()
