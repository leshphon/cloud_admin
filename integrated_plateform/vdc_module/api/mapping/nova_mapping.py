# coding=utf-8
create_server_key2key = {
    "0": "OS-SCH-HNT:scheduler_hints/same_host",
    "1": "server_description",
    "10": "server_user_data",
    "11": "server_accessIPv4",
    "12": "server_accessIPv6",
    "13": "block_device_mapping_v2_disk_bus",
    "14": "block_device_mapping_v2_source_type",
    "15": "block_device_mapping_v2_guest_format",
    "16": "block_device_mapping_v2_boot_index",
    "17": "block_device_mapping_v2_uuid",
    "18": "block_device_mapping_v2_destination_type",
    "19": "block_device_mapping_v2_tag",
    "2": "server_name",
    "20": "block_device_mapping_v2_delete_on_termination",
    "21": "block_device_mapping_v2_device_name",
    "22": "server_config_drive",
    "23": "server_key_name",
    "24": "server_tags",
    "25": "server_metadata",
    "26": "security_groups_name",
    "27": "network_fixed_ip",
    "28": "network_tag",
    "29": "network_uuid",
    "3": "server_imageRef",
    "30": "network_port",
    "31": "min_count",
    "32": "return_reservation_id",
    "33": "max_count",
    "4": "server_adminPass",
    "5": "personality_path",
    "6": "personality_contents",
    "7": "server_flavorRef",
    "8": "server_availability_zone",
    "9": "server_OS-DCF:diskConfig"
}
create_server_key2path = {
    "0": "OS-SCH-HNT:scheduler_hints/same_host",
    "1": "server/description",
    "10": "server/user_data",
    "11": "server/accessIPv4",
    "12": "server/accessIPv6",
    "13": "server/block_device_mapping_v2[/disk_bus",
    "14": "server/block_device_mapping_v2[/source_type",
    "15": "server/block_device_mapping_v2[/guest_format",
    "16": "server/block_device_mapping_v2[/boot_index",
    "17": "server/block_device_mapping_v2[/uuid",
    "18": "server/block_device_mapping_v2[/destination_type",
    "19": "server/block_device_mapping_v2[/tag",
    "2": "server/name",
    "20": "server/block_device_mapping_v2[/delete_on_termination",
    "21": "server/block_device_mapping_v2[/device_name",
    "22": "server/config_drive",
    "23": "server/key_name",
    "24": "server/tags",
    "25": "server/metadata",
    "26": "server/security_groups[/name",
    "27": "server/network[/fixed_ip",
    "28": "server/network[/tag",
    "29": "server/network[/uuid",
    "3": "server/imageRef",
    "30": "server/network[/port",
    "31": "server/min_count",
    "32": "server/return_reservation_id",
    "33": "server/max_count",
    "4": "server/adminPass",
    "5": "server/personality[/path",
    "6": "server/personality[/contents",
    "7": "server/flavorRef",
    "8": "server/availability_zone",
    "9": "server/OS-DCF:diskConfig"
}


update_key2key = {
    "0": "accessIPv4",
    "1": "accessIPv6",
    "2": "OS-DCF:diskConfig",
    "3": "name",
    "4": "server/description"
}
update_key2path = {
    "0": "server/accessIPv4",
    "1": "server/accessIPv6",
    "2": "server/OS-DCF:diskConfig",
    "3": "server/name",
    "4": "server/description"
}

snapshot_key2key = {'1': 'metadata', '0': 'snapshot_name'}
snapshot_key2path = {'1': 'createImage/metadata', '0': 'createImage/name'}


create_flavors_key2key = {
    '1': 'flavor_disk',
    '0': 'flavor_vcpus',
    '3': 'flavor_os-flavor-access:is_public',
    '2': 'flavor_name',
    '5': 'flavor_ram',
    '4': 'flavor_rxtx_factor',
    '7': 'flavor_description',
    '6': 'flavor_id'
}
create_flavors_key2path = {
    '1': 'flavor/disk',
    '0': 'flavor/vcpus',
    '3': 'flavor/os-flavor-access:is_public',
    '2': 'flavor/name',
    '5': 'flavor/ram',
    '4': 'flavor/rxtx_factor',
    '7': 'flavor/description',
    '6': 'flavor/id'
}


rebuild_server_key2key = {
    "2": "name",
    "3": "imageRef",
    "4": "adminPass",
    "5": "key_name",
    "6": "metadata",
    "7": "OS-DCF:diskConfig",
    "8": "description"
}
rebuild_server_key2path = {
    "0": "rebuild/accessIPv4",
    "1": "rebuild/accessIPv6",
    "2": "rebuild/name",
    "3": "rebuild/imageRef",
    "4": "rebuild/adminPass",
    "5": "rebuild/key_name",
    "6": "rebuild/metadata",
    "7": "rebuild/OS-DCF:diskConfig",
    "8": "rebuild/description"
}


rescue_server_key2key = {
    "0": "rescue_image_ref",
    "1": "adminPass"
}
rescue_server_key2path = {
    "0": "rescue/rescue_image_ref",
    "1": "rescue/adminPass"
}


resize_server_key2key = {
    "0": "flavorRef",
    "1": "OS-DCF:diskConfig"
}
resize_server_key2path = {
    "0": "resize/flavorRef",
    "1": "resize/OS-DCF:diskConfig"
}


create_servermeta_key2key = {
    "0": "metadata"
}
create_servermeta_key2path = {
    "0": "metadata"
}


create_keypairs_key2key = {

    "0": "public_key",
    "1": "type",
    "2": "name",
    "3": "user_id"
}
create_keypairs_key2path = {

    "0": "keypair/public_key",
    "1": "keypair/type",
    "2": "keypair/name",
    "3": "keypair/user_id"
}
