# Copyright (C) 2017 Kevin Beaufume, Thomas Saglio
# <thomas.saglio@member.fsf.org>, Louis Senez
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 

import os
from os.path import basename, commonprefix, dirname, join, relpath, normpath, exists, split


class Path:
    """Path is a helper class for manipulating paths. It is primarly
    used by a System instance for managing files.
    """
    def __init__(self, path, system):
        self.path = path
        self.system = system
    
    @property
    def mount_point(self):
        """The mount point of the the filesystem containing the file
        that self.path is referring to.
        """
        current_mount_point = ''
        for mount_point in self.system.mounts:
            common_prefix = commonprefix([mount_point, self.path])
            if (common_prefix == mount_point
                and len(common_prefix) > len(current_mount_point)):
                current_mount_point = mount_point
        return current_mount_point
    
    @property
    def filesystem(self):
        """The Filesystem instance containing the file that self.path is
        referring to.
        """
        return self.system.mounts[self.mount_point]
    
    @property
    def filesystem_root(self):
        """The root string representation of the Filesystem instance
        containing the file that self.path is referring to.
        """
        return self.filesystem.root
    
    @property
    def filesystem_root_relative_path(self):
        """The path relative to the underlying filesystem's root that is
        equivalent to self.path.
        """
        if self.path != self.filesystem_root:
            return relpath(self.path, self.mount_point)
        else:
            return self.filesystem_root
    
    @property
    def filesystem_absolute_path(self):
        """The absolute path on the underlying filesystem that is
        equivalent to self.path.
        """
        return join(self.filesystem_root, self.filesystem_root_relative_path)
    
    @property
    def absolute_path(self):
        """The absolute path on the operating system's root."""
        return join(self.mount_point, self.filesystem_root_relative_path)
    
    @property
    def is_mount_point(self):
        """Whether self.path is a mount point or not (only for Google
        Drive mount points and for the operating system root's mount
        point).
        """
        return self.filesystem_root_relative_path == '.'
    
    @staticmethod
    def split(path):
        """Split a <path> into a list of its file names components."""
        path_list = []
        path = normpath(path)
        while len(path) > 0:
            path_list.append(basename(path))
            path = dirname(path)
        return list(reversed(path_list))

