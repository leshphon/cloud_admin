import vdc_module.api.keystone.interface as keystoneclient


def checkAction(user):
    if keystoneclient.authentication.check(user).enabled is False:
        return None
    else:
        return status2action


status2action = {
    "ACTIVE": [
        {
            "action": "Create snapshot",
            "role": "all",
            "href": "/vdc_snapshotServer",
            # "addition_fields": ["snapshot_name", "metadata"]
        },
        {
            "action": "Edit",
            "role": "all",
            "href": "/vdc_updateServer",
            # "addition_fields": ["accessIPv4", "accessIPv6", "OS-DCF_diskConfig", ]
        },
        {
            "action": "Pause",
            "role": "all",
            "href": "/vdc_pauseServer"
        },
        {
            "action": "Suspend",
            "role": "all",
            "href": "/vdc_suspendServer"
        },
        {
            "action": "Shelve",
            "role": "all",
            "href": "/vdc_shelveServer"
        },
        {
            "action": "Resize",
            "role": "all",
            "href": "/vdc_resizeServer"
        },
        {
            "action": "Lock",
            "role": "all",
            "href": "/vdc_lockServer"
        },
        {
            "action": "Unlock",
            "role": "all",
            "href": "/vdc_unlockServer"
        },
        {
            "action": "Soft reboot",
            "role": "all",
            "href": "/vdc_softRebootServer"
        },
        {
            "action": "Hard reboot",
            "role": "all",
            "href": "/vdc_hardRebootServer"
        },
        {
            "action": "Shutoff",
            "role": "all",
            "href": "/vdc_shutServer"
        },
        {
            "action": "Rebuild",
            "role": "all",
            "href": "/vdc_rebuildServer"
        },
        {
            "action": "Delete",
            "role": "all",
            "href": "/vdc_deleteServer"
        },
        {
            "action": "Migrate Server",  # admin
            "role": "admin",
            "href": "/vdc_migrateServer"
        },
        {
            "action": "Live-Migrate Server",  # admin
            "role": "admin",
            "href": "/vdc_livemigrateServer"
        },
    ],
    "PAUSED": [
        {
            "action": "Create snapshot",
            "role": "all",
            "href": "/vdc_snapshotServer"
        },
        {
            "action": "Edit",
            "role": "all",
            "href": "/vdc_updateServer"
        },
        {
            "action": "Resume paused",
            "role": "all",
            "href": "/vdc_unpauseServer"
        },
        {
            "action": "Shelve",
            "role": "all",
            "href": "/vdc_shelveServer"
        },
        {
            "action": "Lock",
            "role": "all",
            "href": "/vdc_lockServer"
        },
        {
            "action": "Unlock",
            "role": "all",
            "href": "/vdc_unlockServer"
        },
        {
            "action": "Delete",
            "role": "all",
            "href": "/vdc_deleteServer"
        }
    ],
    "SUSPENDED": [
        {
            "action": "Create snapshot",
            "role": "all",
            "href": "/vdc_snapshotServer"
        },
        {
            "action": "Edit",
            "role": "all",
            "href": "/vdc_updateServer"
        },
        {
            "action": "Resume suspended",
            "role": "all",
            "href": "/vdc_unsuspendServer"
        },
        {
            "action": "Shelve",
            "role": "all",
            "href": "/vdc_shelveServer"
        },
        {
            "action": "Lock",
            "role": "all",
            "href": "/vdc_lockServer"
        },
        {
            "action": "Unlock",
            "role": "all",
            "href": "/vdc_unlockServer"
        },
        {
            "action": "Delete",
            "role": "all",
            "href": "/vdc_deleteServer"
        }
    ],
    "SHUTOFF": [
        {
            "action": "Create snapshot",
            "role": "all",
            "href": "/vdc_snapshotServer"
        },
        {
            "action": "Edit",
            "role": "all",
            "href": "/vdc_updateServer"
        },
        {
            "action": "Start",
            "role": "all",
            "href": "/vdc_startServer"
        },
        {
            "action": "Shelve",
            "role": "all",
            "href": "/vdc_shelveServer"
        },
        {
            "action": "Lock",
            "role": "all",
            "href": "/vdc_lockServer"
        },
        {
            "action": "Unlock",
            "role": "all",
            "href": "/vdc_unlockServer"
        },
        {
            "action": "Delete",
            "role": "all",
            "href": "/vdc_deleteServer"
        },
        {
            "action": "Rebuild",
            "role": "all",
            "href": "/vdc_rebuildServer"
        },
        {
            "action": "Resize",
            "role": "all",
            "href": "/vdc_resizeServer"
        },
        {
            "action": "Hard reboot",
            "role": "all",
            "href": "/vdc_hardRebootServer"
        }
    ],
    "VERIFY_RESIZE": [
        {
            "action": "Confirm resize",
            "role": "all",
            "href": "/vdc_comfirmResizedServer"
        },
        {
            "action": "Revert resize",
            "role": "all",
            "href": "/vdc_revertResizedServer"
        },
        {
            "action": "Edit",
            "role": "all",
            "href": "/vdc_updateServer"
        },
        {
            "action": "Lock",
            "role": "all",
            "href": "/vdc_lockServer"
        },
        {
            "action": "Unlock",
            "role": "all",
            "href": "/vdc_unlockServer"
        },
        {
            "action": "Shutoff",
            "role": "all",
            "href": "/vdc_shutServer"
        },
        {
            "action": "Delete",
            "role": "all",
            "href": "/vdc_deleteServer"
        }
    ],
    "SHELVED_OFFLOADED": [
        {
            "action": "Edit",
            "role": "all",
            "href": "/vdc_updateServer"
        },
        {
            "action": "Resume SHELVED",
            "role": "all",
            "href": "/vdc_unshelveServer"
        },
        {
            "action": "Lock",
            "role": "all",
            "href": "/vdc_lockServer"
        },
        {
            "action": "Unlock",
            "role": "all",
            "href": "/vdc_unlockServer"
        },
        {
            "action": "Delete",
            "role": "all",
            "href": "/vdc_deleteServer"
        }

    ],
    "OTHER": [
        {
            "action": "Edit",
            "role": "all",
            "href": "/vdc_updateServer"
        },
        {
            "action": "Lock",
            "role": "all",
            "href": "/vdc_lockServer"
        },
        {
            "action": "Unlock",
            "role": "all",
            "href": "/vdc_unlockServer"
        },
        {
            "action": "Delete",
            "role": "all",
            "href": "/vdc_deleteServer"
        }
    ]
}

