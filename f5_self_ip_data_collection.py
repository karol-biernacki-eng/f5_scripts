import requests
import json

# BIG-IP device details
device_ip = '192.168.0.65'
username = 'admin'
password = 'karol1985'

# List of BIG-IP devices
bigip_devices = [
    {
        'ip': device_ip,
        'username': username,
        'password': password
    },
    {
        'ip': device_ip,
        'username': username,
        'password': password
    },
    # Add more devices as needed
]

# API endpoint to get self IPs
api_endpoint = '/mgmt/tm/net/self'

for device in bigip_devices:
    # Construct the full API URL
    url = f'https://{device["ip"]}{api_endpoint}'

    # Send GET request to the API endpoint
    response = requests.get(url, auth=(device['username'], device['password']), verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        self_ips = response.json()['items']

        # Extract the IP addresses from the response
        ip_addresses = [self_ip['address'] for self_ip in self_ips]

        # Print the IP addresses
        for ip_address in ip_addresses:
            print(ip_address, device['ip'])
    else:
        print(f"Failed to retrieve self IPs for {device['ip']}. Status code: {response.status_code}")
