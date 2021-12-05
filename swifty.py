from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class RefStr:
    """
        A class to hold a string as a reference.
    """
    def __init__(self, s):
        self.str = [s]

    def __set__(self, instance, value):
        self.str[0] = value

    def __bool__(self):
        return bool(self.str[0])

    def __str__(self):
        return self.str[0]


class SwiftyApp:
    INITIAL_WINDOW_X_POS = 50
    INITIAL_WINDOW_Y_POS = 50
    INITIAL_WINDOW_WIDTH = 1024
    INITIAL_WINDOW_HEIGHT = 768

    def __init__(self):
        # Init the main app.
        self.app = QApplication([])

        # Init and adjust the main window properties.
        self.window = QWidget()
        self.window.setWindowTitle("Swifty - Swift Code Editor")
        self.window.setGeometry(self.INITIAL_WINDOW_X_POS,
                                self.INITIAL_WINDOW_Y_POS,
                                self.INITIAL_WINDOW_WIDTH,
                                self.INITIAL_WINDOW_HEIGHT)

        # Set up the code editor, file manager and the terminal.
        self.textEditor = TextEditor()
        self.fileManager = FileManager(self.window, self.textEditor.widget)
        self.terminalManager = TerminalManager(self.fileManager.file_path)

        self.layout = QVBoxLayout()

        # Adjust the layout of the widgets.
        self.layout.addWidget(self.fileManager.widget)
        self.layout.addWidget(self.textEditor.widget)
        self.layout.addWidget(self.terminalManager.widget)

        self.window.setLayout(self.layout)

        # Display window, and run the application.
        self.window.show()
        self.app.exec_()


class TextEditor:
    """
        The main code editor.
    """
    def __init__(self):
        self.widget = QPlainTextEdit()
        self.widget.setWindowTitle("Text editor")


class FileManager:
    """
        The file manager is a widget that allows the user to open and save files.
    """

    file_path = RefStr("")

    def __init__(self, parent, editor):
        self.widget = QWidget()
        self.layout = QHBoxLayout()

        # Create the navigation buttons.
        self.open_button = QPushButton("Open file")
        self.open_button.clicked.connect(self.open_file)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)

        self.save_as_button = QPushButton("Save as")
        self.save_as_button.clicked.connect(self.save_as)

        # Adjust the layout.
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.save_as_button)

        self.widget.setLayout(self.layout)

        self.parent = parent
        self.editor = editor

    def open_file(self):
        path = QFileDialog.getOpenFileName(self.parent, 'Open')[0]
        if path:
            # If a file was selected, open it and insert content into the editor.
            self.editor.setPlainText(open(path).read())
            self.file_path = path
            alert = QMessageBox()
            alert.setText(path)
            alert.exec()

    def save_as(self):
        path = QFileDialog.getSaveFileName(self.parent, 'Save')[0]
        if path:
            self.file_path = path
            self.save()

    def save(self):
        if self.file_path is None:
            # If no file is selected, ask user to create/select a new one, to save the content into.
            self.save_as()
        else:
            # If a file is selected, save the content into it.
            with open(str(self.file_path), 'w') as f:
                f.write(self.editor.toPlainText())
            self.editor.document().setModified(False)


class TerminalManager:
    """
        The terminal manager is a widget that allows the user to execute the code, and display live output.
    """

    def __init__(self, file_path):
        self.widget = QWidget()

        self.terminal_window = QPlainTextEdit()
        self.terminal_window.setWindowTitle("Terminal output")
        self.terminal_window.setReadOnly(True)
        self.exit_code_widget = QLabel("Exit code: ")

        self.run_script_tool = self.RunScriptTool(self.terminal_window, self.exit_code_widget, file_path)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.run_script_tool.widget)
        self.layout.addWidget(self.terminal_window)
        self.layout.addWidget(self.exit_code_widget)

        self.widget.setLayout(self.layout)

    class RunScriptTool:
        def __init__(self, terminal_editor, exit_code_widget, file_path):
            self.file_path = file_path
            self.output = terminal_editor

            # Create a button that will run the script.
            self.widget = QPushButton("Run script")
            self.widget.clicked.connect(self.run_script)

            # Prepare an extra core responsible for the terminal output reading.
            self.process = QtCore.QProcess()
            self.process.stateChanged.connect(self.handle_state_change)
            self.process.readyReadStandardOutput.connect(self.read_output)
            self.process.readyReadStandardError.connect(self.read_error)
            self.process.started.connect(self.started)
            self.process.finished.connect(self.finished)

            # Save the exit code widget.
            self.exit_code_widget = exit_code_widget

        def get_exit_code(self):
            return self.process.exitCode()

        def run_script(self):
            if not self.file_path:
                alert = QMessageBox()
                alert.setText("Not a valid file.")
                alert.exec()
            else:
                self.call_program()

        def call_program(self):
            self.process.start('/usr/bin/env swift ' + str(self.file_path))

        def read_output(self):
            cursor = self.output.textCursor()
            cursor.movePosition(cursor.End)
            cursor.insertText(self.process.readAllStandardOutput().data().decode('utf-8'))
            self.output.ensureCursorVisible()

        def read_error(self):
            cursor = self.output.textCursor()
            cursor.movePosition(cursor.End)

            # TODO - this is not working. This sets text color to red, but doesnt restore the default color.
            #color = QTextCharFormat()
            # # Set QTextFormat to red color.
            # color.setForeground(Qt.red)
            # cursor.setCharFormat(color)
            cursor.insertText(self.process.readAllStandardError().data().decode('utf-8'))
            self.output.ensureCursorVisible()

            # Restore default black color.
            # color.setForeground(Qt.black)
            # cursor.setCharFormat(color)
            # self.output.ensureCursorVisible()

        def handle_state_change(self):
            states = {
                QtCore.QProcess.NotRunning: 'NotRunning',
                QtCore.QProcess.Starting: 'Starting',
                QtCore.QProcess.Running: 'Running'
            }

            self.widget.message = states[self.process.state()]
            print(states[self.process.state()])

        def started(self):
            self.widget.setEnabled(False)

        def finished(self):
            self.exit_code_widget.setText("Exit code: " + str(self.get_exit_code()))
            self.widget.setEnabled(True)

if __name__ == "__main__":
    SwiftyApp()
