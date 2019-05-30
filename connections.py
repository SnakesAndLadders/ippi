import subprocess
from netaddr import ip


def ping(ipaddress):
    if ipaddress:
        bashcommand = "ping -c 5 -n -i 0.2 -W1 1.1.1.1"
        process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return False
        return output


def traceroute(ipaddress):
    if ipaddress:
        bashcommand = "traceroute -n -w 3 -q 1 1.1.1.1"
        process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return False
        return output


def speedtest():
    import pyspeedtest
    st = pyspeedtest.SpeedTest(host="speedtest.ed.shawcable.net")
    output = [st.ping(), st.download() / 1000000, st.upload() / 1000000]
    return output


def nmap(ipaddress):
    import nmap
    nm = nmap.PortScanner()
    cidr = ip.IPNetwork(ipaddress)
    nm.scan(hosts=str(cidr.cidr), arguments="-T4 -F")
    output = ""
    html = "<table>"
    for host in nm.all_hosts():
        output = output + '----------------------------------------------------\n'
        output = output + 'Host : %s (%s)\n' % (host, nm[host].hostname())
        output = output + 'State : %s\n' % nm[host].state()
        html = html + "<tr><th>Host: " + str(nm[host].hostname()) + " " + nm[host]["addresses"]["ipv4"] + \
               " (" + str(nm[host].state()) + ")</th></tr>"
        for proto in nm[host].all_protocols():
            output = output + '----------\n'
            output = output + 'Protocol : %s\n' % proto
            lport = nm[host][proto].keys()
            html = html + "<tr><td>Protocol: " + str(proto) + "</td></tr>"
            for port in lport:
                output = output + 'port : %s\tstate : %s\n' % (port, nm[host][proto][port]['state'])
                html = html + "<tr><td>     " + str(port) + " State: " + str(nm[host][proto][port]['state'])
    tosend = [output, html]
    return tosend

