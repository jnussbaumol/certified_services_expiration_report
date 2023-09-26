"""
This is meant to be a one-time script to complete the first report. 
If building this out to be an automatable report that is regularly scanned, this script needs to be revisited and integrated into the primary workflow script.
"""

import csv

results = [{}]
with open('mysql_results.txt') as textfile:
    counter = 0
    for line in textfile:
        line = line.strip()
        if 'Results' in line:
            results.append({})
            ip = line.split(':')
            results[counter]['IP'] = ip[1].strip()
        elif 'issuer' in line:
            issuer = line.split('=')
            # handling the edge case of issuer having more info:
            if len(issuer) > 3:
                issuer = line.split(',')
                # some voodoo to clean-up and extract the org
                results[counter]['Common Name'] = issuer[3].split('=')[-1].strip()
            else:
                results[counter]['Common Name'] = issuer[2].strip()
        elif 'notBefore' in line:
            creation = line.split('=')
            results[counter]['Not Before'] = creation[1].strip()
        elif 'notAfter' in line:
            expiration = line.split('=')
            results[counter]['Not After'] = expiration[1].strip()
            counter +=1
        elif 'stdin' in line:
            results[counter]['Common Name'] = 'Invalid MYSQL Version'
            results[counter]['Not Before'] = 'Invalid MYSQL Version'
            results[counter]['Not After'] = 'Invalid MYSQL Version'
            counter +=1

with open('mysql_results.csv', 'w', newline='') as csvfile:
    fields = ['IP', 'Common Name', 'Not Before', 'Not After']
    csvwriter = csv.DictWriter(csvfile, fields)
    csvwriter.writeheader()
    for row in results:
        csvwriter.writerow(row)