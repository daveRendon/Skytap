import requests
from requests.auth import HTTPBasicAuth
import json

# Your Skytap "Login name" from the Skytap Portal and API token
login_name='daverendon-monitor'
API_token='0640addf4df485cda044336f138d6160c4b5a636'

base_url = 'https://cloud.skytap.com/'
auth_sky = (login_name,API_token)
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Replace with your specific environment (configuration) ID
# Example: https://cloud.skytap.com/configurations/159726802?section=vms&sort=name&thumbnails=shown
environment_id = '188497438'

# Skytap API endpoint to get the environment details
url = f'https://cloud.skytap.com/v2/configurations/{environment_id}'

response = requests.get(url, headers=headers,auth=auth_sky)

# Check if the request was successful
if response.status_code == 200:
    environment_data = response.json()
    print('Environment Details:')
    # Pretty print the entire environment data for debugging
    # print(json.dumps(environment_data, indent=2))  
    
    # Extract the VMs (LPARs) from the environment data
    vms = environment_data.get('vms', [])
    
   # Initialize markdown table with EC column
    markdown_table = "| VM ID            | Name               | Status     | OS                  | vCPUs | Memory (GB) | Storage (GB) | EC     |\n"
    markdown_table += "|------------------|--------------------|------------|---------------------|-------|-------------|--------------|--------|\n"
    
    total_vcpus = 0
    total_memory_gb = 0
    total_storage_gb = 0
    total_entitled_capacity = 0

    for vm in vms:
        vm_id = vm.get('id', 'N/A')
        name = vm.get('name', 'N/A')
        status = vm.get('runstate', 'N/A')
        
        hardware = vm.get('hardware', {})
        settings = hardware.get('settings', {})
        
        os = hardware.get('guestOS', 'N/A')
        vcpus = settings.get('cpus', {}).get('current', 'N/A')
        memory_mb = settings.get('ram', {}).get('current', 'N/A')
        
        # Convert memory from MB to GB
        memory_gb = memory_mb / 1024 if memory_mb != 'N/A' else 'N/A'

        # Calculate total storage in GB
        storage_gb = 0
        for disk in hardware.get('disks', []):
            storage_gb += disk.get('size', 0) / 1024

        # Extract Entitled Capacity (EC)
        entitled_capacity = settings.get('entitled_capacity', {}).get('current', 0)
        
        # Update totals
        total_vcpus += vcpus
        total_memory_gb += memory_gb
        total_storage_gb += storage_gb
        total_entitled_capacity += entitled_capacity
        
        # Append row to markdown table
        markdown_table += f"| {vm_id:<16} | {name:<18} | {status:<10} | {os:<19} | {vcpus:<5} | {memory_gb:<11.2f} | {storage_gb:<12.2f} | {entitled_capacity:<6.2f} |\n"
    
    # Convert total storage from GB to TB
    total_storage_tb = total_storage_gb / 1024

   # Append totals to the markdown table
    markdown_table += "|------------------|--------------------|------------|---------------------|-------|-------------|--------------|--------|\n"
    markdown_table += f"| {'TOTAL':<16} | {'':<18} | {'':<10} | {'':<19} | {total_vcpus:<5} | {total_memory_gb:<11.2f} | {total_storage_tb:<9.2f} TB | {total_entitled_capacity:<6.2f} |\n"

    # Print the markdown table
    print(markdown_table)
else:
    print('Failed to retrieve environment details')
    print('Status Code:', response.status_code)
    print('Response:', response.text)