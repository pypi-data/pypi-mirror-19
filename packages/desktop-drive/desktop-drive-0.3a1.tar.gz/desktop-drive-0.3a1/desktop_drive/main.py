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

from sys import argv, exit

from desktop_drive.application import Application

def main():
    exit(Application(argv).exec_())
    # Application inherits QApplication.
    #
    # A QApplication instance must always be created when working with
    # PyQt5. argv represents the arguments that were passed to the
    # application by the command line.
    #
    # Application(argv).exec_() creates a QApplication instance and
    # launches the execution by entering the mainloop (were keyboard
    # and mouse signals are caught and forwarded to widgets for
    # handling).
    #
    # When the mainloop is over (e.g. after destroying the root
    # widget), Application(argv).exec_() returns a status code (0 if
    # there was no error, any other value if something went
    # wrong).
    #
    # exit(Application(argv).exec_()) forwards this status code to the
    # operating system (to let it know whether the execution went well
    # or not).

if __name__ == '__main__':
    main()

