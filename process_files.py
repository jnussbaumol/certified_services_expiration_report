"""
This script will take the input files loaded from config.py and extract the hostname and IP address of every service that is running and in the desired IP range.
"""
import csv
#import json # TODO: add json support

def parse_csv(filename):
    server_list = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[6] == "Running" and row[8][:3] == '172': # i don't like this being hardcoded and just referencing the row indices.
                server_list.append({'hostname':row[0], 'IP':row[8]})
    return server_list

def write_csv(headers, data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fields = headers
        csvwriter = csv.DictWriter(csvfile, fields)
        csvwriter.writeheader()
        for row in data:
            csvwriter.writerow(row)

if __name__ == '__main__':
    desired_servers = parse_csv('AzureVirtualMachines.csv')
    for server in desired_servers:
        print(f'Server: {server[0]}, IP: {server[1]}')