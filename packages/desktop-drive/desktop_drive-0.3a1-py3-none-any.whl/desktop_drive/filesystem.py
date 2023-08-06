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

from abc import ABCMeta, abstractmethod


# The 'metaclass=ABCMeta' thing explicitly makes Filesystem an abstract class:
# Python will forbid direct instantiations of Filesystem (which would be
# impossible to do since some methods defined in this class are abstract methods
# that have no implementation).
#
#     f = Filesystem()  # WRONG! Illegal operation: Filesystem is an
#                       # abstract class.
#
# Instead, you must inherit Filesystem and provide an implementation for the
# abstract methods (like the Local and Drive classes, that both provide
# an implementation for update(), delete(), list(), etc). Then it becomes
# totally legal to instantiate the derived class (like Local or Drive), they are
# not abstract classes.
#
#     f = Local()  # OK
#
class Filesystem(metaclass=ABCMeta):
    """Filesystem is a class abstracting filesystem operations (e.g. removing
    and creating files).
    
    It is an abstract class inherited by local.Local (that implement operations
    on the local filesystem), and by drive.Drive (that implement operations
    on a remote Google Drive filesystem).
    """
    directory_mimetypes = {'inode/directory',
                           'application/vnd.google-apps.folder', ''}
    
    def __init__(self):
        pass

    @abstractmethod
    def update(self, absolute_path, metadata=None, data=None):
        """Update the <metadata> or <contents> of the file located at
        <absolute_path>.
        
        <metadata> must be a dictionary mapping the metadata entries to be
        updated for the file, if any (only the 'mime_type' and  'modified_time'
        keys are currently supported).
        
        <data> must be a io.FileIO object containing the replacement data, if
        any.
        
        If the file located at <absolute_path> does not already exist, it is
        created.
        
        NOTE
        
        If <mime_type> is any of 'application/vnd.google-apps.folder',
        'inode/directory', or '', a directory is always successfully created
        (no matter which MIME type the underlying filesystem actually uses to
        represent directories).
        """
        pass

    @abstractmethod
    def delete(self, absolute_path):
        """Remove the file located at <absolute_path>."""
        pass

    @abstractmethod
    def list(self, absolute_path):
        """List the files in directory located at <absolute_path> on the
        filesystem.
        """
        pass

    @abstractmethod
    def open(self, absolute_path):
        """Return a (metadata, data) tuple.
        
        metadata is a dictionary mapping the metadata entries for the file
        located at <absolute_path> (only the 'mime_type' and 'modified_time'
        keys are currently supported).
        
        data is an io.FileIO object providing a view on the contents of the
        file located at <absolute_path>.
        """
        pass

    def exists(self, absolute_path):
        """Check for the existence of the file located at <absolute_path>.
        Return True if the file exists, False otherwise.
        """
        try:
            self.list(absolute_path)
        except FileNotFoundError:
            return False
        else:
            return True

    @staticmethod
    def checkpathmethod(method):
        """Decorator for performing checks on the existence of a path.
        """
        def checkpathmethod(self, path, *args, **kwargs):
            if not self.exists(path):
                raise FileNotFoundError('File does not exist.')
            return method(self, path, *args, **kwargs)
        return checkpathmethod
