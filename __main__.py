"""
This script runs all the things.
"""

import config
import validate_certs
import scan_ports
import process_files


def run():
    print("this is where the fun happens")
    # server_list = process_files.parse_csv(config.source_files)
    server_list = process_files.parse_csv(config.source_files)
    scanner = scan_ports.initialize_port_scanner()
    leftovers = []
    results = []
    for server in server_list:
        print(f'Scanning {server["hostname"]} ({server["IP"]}) for open ports...')
        open_ports = scan_ports.identify_open_ports(
            scanner, server["IP"], config.target_ports
        )
        print("Done!")
        if len(open_ports) > 0:
            if len(open_ports) == 1:
                server["Ports"] = open_ports[0]
            else:
                server["Ports"] = open_ports
            print(f'Open: {server["Ports"]}')
        else:
            server["Ports"] = None
            print("No open ports found.")
        if server["Ports"] is not None:
            print("Gathering certificates...")
            if len(open_ports) > 1:
                server["Certification"] = []
            for port in open_ports:
                if port == 3306:  # hardcoded until i can fix the sql ssl bug.
                    print("mysql, needs manually sorting")
                    leftovers.append(server)
                else:
                    # creates a certificate object by extracting the cert for the IP:Port, then grabbing the relevant info.
                    certification = validate_certs.determine_certificate_information(
                        validate_certs.extract_certificate(server["IP"], port)
                    )
                    # Formatting to get it to parse the datetime.datetime
                    before = f'{certification["NotBefore"]}'
                    after = f'{certification["NotAfter"]}'
                    org = f'{certification["Organization"]}'
                    common = f'{certification["CommonName"]}'
                    cert = {
                        "NotBefore": before,
                        "NotAfter": after,
                        "Organization": org,
                        "CommonName": common,
                    }
                    if len(open_ports) == 1:
                        server["Certification"] = cert
                    else:
                        server["Certification"].append(cert)
                    results.append(server)
        print("Done! Moving onto next server...")
    print("Done! Writing to files...")
    process_files.write_csv(
        ["hostname", "IP", "Ports", "Certification"], results, "checked_servers.csv"
    )
    process_files.write_csv(
        ["hostname", "IP", "Ports", "Certification"], leftovers, "skipped_servers.csv"
    )


if __name__ == "__main__":
    run()
