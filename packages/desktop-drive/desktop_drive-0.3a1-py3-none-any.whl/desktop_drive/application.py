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

from PyQt5.QtWidgets import QApplication

from desktop_drive.terminal import Terminal
from desktop_drive.system import System


class Application(QApplication):
    """Application instance manages the GUI of a System and Terminal
    instances.
    
    The application stops when it catches a System.exit_signal signal.
    """
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.terminal = Terminal()
        self.system = System(self.terminal)
        self.system.exit_signal.connect(self.quit)
        self.terminal.show()

