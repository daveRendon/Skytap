import requests
from requests.auth import HTTPBasicAuth
import uuid

# Skytap API credentials
login_name = 'your_login_name'
API_token = 'your_API_token'

base_url = 'https://cloud.skytap.com'
auth_sky = HTTPBasicAuth(login_name, API_token)
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Replace this with your Environment (configuration) ID
ENVIRONMENT_ID = '160281144'

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
    if response.status_code == 404:
        print("Error 404: Multi-attach storage group creation endpoint not found.")
        return None
    response.raise_for_status()
    return response.json()

def add_storage_allocations(new_storage_id, storage_allocations):
    allocation_url = f"{base_url}/v2/multi_attach_storage_groups/{new_storage_id}/storage_allocations"
    allocation_ids = []
    
    for allocation in storage_allocations:
        allocation_payload = {
            "spec": {
                "volume": [allocation['size']]
            }
        }

        print(f"\nSending storage allocation payload for {new_storage_id}:\n{allocation_payload}")

        response = requests.post(allocation_url, headers=headers, auth=auth_sky, json=allocation_payload)
        if response.status_code == 404:
            print("Error 404: Storage allocation endpoint not found.")
            continue
        response.raise_for_status()
        
        added_allocation = response.json()
        allocation_id = added_allocation.get('id')
        allocation_size = added_allocation.get('size', 'Unknown size')
        if allocation_id:
            print(f"  Added Allocation ID: {allocation_id}, Size: {allocation_size} MB")
            allocation_ids.append(allocation_id)
        else:
            print("  Warning: Allocation ID missing in response.")

        for attachment in allocation.get('disk_attachments', []):
            add_disk_attachment(new_storage_id, allocation_id, attachment)

    return allocation_ids

def add_disk_attachment(storage_id, allocation_id, attachment):
    attachment_url = f"{base_url}/v2/multi_attach_storage_groups/{storage_id}/storage_allocations/{allocation_id}/disk_attachments"
    attachment_payload = {
        'controller': attachment['controller'],
        'bus_type': attachment['bus_type'],
        'bus_id': attachment['bus_id'],
        'lun': attachment['lun']
    }
    print(f"Adding disk attachment with payload:\n{attachment_payload}")
    
    response = requests.post(attachment_url, headers=headers, auth=auth_sky, json=attachment_payload)
    if response.status_code == 404:
        print("Error 404: Disk attachment endpoint not found.")
        return None
    response.raise_for_status()
    
    added_attachment = response.json()
    print(f"  Added Disk Attachment ID: {added_attachment['id']}")
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
            for storage in multi_attach_storage:
                print(f"  Original Storage Group ID: {storage['id']}, Name: {storage['name']}, Configuration ID: {storage['configuration_id']}")
                
                copied_storage = create_multi_attach_storage(storage)
                if copied_storage is None:
                    print("Copy of multi-attach storage group could not be created.")
                    continue

                print(f"  Copied Storage Group ID: {copied_storage['id']}, Name: {copied_storage['name']}")

                # Add storage allocations and disk attachments, and print results
                copied_allocation_ids = add_storage_allocations(copied_storage['id'], storage.get('storage_allocations', []))
                print(f"  Completed copying storage allocations for group ID {copied_storage['id']}. Allocations copied: {copied_allocation_ids}")

        else:
            print("No multi-attach storage configurations found.")
            
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 404:
            print("HTTP 404 Error: Resource not found.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()
