from nodeconductor.logging.loggers import EventLogger, event_logger
from nodeconductor.structure import models as structure_models

from . import models


class ResourceActionEventLogger(EventLogger):
    resource = structure_models.NewResource
    action_details = dict

    class Meta:
        event_types = (
            'resource_pull_scheduled',
            'resource_pull_succeeded',
            'resource_pull_failed',
            # volume
            'resource_attach_scheduled',
            'resource_attach_succeeded',
            'resource_attach_failed',

            'resource_detach_scheduled',
            'resource_detach_succeeded',
            'resource_detach_failed',

            'resource_extend_scheduled',
            'resource_extend_succeeded',
            'resource_extend_failed',

            # instance
            'resource_update_security_groups_scheduled',
            'resource_update_security_groups_succeeded',
            'resource_update_security_groups_failed',

            'resource_change_flavor_scheduled',
            'resource_change_flavor_succeeded',
            'resource_change_flavor_failed',

            'resource_assign_floating_ip_scheduled',
            'resource_assign_floating_ip_succeeded',
            'resource_assign_floating_ip_failed',

            'resource_stop_scheduled',
            'resource_stop_succeeded',
            'resource_stop_failed',

            'resource_start_scheduled',
            'resource_start_succeeded',
            'resource_start_failed',

            'resource_restart_scheduled',
            'resource_restart_succeeded',
            'resource_restart_failed',
        )
        event_groups = {'resources': event_types}


class BackupScheduleEventLogger(EventLogger):
    resource = models.Instance
    backup_schedule = models.BackupSchedule

    class Meta:
        event_types = (
            'resource_backup_schedule_created',
            'resource_backup_schedule_deleted',
            'resource_backup_schedule_activated',
            'resource_backup_schedule_deactivated',
        )
        event_groups = {'resources': event_types}


event_logger.register('openstack_resource_action', ResourceActionEventLogger)
event_logger.register('openstack_backup_schedule', BackupScheduleEventLogger)
