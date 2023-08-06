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
import os
from os import curdir
from os.path import abspath, isabs, join, normpath
from shlex import split
from textwrap import dedent

from PyQt5.QtCore import QObject, pyqtSignal

from desktop_drive.path import Path
from desktop_drive.terminal import Terminal
from desktop_drive.local import Local
from desktop_drive.drive import Drive


class System(QObject):
    """A System object is in charge of a terminal and of one or several
    filesystems. It interprets files-related commands entered by the
    user in the terminal, and performs the corresponding operations. The
    supported commands are a subset of the bash commands:
    
        pwd, cd, ls, mkdir, rm, touch, cp, mv, exit
        
    It also implements an extra command:
    
        mount-drive
    
    It can operate on files located either on the local filesystem, or
    on a remote Google Drive filesystem. Drive files can be accessed
    after they have been mounted with the mount-drive command.
    
    A system is associated to a dedicated Terminal instance. When the
    user provides input in the terminal, it emits a
    Terminal.input_signal signal. It is connected to System.execute()
    for interpretation and execution of user input.
    
    When the system is exited by the user (with the exit command),
    it emits a System.exit_signal signal to ask for end of program
    execution.
    """
    
    root = abspath('/')
    
    default_prompt_string = '$ '
    default_welcome_string = 'Welcome to Desktop-Drive 0.3!\n'
    default_help_string = dedent("""\
        List of available commands:
            pwd             ls [path]       mount-drive <path>      exit
            cd <path>       rm <path>       hello <name>
            
            mkdir <path>    cp <source_path> <target_path>
            touch <path>    mv <source_path> <target_path>
        Type 'help' to print this help.
        """)
    default_command_prefix = 'command_'  # Prefix used in methods names to
                                         # distinguish commands from regular
                                         # methods.
    exit_signal = pyqtSignal()
    
    def __init__(self, terminal):
        QObject.__init__(self)
        self.cwd = abspath(curdir)
        self.mounts = {System.root: Local()}
        
        self.terminal = terminal
        self.welcome_string = System.default_welcome_string
        self.help_string = System.default_help_string
        self.prompt_string = System.default_prompt_string
        self.command_prefix = System.default_command_prefix
        self.terminal.input_signal.connect(self.execute)
        
        self.welcome()
    
    def welcome(self):
        """Print a welcome message on the terminal, and prompt for the
        first command.
        """
        self.terminal.print(self.welcome_string)
        self.command_help()
        self.prompt()
    
    def prompt(self):
        """Print the prompt on the terminal."""
        self.terminal.print(self.cwd)
        self.terminal.print(self.prompt_string)
    
    def handle_error(self, error):
        """Handle a generic <error> that occured during command
        execution by printing the appropriate error message.
        """
        self.terminal.print('Oops! Some error occured!\n')
        self.terminal.print('{}\n'.format(error))
    
    def handle_undefined_command(self, command_name):
        """Print a 'does not exists' message. This is called when the
        user asks for an undefined <command_name>."""
        self.terminal.print('Command "{}" does not exist!\n'.format(command_name))
    
    def execute(self, user_input):
        """Interpret the given <user_input> and execute the command."""
        # Analyze input to get the different command elements.
        user_input = user_input.strip()
        if user_input == '':  # Empty command.
            self.prompt()
            return
        command_elements = split(user_input)
        
        # Interpret. The first element of <command_elements> is the
        # command name, while the other elements are the arguments and
        # options passed to the command.
        command_name = command_elements[0]
        arguments = command_elements[1:]
        
        method_name = ''.join([self.command_prefix, command_name.replace('-', '_')])
        method = getattr(self, method_name, None)  # (Try to) get the method corresponding to the given <command_name>...
        if method is None or not callable(method):
            # ... If the command does not exist, print an error message and
            # continue the mainloop for executing further commands...
            self.handle_undefined_command(command_name)
            self.prompt()
            return
        
        # ... Otherwise, try to execute the command.
        try:
            method(*arguments)        # Execute...
        except Exception as error:
            self.handle_error(error)  # ... If an error occurs during execution, handle it.
        finally:
            self.prompt()
    
    # Note: any method name that starts with 'command_' is considered by
    # execute() to be a legal system command accessible from the terminal.
    def command_hello(self, name):
        """Great the given <name> by printing a message on the terminal.
        This is mainly for demonstration purposes."""
        self.terminal.print('Hello, {}!\n'.format(name))
    
    def command_help(self):
        """Print a help message on the terminal."""
        self.terminal.print(self.help_string)
    
    def command_exit(self):
        """Ask for end of program execution by emitting a
        System.exit_signal signal.
        """
        self.exit_signal.emit()
    
    def canonicalize(self, path):
        """Convert an absolute or relative <path> to a much more handy
        format. Ir returns a Path instance.
        """
        # Preformat <path> (make absolute, then normalize)...
        if not isabs(path):
            path = join(self.cwd, path)
        path = normpath(path)
        
        # ... And return a Path instance for easy handling.
        return Path(path, self)
    
    def command_mount_drive(self, path):
        """Mount a drive on the directory located at <path>. Note that
        the drive is not really mounted on the underlying filesystem,
        and that only the current System instance is aware of such a
        mount point.
        """
        path = self.canonicalize(path)

        if not path.filesystem.exists(path.absolute_path):
            self.terminal.print('Path does not exist\n')
            return
        self.mounts[path.absolute_path] = Drive()
    
    def command_pwd(self):
        """Print the current working directory."""
        self.terminal.print('{}\n'.format(self.cwd))
        
        path = self.canonicalize(self.cwd)
        self.terminal.print('[DEBUG] self.cwd:                      {}\n'.format(path.path))
        self.terminal.print('[DEBUG] mount_point:                   {}\n'.format(path.mount_point))
        self.terminal.print('[DEBUG] filesystem:                    {}\n'.format(path.filesystem))
        self.terminal.print('[DEBUG] filesystem_root:               {}\n'.format(path.filesystem_root))
        self.terminal.print('[DEBUG] filesystem_root_relative_path: {}\n'.format(path.filesystem_root_relative_path))
        self.terminal.print('[DEBUG] filesystem_absolute_path:      {}\n'.format(path.filesystem_absolute_path))
        self.terminal.print('[DEBUG] absolute_path:                 {}\n'.format(path.absolute_path))
        self.terminal.print('[DEBUG] is_mount_point:                {}\n'.format(path.is_mount_point))
        self.terminal.print('[DEBUG] self.mounts:                   {}\n'.format(', '.join(self.mounts)))

    def command_cd(self, path):
        """Change current working directory."""
        path = self.canonicalize(path)
        if not path.filesystem.exists(path.filesystem_absolute_path):
            raise FileNotFoundError('File does not exist.')
        self.cwd = path.absolute_path
    
    def command_ls(self, path=curdir):
        """List files in a directory."""
        path = self.canonicalize(path)
        for filename in path.filesystem.list(path.filesystem_absolute_path):
            self.terminal.print('{}\n'.format(filename))

    def command_mkdir(self, path):
        """Create a new directory."""
        path = self.canonicalize(path)
        
        if path.filesystem.exists(path.filesystem_absolute_path):
            self.terminal.print('File already exists.\n')
            return
        
        path.filesystem.update(path.filesystem_absolute_path,
                               metadata={'mime_type': 'inode/directory'})

    def command_rm(self, path):
        """Remove a file."""
        path = self.canonicalize(path)
        if path.is_mount_point:
            self.terminal.print('File is mounted, cannot remove.\n')
            return
        path.filesystem.delete(path.filesystem_absolute_path)

    def command_touch(self, path):
        """Update a file's timestamp, or create a new file if it doesn't
        already exist.
        """
        path = self.canonicalize(path)
        if path.filesystem.exists(path.filesystem_absolute_path):
            path.filesystem.update(path.filesystem_absolute_path,
                                   metadata={'modified_time': System.timestamp()})
        else:
            path.filesystem.update(path.filesystem_absolute_path,
                                   metadata={'mime_type': 'text/plain'})

    def command_cp(self, source_path, target_path):
        """Copy file."""
        source_path = self.canonicalize(source_path)
        target_path = self.canonicalize(target_path)
        if target_path.is_mount_point:
            self.terminal.print('File is mounted, cannot replace by copy.\n')
            return
        
        metadata, data = source_path.filesystem.open(source_path.filesystem_absolute_path)
        target_path.filesystem.update(target_path.filesystem_absolute_path,
                                      metadata=metadata, data=data)

    def command_mv(self, source_path, target_path):
        """Move (or rename) file to another location."""
        # It might seems a bold implementation of mv (a deep copy of the file
        # is performed each time), but it is the safest when working with files
        # that can be either on the local or on a remote filesystem.
        source_path = self.canonicalize(source_path)
        if source_path.is_mount_point:
            self.terminal.print('File is mounted, cannot move.\n')
            return
        self.command_cp(source_path, target_path)
        self.command_rm(source_path)
    
    @staticmethod
    def timestamp():
        """Return current time under ISO format. Used for stamping files
        with last modified time.
        """
        return datetime.now().isoformat()