# admin_action2status = {
#     # If the server is locked, you must have administrator privileges to handle the server.
#
#     'status': ['SHUTOFF', 'ACTIVE', 'PAUSED', 'SUSPENDED', 'RESCUE', 'SHELVED', 'SHELVED_OFFLOADED', 'ERROR',
#                'BUILDING', 'SOFT_DELETED', 'VERIFY_RESIZE', 'RESIZED', 'shutoff', 'active', 'paused', 'suspended',
#                'rescue', 'shelved', 'shelved_offloaded', 'error', 'building', 'soft_deleted', 'resized'],
#
#     'update': ['ACTIVE', 'SHUTOFF', 'PAUSED', 'SUSPENDED', 'shutoff', 'active', 'paused', 'suspended'],
#     'delete': ['ALL', 'all'],
#
#     'lock': ['ALL', 'all'],
#     'unlock': ['ALL', 'all'],
#
#     'shelve': ['ACTIVE', 'SHUTOFF', 'PAUSED', 'SUSPENDED', 'shutoff', 'active', 'paused', 'suspended'],
#     'unshelve': ['SHELVED', 'shelved', 'SHELVED_OFFLOADED', 'shelved_offloaded'],
#     'shelved_offload': ['SHELVED', 'shelved'],
#
#     'pause': ['ACTIVE', 'RESCUE', 'SHUTOFF', 'active', 'rescue', 'shutoff'],
#     'unpause': ['PAUSED', 'paused'],
#
#     'suspend': ['ACTIVE', 'SHUTOFF', 'active', 'shutoff'],
#     'unsuspend': ['SUSPENDED', 'suspended'],
#
#     'rescue': ['ACTIVE', 'SHUTOFF', 'active', 'shutoff'],
#     'unrescue': ['RESCUE', 'rescue'],
#
#     'rebuild': ['ACTIVE', 'SHUTOFF', 'shutoff', 'active'],
#
#     'snapshot': ['ACTIVE', 'SHUTOFF', 'PAUSED', 'SUSPENDED', 'shutoff', 'active', 'paused', 'suspended'],
#
#     'start': ['SHUTOFF', 'shutoff'],
#     'stop': ['ACTIVE', 'ERROR', 'active', 'error'],
#
#     'softreboot': ['ACTIVE', 'RESCUE', 'SHUTOFF', 'active', 'rescue', 'shutoff'],
#     'hardreboot': ['ACTIVE', 'RESCUE', 'SHUTOFF', 'active', 'rescue', 'shutoff'],
#
#     'resize': ['ACTIVE', 'active', 'SHUTOFF', 'shutoff'],
#     'revert_resize': ['ACTIVE', 'active', 'SHUTOFF', 'shutoff'],
#     'confirm_resize': ['ACTIVE', 'active', 'SHUTOFF', 'shutoff']

# 'set_admin_password': ['ACTIVE', 'active'],
# 'force_delete': ['SOFT_DELETED', 'soft_deleted'],
# 'restore': ['SOFT_DELETED', 'soft_deleted'],
# 'soft_delete': ['ACTIVE', 'SHUTOFF', 'ERROR', 'active', 'shutoff', 'error'],
# 'backup': ['SHUTOFF', 'ACTIVE', 'shutoff', 'active']
# }
