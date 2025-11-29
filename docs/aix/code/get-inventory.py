import requests
import json
from collections import defaultdict

# Your Skytap "Login name" from the Skytap Portal and API token
login_name='daverendon-monitor'
API_token='0640addf4df485cda044336f138d6160c4b5a636'

base_url = 'https://cloud.skytap.com/'
auth_sky = (login_name,API_token)
http_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Replace with your specific environment (configuration) ID
# Example: https://cloud.skytap.com/configurations/159726802?section=vms&sort=name&thumbnails=shown
environment_id = '188497438'

# Skytap API endpoint to get the environment details
url = f'https://cloud.skytap.com/v2/configurations/{environment_id}'

response = requests.get(url, headers=http_headers, auth=auth_sky)

# Check if the request was successful
if response.status_code == 200:
    environment_data = response.json()
    print('Environment Details:')

    # Extract the VMs (LPARs) from the environment data
    vms = environment_data.get('vms', [])

    table_headers = [
        '#',
        'VM ID',
        'Name',
        'Status',
        'OS',
        'vCPUs',
        'Memory',
        'Storage',
        'MAS Storage',
        'EC'
    ]
    table_alignments = ['right', 'left', 'left', 'left', 'left', 'right', 'right', 'right', 'right', 'right']
    rows = []

    total_vcpus = 0
    total_memory_gb = 0.0
    total_storage_gb = 0.0
    total_entitled_capacity = 0.0

    multi_attach_total_mb = 0.0
    vm_multi_attach_mb = defaultdict(float)

    def normalize_mas_groups(raw_groups):
        if raw_groups is None:
            return []
        if isinstance(raw_groups, dict):
            possible_list = raw_groups.get('multi_attach_storage_groups')
            if isinstance(possible_list, list):
                return possible_list
            return []
        if isinstance(raw_groups, list):
            return raw_groups
        return []

    mas_groups = normalize_mas_groups(environment_data.get('multi_attach_storage_groups'))

    if not mas_groups:
        mas_url = f'https://cloud.skytap.com/v2/configurations/{environment_id}/multi_attach_storage_groups'
        mas_response = requests.get(mas_url, headers=http_headers, auth=auth_sky)
        if mas_response.status_code == 200:
            mas_groups = normalize_mas_groups(mas_response.json())

    for group in mas_groups:
        allocations = group.get('storage_allocations', [])
        group_total_mb = 0.0
        for allocation in allocations:
            size_mb = allocation.get('size')
            if isinstance(size_mb, (int, float)):
                group_total_mb += size_mb
        if group_total_mb:
            multi_attach_total_mb += group_total_mb
            for attached_vm_id in group.get('vm_attachments', []):
                vm_multi_attach_mb[attached_vm_id] += group_total_mb

    for index, vm in enumerate(vms, start=1):
        vm_id = vm.get('id', 'N/A')
        name = vm.get('name', 'N/A')
        status = vm.get('runstate', 'N/A')

        hardware = vm.get('hardware', {})
        settings = hardware.get('settings', {})

        os = hardware.get('guestOS', 'N/A')

        vcpus_value = settings.get('cpus', {}).get('current')
        if isinstance(vcpus_value, (int, float)):
            total_vcpus += vcpus_value
            vcpus_display = f"{vcpus_value}"
        else:
            vcpus_display = 'N/A'

        memory_mb = settings.get('ram', {}).get('current')
        if isinstance(memory_mb, (int, float)):
            memory_gb = memory_mb / 1024
            total_memory_gb += memory_gb
            memory_display = f"{memory_gb:.2f} GB"
        else:
            memory_display = 'N/A'

        storage_gb = 0.0
        for disk in hardware.get('disks', []):
            disk_size = disk.get('size')
            if isinstance(disk_size, (int, float)):
                storage_gb += disk_size / 1024
        total_storage_gb += storage_gb
        storage_display = f"{storage_gb:.2f} GB" if storage_gb else '0.00 GB'

        mas_storage_mb = vm_multi_attach_mb.get(vm_id, 0.0)
        mas_storage_gb = mas_storage_mb / 1024 if mas_storage_mb else 0.0
        mas_display = f"{mas_storage_gb:.2f} GB" if mas_storage_gb else '0.00 GB'

        entitled_capacity_value = settings.get('entitled_capacity', {}).get('current')
        if isinstance(entitled_capacity_value, (int, float)):
            total_entitled_capacity += entitled_capacity_value
            entitled_capacity_display = f"{entitled_capacity_value:.2f}"
        else:
            entitled_capacity_display = '0.00'

        rows.append([
            f"{index}",
            f"{vm_id}",
            f"{name}",
            f"{status}",
            f"{os}",
            vcpus_display,
            memory_display,
            storage_display,
            mas_display,
            entitled_capacity_display
        ])

    total_vms = len(rows)
    total_storage_tb = total_storage_gb / 1024 if total_storage_gb else 0.0
    multi_attach_total_gb = multi_attach_total_mb / 1024 if multi_attach_total_mb else 0.0
    multi_attach_total_tb = multi_attach_total_gb / 1024 if multi_attach_total_gb else 0.0

    rows.append([
        'TOTAL',
        '',
        '',
        '',
        '',
        f"{total_vcpus}",
        f"{total_memory_gb:.2f} GB",
        f"{total_storage_gb:.2f} GB",
        f"{multi_attach_total_gb:.2f} GB",
        f"{total_entitled_capacity:.2f}"
    ])

    rows.append([
        'SUMMARY',
        'Total VMs',
        f"{total_vms}",
        '',
        '',
        '',
        f"{total_memory_gb:.2f} GB",
        f"{total_storage_tb:.2f} TB",
        f"{multi_attach_total_tb:.2f} TB",
        f"{total_entitled_capacity:.2f}"
    ])

    column_widths = []
    for idx, header in enumerate(table_headers):
        max_cell_width = max(len(row[idx]) for row in rows) if rows else 0
        column_widths.append(max(len(header), max_cell_width))

    def format_cell(value, width, alignment):
        if alignment == 'right':
            return value.rjust(width)
        if alignment == 'center':
            return value.center(width)
        return value.ljust(width)

    def alignment_rule(width, alignment):
        width = max(width, 2)
        if alignment == 'right':
            return '-' * (width - 1) + ':'
        if alignment == 'center':
            inner_width = width - 2
            inner = '-' * inner_width if inner_width > 0 else ''
            return ':' + inner + ':'
        return ':' + '-' * (width - 1)

    header_line = '| ' + ' | '.join(
        format_cell(table_headers[idx], column_widths[idx], table_alignments[idx])
        for idx in range(len(table_headers))
    ) + ' |'

    separator_line = '| ' + ' | '.join(
        alignment_rule(column_widths[idx], table_alignments[idx])
        for idx in range(len(table_headers))
    ) + ' |'

    data_lines = []
    for row in rows:
        data_lines.append(
            '| ' + ' | '.join(
                format_cell(row[idx], column_widths[idx], table_alignments[idx])
                for idx in range(len(table_headers))
            ) + ' |'
        )

    markdown_table = '\n'.join([header_line, separator_line] + data_lines)

    print(markdown_table)
    print(f"\nTotal VMs: {total_vms}")
else:
    print('Failed to retrieve environment details')
    print('Status Code:', response.status_code)
    print('Response:', response.text)