# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#
from model.task.completion_status import CompletionStatus

from enum import Enum, unique

@unique
class SafeGuardTaskType(Enum):
    unknown                       = 0
    # 'export' is deprecated, use export_s3_* instead
    export                        = 1
    # Server uses 'import', but that value is reserved in Python
    volume_import                 = 2
    # 'incremental' is deprecated, use export_replica_incremental instead
    incremental                   = 3
    # 'snapshot' is deprecated, use export_s3_snapshot or export_remoteclone_snapshot instead
    snapshot                      = 4
    export_remoteclone_checkpoint = 5
    export_remoteclone_snapshot   = 6
    export_replica_checkpoint     = 7
    export_replica_incremental    = 8
    export_s3_checkpoint          = 9
    export_s3_snapshot            = 10

    def __str__(self):
        '''
        Crucial for converting between json and this enum
        '''
        if self.value == SafeGuardTaskType.volume_import.value:
            return "import"
        return self.name

    @classmethod
    def getTableDisplayString(cls, enum_task_type):
        '''
        Returns
        -------
        :type str
        '''
        if enum_task_type.value == SafeGuardTaskType.volume_import.value:
            return "import"
        if enum_task_type.value == SafeGuardTaskType.export_remoteclone_checkpoint.value:
            return "volume copy"
        if enum_task_type.value == SafeGuardTaskType.export_remoteclone_snapshot.value:
            return "volume snapshot copy"
        if enum_task_type.value == SafeGuardTaskType.export_replica_checkpoint.value:
            return "volume replicate"
        if enum_task_type.value == SafeGuardTaskType.export_replica_incremental.value:
            return "volume incremental replicate"
        if enum_task_type.value == SafeGuardTaskType.export_s3_checkpoint.value:
            return "volume export"
        if enum_task_type.value == SafeGuardTaskType.export_s3_snapshot.value:
            return "volume snapshot export"
        return enum_task_type.name

class SafeGuardTaskStatus(object):
    '''A point-in-time status for a SafeGuard data migration task.

    Attributes
    ----------
    :type __uuid:

    :type __description: string
    :attr __description: A description of the task

    :type __volume_id: int

    :type __status: ``model.task.CompletionStatus``

    :type __task_type: ``model.task.SafeGuardTaskType``
    '''
    def __init__(self, uuid=-1, description=None, volume_id=-1, status=None,
        task_type=None):

        self.uuid = uuid
        self.description = description
        self.volume_id = volume_id
        self.status = status
        if self.status is None:
            self.status = CompletionStatus.unknown
        self.task_type = task_type
        if self.task_type is None:
            self.task_type = SafeGuardTaskType.unknown

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, uuid):
        self.__uuid = uuid

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description
 
    @property
    def volume_id(self):
        return self.__volume_id

    @volume_id.setter
    def volume_id(self, volume_id):
        self.__volume_id = volume_id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def task_type(self):
        return self.__task_type

    @task_type.setter
    def task_type(self, task_type):
        self.__task_type = task_type
