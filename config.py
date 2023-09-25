"""
Configuration file, containing variables used throughout the rest of the script for easy editng and maintenance.
Files are lists of relative filepaths to the source files
Networks are lists of IP ranges written in CIDR notation 
Port ranges are lists of strings containing the target port ranges in the format start-end
Ports are lists of integers
Hosts are dictionaries with key-value pairs of domain(string):ip(string)
"""

# source_files = 'test.csv'

# allowlist
# target_networks = [
#     '127.0.0.1/32',
# ]
# target_port_ranges = [
#     '0-127',
# ]
# target_ports = [
#     0,
# ] 
# target_hosts = {
#     'domainhere.tld':'127.0.0.1',
# } 

# blocklist
# excluded_networks = [
#     '127.0.0.1/32',
# ]
# excluded_port_ranges = [
#     '0-127',
# ]
# excluded_ports = [
#     0,
# ]
# excluded_hosts = {
#     'domainhere.tld':'127.0.0.1',
# }