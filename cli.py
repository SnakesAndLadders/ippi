#!/usr/bin/env python3
import datetime
import os
import subprocess
import sys
from getipinfo import ipscan
import connections

ipinfo = ipscan()
report = {}
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    mydomain = ipinfo["domain"]
except KeyError:
    mydomain = "None"

try:
    dns2 = ipinfo["dns2"]
except KeyError:
    dns2 = "None"

try:
    htmloutput = "<html<head><title>Report for " + str(ipinfo["ipaddress"]) + "</title></head><body>"
    htmloutput += "<h2>Report for " + str(ipinfo["ipaddress"]) + "</h2><br>"
    ipoutput = "IP Address: " + ipinfo["ipaddress"] + "\nDefault Gateway: " + ipinfo["gateway"] + \
               "\nDomain: " + mydomain + "\nDNS 1: " + ipinfo["dns1"] + "\nDNS 2: " + dns2
    htmloutput += ipoutput.replace("\n", "<br>")
    print(chr(27) + "[2J")
    print(bcolors.OKGREEN + "IPPI CLI - Running all tests. Please wait.\n\n" + bcolors.ENDC)
    print(ipoutput)
    print(bcolors.OKGREEN + "\n******* Ping *******\n" + bcolors.ENDC)
    pinginfo = connections.ping(ipinfo["ipaddress"]).decode("utf-8")
    print(pinginfo)
    htmloutput += "<br><hr><b>Ping Output</b><br><p>" + pinginfo.replace("\n", "<br>")
    print(bcolors.OKGREEN + "\n******* Trace Route *******\n" + bcolors.ENDC)
    traceoutput = connections.traceroute(ipinfo["ipaddress"]).decode("utf-8")
    print(traceoutput)
    htmloutput += "<br><hr><b>Trace Route Output</b><br><p>" + traceoutput.replace("\n", "<br>")
    print(bcolors.OKGREEN + "\n******* Speed Test *******\n" + bcolors.ENDC)
    data = connections.speedtest()
    ping = data[0]
    download = data[1]
    upload = data[2]
    stoutput = "Ping: " + str(int(ping)) + "\nDownload: " + str(int(download)) + "\nUpload: " + str(int(upload)) + "\n"
    print(stoutput)
    htmloutput += "<br><hr><b>Speed Test Output</b><br><p>" + stoutput.replace("\n", "<br>")
    print(bcolors.OKGREEN + "\n******* NMap *******\n" + bcolors.ENDC)
    data = connections.nmap(ipinfo["ipaddress"])
    output = data[0]
    print(output)
    htmloutput += "<br><hr><b>NMAP Output</b><br><p>" + output.replace("\n", "<br>")
    htmloutput += "</body></html>"
    report = input(bcolors.FAIL + "Would you like to save the report? [y] for yes, anything else to quit\n" + bcolors.ENDC)
    while report:
        if report == "y" or report == "Y":
            print(bcolors.FAIL + "Saving Report" + bcolors.ENDC)
            outfile = os.getcwd() + "/" + str(ipinfo["ipaddress"].replace("/", "")) + "-" + str(
                datetime.datetime.now().strftime("%y-%m-%d")) + ".html"
            sourcefile = outfile
            p = open(sourcefile, "w")
            p.write(htmloutput)
            print(bcolors.FAIL + "Report saved to " + bcolors.OKBLUE + outfile + bcolors.ENDC)
            openme = input(bcolors.OKGREEN + "Would you like to open the report in Chrome? [y] for yes, "
                                             "anything else to quit\n" + bcolors.ENDC)

            if openme == "y" or openme == "Y":
                bashcommand = "/usr/bin/google-chrome " + outfile
                subprocess.Popen(bashcommand.split())
            else:
                print(bcolors.FAIL + "Exiting" + bcolors.ENDC)
                break

            break
        else:
            print(bcolors.FAIL + "Exiting" + bcolors.ENDC)
            break

except KeyError:
    print(bcolors.FAIL + "You are not connected to a network\n" + bcolors.ENDC)


