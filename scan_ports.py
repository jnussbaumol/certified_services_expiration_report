"""
This script searches through the hosts and ports within config.py and identifies available addresses and ports using nmap.

If run on its own, it will perform a test to see if it works by scanning localhost's HTTP ports
"""

import nmap
import sys

# TODO: get opinions on if this is self_documenting enough
def initialize_port_scanner():
    print('Initializing PortScanner...')
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(1)
    except:
        print('Unexpected error:.', sys.exc_info()[0])
        sys.exit(1)
    return nm
 
def identify_open_ports(scanner, hostname, ports):
    formatted_ports = ','.join([str(port) for port in ports])
    print(f'Scanning {hostname} on ports {formatted_ports}...')
    scanner.scan(hosts=hostname, ports=formatted_ports)
    # print(f'Running nmap command: {scanner.command_line()}')
    open_ports = []
    for host in scanner.all_hosts():
        for port in scanner[host].all_tcp():
            results = scanner[host]['tcp'][port]
            if results['state'] == 'open':
                open_ports.append(port)
    return open_ports

if __name__ == '__main__':
    print('Running port scanning test...')
    test_host = '127.0.0.1'
    test_port = [80, 443, 8080, 8443]
    test_scanner = initialize_port_scanner()
    open_ports = identify_open_ports(test_scanner, test_host, test_port)
    print('Done! Summarizing results...')
    print(f'Open Ports on {test_host}:\n{",".join(open_ports)}')