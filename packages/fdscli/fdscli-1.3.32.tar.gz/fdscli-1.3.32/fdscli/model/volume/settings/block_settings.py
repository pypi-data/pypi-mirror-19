# Copyright (c) 2015, Formation Data Systems, Inc. All Rights Reserved.
#

from model.volume.settings.volume_settings import VolumeSettings
from model.common.size import Size

class BlockSettings(VolumeSettings):
    '''
    Created on May 29, 2015
    
    @author: nate
    '''

    def __init__(self, capacity=Size(10, "GB"), block_size=None, encryption=False, compression=False, allow_mount=True, replica=False):
        VolumeSettings.__init__(self, "BLOCK", encryption, compression, allow_mount, replica)
        self.type = "BLOCK"
        self.capacity = capacity
        self.block_size = block_size
        self.encryption = encryption
        self.compression = compression

    @property
    def capacity(self):
        return self.__capacity
    
    @capacity.setter
    def capacity(self, size):
        
        self.__capacity = size
        
    @property
    def block_size(self):
        return self.__block_size
    
    @block_size.setter
    def block_size(self, size):
        
        self.__block_size = size

