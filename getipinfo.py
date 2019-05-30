import re
import subprocess


def ipscan():
    """
    Get all IP and Network info
    :return: ipinfo dictionary
    """
    ipbashcommand = "nmcli dev show"
    process = subprocess.Popen(ipbashcommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    formatted = re.split('\n', output.decode("utf-8"))
    final = []
    for y in formatted:
        y.lstrip()
        final.append(y.split(':', 1))

    ipinfo = {}
    for b in final:
        try:
            key = b[0]
            data = b[1].lstrip()
            if key.startswith("IP4.") and (not key.startswith("IP4.ROUTE")):
                if (not data) or (data != "--"):

                    if data.startswith("127"):
                        continue
                    elif key.startswith("IP4.GATEWAY"):
                        ipinfo["gateway"] = data
                    elif key.startswith("IP4.DNS[1]"):
                        ipinfo["dns1"] = data
                    elif key.startswith("IP4.DNS[2]"):
                        ipinfo["dns2"] = data
                    elif key.startswith("IP4.ADDRESS"):
                        ipinfo["ipaddress"] = data
                    elif key.startswith("IP4.DOMAIN"):
                        ipinfo["domain"] = data
            else:
                if (not data) or (data != "--"):
                    if key in ipinfo:
                        ipinfo[key + "(2)"] = data
                    else:
                        ipinfo[key] = data
        except IndexError:
            continue
    return ipinfo
