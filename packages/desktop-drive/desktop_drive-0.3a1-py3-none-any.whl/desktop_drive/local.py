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

from datetime import datetime
from io import FileIO
from  mimetypes import guess_type
import os
from os import mkdir, scandir, remove, rmdir, stat, utime
from os.path import abspath, basename, exists, isdir, isfile

from desktop_drive.filesystem import Filesystem


class Local(Filesystem):
    """Implementation of FileSystem on the local filesystem. Note that
    the implementation is platform-independent.
    """
    def __init__(self):
        Filesystem.__init__(self)
        self.root = abspath('/')

    def update(self, absolute_path, metadata=None, data=None):
        # If no file exists at <absolute_path>, create it first.
        if not self.exists(absolute_path):
            if metadata.get('mime_type') in Filesystem.directory_mimetypes:
                mkdir(absolute_path)
            else:
                open(absolute_path, mode="x").close()  # Visit the file to create it.
        
        # If <data> is supplied, update file contents.
        if data is not None:
            with open(absolute_path, 'wb') as stream:
                stream.write(data.read())
        
        # If <metadata> is supplied, update file metadata.
        if metadata is not None:
            if 'modified_time' in metadata:
                timestamp = datetime.strptime(metadata['modified_time'],
                                              '%Y-%m-%dT%H:%M:%S.%f').timestamp()
                utime(absolute_path, (timestamp, timestamp))

    @Filesystem.checkpathmethod
    def delete(self, absolute_path):
        if isfile(absolute_path):
            remove(absolute_path)
        elif isdir(absolute_path):
            rmdir(absolute_path)
        else:
            raise TypeError('Cannot delete file.')
    
    # Do not use the @Filesystem.checkpathmethod safeguard: Filesystem.list()
    # has been chosen to test whether a file exists or not (and this test is
    # used to implement @Filesystem.checkpathmethod).
    def list(self, absolute_path):
        if not exists(absolute_path):
            raise FileNotFoundError
        if isdir(absolute_path):
            return sorted([f.name for f in scandir(absolute_path)])
        elif isfile(absolute_path):
            return [basename(absolute_path)]

    @Filesystem.checkpathmethod
    def open(self, absolute_path):
        mimetype, encoding = guess_type(absolute_path)
        mtime = datetime.fromtimestamp(stat(absolute_path).st_mtime).isoformat()
        metadata = {'mime_type': mimetype, 'modified_time': mtime}
        data = FileIO(absolute_path)
        return metadata, data

