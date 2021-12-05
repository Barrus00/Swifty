from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import Qt


class TerminalTextHighlighter(QSyntaxHighlighter):
    # This class is used to highlight and format the text in the terminal.

    # These values indicates states, that are used to determine the color of the text.
    DEFAULT_STATE = 0
    ERROR_STATE = 1
    BEGIN_OR_END_STATE = 2

    def __init__(self, parent):
        super(TerminalTextHighlighter, self).__init__(parent)
        self.sectionFormat = QTextCharFormat()
        self.sectionFormat.setForeground(Qt.blue)

        self.errorFormat = QTextCharFormat()
        self.errorFormat.setForeground(Qt.red)
        self.errorFormat.setFontWeight(QFont.Bold)

        self.my_state = self.DEFAULT_STATE

    def set_state(self, state):
        self.my_state = state

    def highlightBlock(self, text):
        if self.my_state == self.ERROR_STATE:
            self.setFormat(0, len(text), self.errorFormat)
        elif self.my_state == self.BEGIN_OR_END_STATE:
            self.setFormat(0, len(text), self.sectionFormat)

