#!/bin/bash
server_list=$1

# echo 'starting...'

# parsing the CSV
for line in $(grep 'az' $server_list)
do
    # grab the IP address for the server
    server=$(echo $line | awk -F ',' '{print $2}')
    # echo "Scanning $server..."
    echo "Results for: $server" >> mysql_results.txt
    # grab the certificate information from the server.
    openssl s_client -timeout -starttls mysql -connect "$server:3306" | openssl x509 -noout -issuer -subject -dates >> mysql_results.txt 2>&1
    # this will still print some information to the console, but it shouldn't matter
done
# echo 'done!'