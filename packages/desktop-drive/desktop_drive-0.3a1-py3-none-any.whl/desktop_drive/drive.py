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

from argparse import ArgumentParser
from io import BytesIO
from httplib2 import Http
import os
from os.path import basename, dirname

from apiclient import discovery
from apiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from oauth2client import client, tools
from oauth2client.file import Storage

from desktop_drive.filesystem import Filesystem
from desktop_drive.path import Path


class Drive(Filesystem):
    """Implementation of Filesystem for a Google Drive filesystem."""
    client_secret_file = 'client_id.json'
    app_name = 'Drive API Python Quickstart'
    root = 'root'
    root_name = 'mydrive'
    directory_mimetype = 'application/vnd.google-apps.folder'

    def __init__(self, scope='https://www.googleapis.com/auth/drive',
                 credentials_file_name='local_credentials.json'):
        Filesystem.__init__(self)
        self.root = Drive.root_name
        
        self.store = None
        self.credentials = None
        self.drive = None
        self.scope = scope
        self.credentials_file_name = credentials_file_name
        self.authenticate()
    
    # The three following methods are involved in Drive authentification using
    # the OAuth2 API. Code has been taken from Google Drive API code examples
    # <https://developers.google.com/drive/v3/web/quickstart/python>.
    def get_credentials(self):
        """Try to account for credentials from a previous user
        authentification. If a credentials file does not exist, it
        is created.
        """
        self.store = Storage(self.credentials_file_name)
        self.credentials = self.store.get()
        if not self.credentials or self.credentials.invalid:
            self.create_credentials()

    def create_credentials(self):
        """Create credentials file. The user is asked to give the
        program the permission to manage its Google Drive contents.
        """
        flags = ArgumentParser(parents=[tools.argparser]).parse_args()
        flow = client.flow_from_clientsecrets(Drive.client_secret_file, self.scope)
        flow.user_agent = Drive.app_name
        self.credentials = tools.run_flow(flow, self.store, flags)

    def authenticate(self):
        """Perform the actual authentification."""
        self.get_credentials()
        http = self.credentials.authorize(Http())
        self.drive = discovery.build('drive', 'v3', http=http)

    def _get_id(self, directory, name):
        """Get the ID of a file in <directory> with the given <name>.
        Note that <name> is a regular file name string, while
        <directory> must be a file ID string.
        """
        # Send http request for listing files.
        q = "name='{}' and '{}' in parents and trashed=false".format(name, directory)
        fields = 'files(id)'
        request = self.drive.files().list(q=q, fields=fields)
        response = request.execute()

        # Interpret response.
        files = response.get('files', [])
        if len(files) == 0:
            return None
        elif len(files) == 1:
            return files[0].get('id')
        else:
            # FIXME
            raise ValueError('More than one match in Drive! Not supported yet.')

    def info(self, absolute_path, **options):
        """Fetch info for the file located at <absolute_path>. The
        information format returned depend on the given <options>.
        The format of <options> is the same as Google API's.
        """
        # Get file ID.
        current_id = Drive.root
        for directory in Path.split(absolute_path)[1:]:  # First element is drive's root. Pass.
            current_id = self._get_id(current_id, directory)
        if current_id is None:
            raise FileNotFoundError

        # Get requested metadata for the file ID.
        request = self.drive.files().get(fileId=current_id, **options)
        return request.execute()

    @Filesystem.checkpathmethod
    def delete(self, absolute_path):
        file_info = self.info(absolute_path, fields='id')
        request = self.drive.files().delete(fileId=file_info.get('id'))
        request.execute()

    @Filesystem.checkpathmethod
    def update(self, absolute_path, metadata=None, data=None):
        # Prepare metadata.
        file_metadata = {}
        
        name = basename(absolute_path)
        file_metadata['name'] = name
        
        directory_info = self.info(dirname(absolute_path), fields='id')
        parents = [directory_info.get('id')]
        file_metadata['parents'] = parents
        
        if 'mime_type' in metadata:
            mime_type = metadata.get('mime_type')
            if mime_type in Filesystem.directory_mimetypes:
                mime_type = Drive.directory_mimetype
            file_metadata['mimeType'] = mime_type
        
        if 'modified_time' in metadata:
            modified_time = metadata.get('modified_time')
            modified_time = ''.join([modified_time, 'Z'])
            file_metadata['modifiedTime'] = modified_time
        
        # Create file first if it does not exist.
        if not self.exists(absolute_path):
            request = self.drive.files().create(body=file_metadata)
            request.execute()
        
        # Retrieve file info to fill metadata if incomplete.
        file_info = self.info(absolute_path, fields='id, parents, mimeType')
        
        # Fill MIME type if incomplete.
        if metadata.get('mime_type') is None:
            file_metadata['mimeType'] = file_info.get('mimeType')
        
        # Update data.
        if data is not None:
            media = MediaIoBaseUpload(data, file_metadata.get('mimeType'))
            request = self.drive.files().update(fileId=file_info.get('id'),
                                                media_body=media)
            request.execute()
        
        # Update metadata.
        old_parents = file_info.get('parents')
        new_parents = file_metadata.pop('parents')
        request = self.drive.files().update(fileId=file_info.get('id'),
                                            body=file_metadata,
                                            addParents=new_parents,
                                            removeParents=old_parents)
        request.execute()

    def list(self, absolute_path):
        file_info = self.info(absolute_path, fields='id, name, mimeType')
        if file_info.get('mimeType') != Drive.directory_mimetype:
            return [file_info.get('name')]
        

        # Send http request for listing files.
        q = "'{}' in parents and trashed=false".format(file_info.get('id'))
        fields = 'files(name)'
        request = self.drive.files().list(q=q, fields=fields)
        response = request.execute()
        
        return sorted([f.get('name') for f in response.get('files', [])])
    
    @Filesystem.checkpathmethod
    def open(self, absolute_path):
        file_info = self.info(absolute_path, fields='id, mimeType, modifiedTime')
        
        # Retrieve metadata.
        metadata = {'mime_type': file_info.get('mimetype'),
                    'modified_time': file_info.get('modifiedTime')[:-1]}
        
        # Retrieve file contents by downloading it in a BytesIO instance.
        # NOTE : This block is inspired from the code example in
        # <https://developers.google.com/drive/v3/web/manage-downloads>.
        request = self.drive.files().get_media(fileId=file_info.get('id'))
        stream = BytesIO()
        downloader = MediaIoBaseDownload(stream, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        stream.seek(0)
        
        return metadata, stream


