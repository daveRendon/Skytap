import requests
from requests.auth import HTTPBasicAuth

# This script attaches a multi-attach storage group to a VM in a Skytap environment.
# It assumes the storage group is already created and available in the environment.
# It also assumes the VM is powered off before attaching the storage group.
# If you need to create a multi-attach storage group, use the create-multi-attach-storage-copy.py script first.
# You need your Skytap API credentials, the environment ID where the VM and storage group are located, and the VM ID to which you want to attach the storage group.

# Skytap API credentials
login_name = 'your-login-name'  # e.g., 'daverendon_admin'
API_token = 'your-api-token'  

base_url = 'https://cloud.skytap.com'
auth_sky = HTTPBasicAuth(login_name, API_token)
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Replace this with your Environment (configuration) ID
ENVIRONMENT_ID = '185625238'  # e.g., '170350838'

def get_environment(environment_id):
    url = f'{base_url}/v2/configurations/{environment_id}'
    response = requests.get(url, headers=headers, auth=auth_sky)
    if response.status_code == 404:
        print("Error 404: Environment not found.")
        return None
    response.raise_for_status()
    return response.json()

def get_multi_attach_storage(environment):
    multi_attach_storage = environment.get('multi_attach_storage_groups', [])
    if not multi_attach_storage:
        print("No multi-attach storage groups found in the environment.")
    return multi_attach_storage

def list_vms(environment):
    vms = environment.get('vms', [])
    if not vms:
        print("No VMs found in the environment.")
        return []
    print("Available VMs:")
    for vm in vms:
        print(f"  VM ID: {vm['id']}, VM Name: {vm['name']}, State: {vm['runstate']}")
    return vms

def find_last_copied_storage_group(storage_groups):
    # Sort storage groups by name (assuming the naming convention indicates the latest copy)
    sorted_storage = sorted(storage_groups, key=lambda sg: sg['name'], reverse=True)
    for storage in sorted_storage:
        if '-copy-' in storage['name']:
            return storage
    print("No copied storage groups found.")
    return None

def attach_multi_attach_storage_to_vm(storage_id, vm_id):
    if not vm_id:
        print("Error: VM ID is not specified or invalid.")
        return None

    # Ensure the VM is powered off before attaching the storage group
    vm_url = f"{base_url}/v2/vms/{vm_id}"
    vm_response = requests.get(vm_url, headers=headers, auth=auth_sky)
    vm_response.raise_for_status()
    vm = vm_response.json()

    if vm['runstate'] != 'stopped':
        print(f"Error: VM {vm_id} must be powered off to attach the storage group.")
        return None

    attach_url = f"{base_url}/v2/multi_attach_storage_groups/{storage_id}/vm_attachments"
    payload = {
        'vm_ids': [vm_id]  # Note the use of 'vm_ids' as a list
    }
    print(f"Attaching storage group {storage_id} to VM {vm_id} with payload:\n{payload}")
    response = requests.post(attach_url, headers=headers, auth=auth_sky, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while attaching storage: {http_err.response.status_code} - {http_err.response.text}")
        return None
    print(f"Successfully attached storage group {storage_id} to VM {vm_id}.")
    return response.json()

def main():
    try:
        # Fetch environment details
        environment = get_environment(ENVIRONMENT_ID)
        if environment is None:
            return

        print(f"Environment ID: {environment['id']}")
        print(f"Environment Name: {environment['name']}")

        # List VMs in the environment
        vms = list_vms(environment)
        if not vms:
            print("No VMs available in this environment.")
            return

        # Select a VM (modify logic if needed to select a specific VM)
        #vm_id = vms[1]['id']  # Example: Use the first VM in the list
        vm_id = '125505222' #specify the VM ID directly
        print(f"Using VM ID: {vm_id}")

        # Fetch multi-attach storage groups
        multi_attach_storage = get_multi_attach_storage(environment)
        if not multi_attach_storage:
            return

        # Find the last copied storage group
        last_copied_storage = find_last_copied_storage_group(multi_attach_storage)
        if not last_copied_storage:
            print("No copied storage group found.")
            return

        print(f"Last copied storage group found: ID = {last_copied_storage['id']}, Name = {last_copied_storage['name']}")

        # Attach the last copied storage group to the VM
        attach_multi_attach_storage_to_vm(last_copied_storage['id'], vm_id)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()
