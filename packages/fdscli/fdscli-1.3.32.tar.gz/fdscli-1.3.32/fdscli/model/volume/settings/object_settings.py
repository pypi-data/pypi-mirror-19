# Copyright (c) 2015, Formation Data Systems, Inc. All Rights Reserved.
#

from model.volume.settings.volume_settings import VolumeSettings

class ObjectSettings(VolumeSettings):
    '''
    Created on May 29, 2015
    
    @author: nate
    '''

    def __init__(self, max_object_size=None, encryption=False, compression=False,
        allow_mount=True, replica=False):

        VolumeSettings.__init__(self, "OBJECT", encryption, compression, allow_mount, replica)
        self.type = "OBJECT"
        self.max_object_size = max_object_size
        self.encryption = encryption
        self.compression = compression

    @property
    def max_object_size(self):
        return self.__max_object_size
    
    @max_object_size.setter
    def max_object_size(self, size):
        
        self.__max_object_size = size
