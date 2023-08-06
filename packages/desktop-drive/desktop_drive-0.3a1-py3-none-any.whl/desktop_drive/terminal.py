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

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QTextCursor, QFont, QFontMetrics
from PyQt5.QtWidgets import QTextEdit


class Terminal(QTextEdit):
    """A Terminal implementation for printing output and getting user
    input.
    
    Output can be displayed by calling the print() method.
    
    User input can be caught by connecting the Terminal.input_signal
    signal.
    """
    input_signal = pyqtSignal(str)
    default_font = QFont('Courier New')
    default_columns = 80
    default_rows = 25
    
    def __init__(self):
        QTextEdit.__init__(self)
        self.setCurrentFont(Terminal.default_font)
        self.resize(self.default_size)
        self.anchor = 0  # self.anchor saves the character position after which
                         # user text edits are allowed (typically after '$' in
                         # the terminal).
                         # 
                         # Text before this position is read-only text that
                         # comes from previous outputs and user commands.
                         #
                         # Text after this position is editable, and corresponds
                         # to the command field (where the user types the next
                         # command to be executed).
    
    @property
    def default_size(self):
        """The default size of the terminal if it has default_columns,
        default_width, and uses the default_font. This value is used
        to properly size the terminal at initialization.
        """
        font_metrics = QFontMetrics(Terminal.default_font)
        return QSize(font_metrics.width(' ')*Terminal.default_columns,
                     font_metrics.height()*Terminal.default_rows)
    
    def _get_view(self):
        """Return the coordinates of the current view in the terminal
        (in terms of QScrollBar coordinates).
        """
        return QSize(self.horizontalScrollBar().sliderPosition(),
                     self.verticalScrollBar().sliderPosition())
    def _set_view(self, view):
        self.horizontalScrollBar().setSliderPosition(view.width())
        self.verticalScrollBar().setSliderPosition(view.height())
    view = property(_get_view, _set_view)
    
    def keyPressEvent(self, event):
        """Process user input. Emit a Terminal.input_signal signal if
        the user pressed Return, and perform sanity checks for user
        input.
        """
        saved_text = self.toPlainText()
        saved_pos = self.textCursor().position()
        saved_view = self.view
        
        # Modest safety conditional that prevents the user from editing
        # read-only text (located before self.anchor). It does the job most of
        # the time, but does not replace the full fool-proof safety-guard
        # implemented below.
        if not (event.key() == Qt.Key_Backspace and saved_pos == self.anchor):
            QTextEdit.keyPressEvent(self, event)
        
        # If the user pressed Return in the command input field (located after
        # self.anchor), signal it (so the underlying System instance can catch
        # the command call).
        if event.key() == Qt.Key_Return and saved_pos >= self.anchor:
            user_input = saved_text[self.anchor:]  # The user input is the text located after self.anchor.
            self.input_signal.emit(user_input)
            return
        
        if saved_text[:self.anchor] != self.toPlainText()[:self.anchor]:
            # For fool-proof edits: if somehow the user managed to apply edits
            # to read-only text (located before self.anchor), the edits are
            # reverted back.
            self.setPlainText(saved_text)                   # Text is restored.
            
            for c in range(saved_pos):                      # Cursor position is restored. 
                self.moveCursor(QTextCursor.NextCharacter)  #
            
            self.view = saved_view                          # View is restored.
        
    
    def print(self, text):
        """Output <text> in the terminal."""
        self.moveCursor(QTextCursor.End)            # Add output to the end of
        self.setCurrentFont(Terminal.default_font)  # the terminal log, with
        self.insertPlainText(text)                  # the terminal font.
        
        self.anchor = self.textCursor().position()  # Set the anchor to the end
                                                    # of the last output.
        
