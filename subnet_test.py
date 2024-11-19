#!/usr/bin/python3

# subnet_test.py: A script that tests the subnet_calculator program.

import sys, re
from subnet_calculator import calculate_subnet_details

# Regex for validating IPv4 with CIDR
ipv4_cidr_regex = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(3[0-2]|[12]?[0-9])$"

# Check user arguments
if len(sys.argv) != 2:
  exit("Usage: python3 subnet_test.py <IPv4>") # you can try with 154.71.0.0 as an example

# Validate the IPv4 using the regex
if not re.match(ipv4_cidr_regex, sys.argv[1]):
  exit("Error: Invalid IPv4 with CIDR notation. Example: 192.168.0.1/24")

# Calculate network details
network_details = calculate_subnet_details(sys.argv[1])

# Output results
print(f"Subnetting details for {sys.argv[1]}:\n")
for key, value in network_details.items():
  print(f"- {key}: {value}")
