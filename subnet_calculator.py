"""
subnet_calculator.py: A Python module to calculate subnet details for an IPv4 address.
"""

# Constants
TOTAL_OCTETS_PER_IPv4 = 4
TOTAL_BITS_PER_IPv4_OCTET = 8
TOTAL_BITS_PER_IPv4 = TOTAL_OCTETS_PER_IPv4 * TOTAL_BITS_PER_IPv4_OCTET  # 32
MAX_OCTET_VALUE = 2 ** TOTAL_BITS_PER_IPv4_OCTET # 256

def calculate_subnet_details(ip_with_cidr):
  """
  Calculates subnet details for a given IPv4 address with CIDR notation.

  Args:
      ip_with_cidr (str): The IPv4 address in CIDR notation (e.g., "192.168.1.0/24").

  Returns:
      dict: A dictionary containing subnet details: 
        - Subnet Mask
        - Total Hosts
        - Usable Hosts
        - Block Size
        - Network Address
        - Broadcast address
        - Usable Range
  """
    
  # Split the input into IP and CIDR
  ip, cidr = ip_with_cidr.split('/')
  cidr = int(cidr)
  
  # Calculate subnet mask
  mask_bits = '1' * cidr + '0' * (TOTAL_BITS_PER_IPv4 - cidr)
  subnet_mask = [int(mask_bits[i:i+8], 2) for i in range(0, TOTAL_BITS_PER_IPv4, TOTAL_BITS_PER_IPv4_OCTET)]
  subnet_mask_str = ".".join(map(str, subnet_mask))
  
  # Calculate total hosts
  total_hosts = 2 ** (TOTAL_BITS_PER_IPv4 - cidr)
  
  # Calculate usable hosts (subtract 2 for network and broadcast, unless it's a /31 or /32)
  usable_hosts = total_hosts - 2 if total_hosts > 2 else 0
  
  # Calculate block size (increment in the subnet range)
  block_size = 256 - subnet_mask[3] if cidr > 24 else 2 ** (32 - cidr) // 256
  
  # Convert IP to binary
  ip_parts = list(map(int, ip.split('.')))
  ip_binary = ''.join(f"{part:08b}" for part in ip_parts) # padding of 8 with zeros
  
  # Calculate network address
  network_binary = ip_binary[:cidr] + '0' * (TOTAL_BITS_PER_IPv4 - cidr)
  network_parts = [int(network_binary[i:i+8], 2) for i in range(0, TOTAL_BITS_PER_IPv4, TOTAL_BITS_PER_IPv4_OCTET)]
  network_address = ".".join(map(str, network_parts))
  
  # Calculate broadcast address
  broadcast_binary = ip_binary[:cidr] + '1' * (TOTAL_BITS_PER_IPv4 - cidr)
  broadcast_parts = [int(broadcast_binary[i:i+8], 2) for i in range(0, TOTAL_BITS_PER_IPv4, TOTAL_BITS_PER_IPv4_OCTET)]
  broadcast_address = ".".join(map(str, broadcast_parts))
  
  # Calculate first & last usable addresses
  first_usable = (
    f"{network_parts[0]}.{network_parts[1]}.{network_parts[2]}.{network_parts[3] + 1}"
    if usable_hosts > 0 else "N/A"
  )

  last_usable = (
    f"{broadcast_parts[0]}.{broadcast_parts[1]}.{broadcast_parts[2]}.{broadcast_parts[3] - 1}"
    if usable_hosts > 0 else "N/A"
  )
  
  # Return the results
  return {
    "Subnet Mask": subnet_mask_str,
    "Total Hosts": total_hosts,
    "Usable Hosts": usable_hosts,
    "Block Size": block_size,
    "Network Address": network_address,
    "Broadcast Address": broadcast_address,
    "First Usable Address": first_usable,
    "Last Usable Address": last_usable,
  }