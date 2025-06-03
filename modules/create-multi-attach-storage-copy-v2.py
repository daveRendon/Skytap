import requests
from requests.auth import HTTPBasicAuth
import uuid
import sys
import time

# Skytap API credentials
login_name = 'your-login-name'  # e.g., 'daverendon_admin'
API_token = 'your-api-token'

base_url = 'https://cloud.skytap.com'
auth_sky = HTTPBasicAuth(login_name, API_token)
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

ENVIRONMENT_ID = '187094628'

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=40, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()

def get_environment(environment_id):
    url = f'{base_url}/v2/configurations/{environment_id}'
    response = requests.get(url, headers=headers, auth=auth_sky)
    if response.status_code == 404:
        print("Error 404: Environment not found.")
        return None
    response.raise_for_status()
    return response.json()

def get_multi_attach_storage(environment):
    return environment.get('multi_attach_storage_groups', [])

def get_storage_group(storage_group_id):
    url = f"{base_url}/v2/multi_attach_storage_groups/{storage_group_id}"
    response = requests.get(url, headers=headers, auth=auth_sky)
    if response.status_code == 404:
        print("Error 404: Storage group not found.")
        return None
    response.raise_for_status()
    return response.json()

def create_multi_attach_storage(storage):
    unique_name = f"{storage['name']}-copy-{uuid.uuid4()}"
    payload = {
        'name': unique_name,
        'configuration_id': storage['configuration_id'],
        'hypervisor': storage['hypervisor'],
        'vm_attachments': storage.get('vm_attachments', [])
    }
    post_url = f"{base_url}/v2/configurations/{ENVIRONMENT_ID}/multi_attach_storage_groups"
    print(f"Creating multi-attach storage group with payload:\n{payload}")
    response = requests.post(post_url, headers=headers, auth=auth_sky, json=payload)
    if response.status_code == 409:
        print("Error 409: Multi-attach storage group already exists. Skipping creation.")
        return None
    if response.status_code == 404:
        print("Error 404: Multi-attach storage group creation endpoint not found.")
        return None
    response.raise_for_status()
    return response.json()

def add_storage_allocations(new_storage_id, storage_allocations):
    allocation_url = f"{base_url}/v2/multi_attach_storage_groups/{new_storage_id}/storage_allocations"
    sizes = [alloc['size'] for alloc in storage_allocations]
    allocation_payload = {
        "spec": {
            "volume": sizes
        }
    }
    print(f"\nSending storage allocation payload for {new_storage_id}:\n{allocation_payload}")
    response = requests.post(allocation_url, headers=headers, auth=auth_sky, json=allocation_payload)
    if response.status_code == 404:
        print("Error 404: Storage allocation endpoint not found.")
        return []
    response.raise_for_status()
    # After creation, fetch the new storage group to get the real allocation IDs and VM attachments
    new_group = get_storage_group(new_storage_id)
    if not new_group or 'storage_allocations' not in new_group:
        print("Could not fetch new storage allocations.")
        return []
    new_allocs = new_group['storage_allocations']
    vm_attachments = new_group.get('vm_attachments', [])
    allocation_ids = []
    total_allocs = len(new_allocs)
    for idx, (orig_alloc, new_alloc) in enumerate(zip(storage_allocations, new_allocs), 1):
        allocation_id = new_alloc.get('id')
        allocation_size = new_alloc.get('size', 'Unknown size')
        print(f"  Added Allocation ID: {allocation_id}, Size: {allocation_size} MB")
        allocation_ids.append(allocation_id)
        print_progress_bar(idx, total_allocs, prefix='Allocations Progress', suffix='Complete')
        # Only attach disks if there are VM attachments
        if vm_attachments:
            total_disks = len(orig_alloc.get('disk_attachments', []))
            for disk_idx, attachment in enumerate(orig_alloc.get('disk_attachments', []), 1):
                # Only attach if the VM is in the new group's vm_attachments (if vm_key is present)
                if 'vm_key' in attachment:
                    vm_id = attachment['vm_key'].split('-')[-1]
                    if vm_id not in vm_attachments:
                        continue
                attachment_payload = {
                    'controller': attachment.get('controller'),
                    'bus_type': attachment.get('bus_type'),
                    'bus_id': attachment.get('bus_id'),
                    'lun': attachment.get('lun')
                }
                add_disk_attachment(new_storage_id, allocation_id, attachment_payload)
                print_progress_bar(disk_idx, total_disks, prefix='  Disk Attach Progress', suffix='Complete')
        else:
            print("  Skipping disk attachment: no VM attachments in new storage group.")
    return allocation_ids

def add_disk_attachment(storage_id, allocation_id, attachment):
    if not allocation_id or not allocation_id.startswith("storage_allocation-"):
        print(f"  Skipping disk attachment: invalid allocation_id {allocation_id}")
        return None
    attachment_url = f"{base_url}/v2/multi_attach_storage_groups/{storage_id}/storage_allocations/{allocation_id}/disk_attachments"
    print(f"Adding disk attachment with payload:\n{attachment}")
    response = requests.post(attachment_url, headers=headers, auth=auth_sky, json=attachment)
    if response.status_code == 404:
        print("Error 404: Disk attachment endpoint not found.")
        return None
    response.raise_for_status()
    added_attachment = response.json()
    print(f"  Added Disk Attachment ID: {added_attachment.get('id', 'Unknown')}")
    return added_attachment

def main():
    try:
        environment = get_environment(ENVIRONMENT_ID)
        if environment is None:
            print("Environment could not be retrieved.")
            return

        print(f"Environment ID: {environment['id']}")
        print(f"Environment Name: {environment['name']}")

        multi_attach_storage = get_multi_attach_storage(environment)
        if multi_attach_storage:
            print("\nMulti-Attach Storage:")
            total_groups = len(multi_attach_storage)
            for idx, storage in enumerate(multi_attach_storage, 1):
                print_progress_bar(idx-1, total_groups, prefix='Storage Groups Progress', suffix='Complete')
                print(f"  Original Storage Group ID: {storage['id']}, Name: {storage['name']}, Configuration ID: {storage['configuration_id']}")
                copied_storage = create_multi_attach_storage(storage)
                if copied_storage is None:
                    print("Copy of multi-attach storage group could not be created.")
                    continue
                print(f"  Copied Storage Group ID: {copied_storage['id']}, Name: {copied_storage['name']}")
                # Add storage allocations and disk attachments, and print results
                copied_allocation_ids = add_storage_allocations(
                    copied_storage['id'],
                    storage.get('storage_allocations', [])
                )
                print(f"  Completed copying storage allocations for group ID {copied_storage['id']}. Allocations copied: {copied_allocation_ids}")
                print_progress_bar(idx, total_groups, prefix='Storage Groups Progress', suffix='Complete')
        else:
            print("No multi-attach storage configurations found.")

    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 404:
            print("HTTP 404 Error: Resource not found.")
        elif http_err.response.status_code == 409:
            print("HTTP 409 Error: Conflict. Resource may already exist.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()