import sys
import os
import subprocess
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog
from PyQt5.QtGui import QIcon
import PyQt5.QtCore as QtCore
from PyQt5.Qsci import QsciScintilla, QsciLexerPython

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Local Code')

        # Set the size and title of the window
        self.setGeometry(50, 50, 1600, 900)  # (x, y, width, height)

        # Set the icon for the window
        path = os.path.join("Icons", "Icon.png")
        self.setWindowIcon(QIcon(path))

        # Get the geometry of the screen
        screen_geometry = QApplication.desktop().screenGeometry()

        # Create a menu bar
        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu('File')

        # New File
        new_file_action = QAction('New File', self)
        file_menu.addAction(new_file_action)

        # New Folder
        new_folder_action = QAction("New Folder", self)
        file_menu.addAction(new_folder_action)

        # Open File
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Save As
        save_as_action = QAction('Save As', self)
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)

        # Create Edit menu
        edit_menu = menubar.addMenu('Edit')
        undo_action = QAction('Undo', self)
        edit_menu.addAction(undo_action)

        # Run Menu
        run_menu = menubar.addMenu("Run")

        # Run Local
        run_local = QAction("Run Locally", self)
        run_local.triggered.connect(local.run)
        run_menu.addAction(run_local)

        # Run remotely
        run_server = QAction("Run on Server", self)
        run_menu.addAction(run_server)

        # Calculate the width and height of the code editor
        editor_width = int(screen_geometry.width() * 0.85)
        editor_height = int(screen_geometry.height() * 0.85)

        # Add a code editor
        self.editor = QsciScintilla(self)
        self.editor.setGeometry(200, 50, editor_width, editor_height)
        self.editor.setLexer(QsciLexerPython())  # Set lexer for Python syntax highlighting

        # Set dark mode style sheet
        dark_stylesheet = """
        QMainWindow {
            background-color: #333;
            color: #fff;
        }
        QMenuBar {
            background-color: #333;
            color: #fff;
        }
        QMenuBar::item {
            background-color: #333;
            color: #fff;
        }
        QMenuBar::item:selected {
            background-color: #555;
            color: #fff;
        }
        QMenu {
            background-color: #333;
            color: #fff;
        }
        QMenu::item {
            background-color: #333;
            color: #fff;
        }
        QMenu::item:selected {
            background-color: #555;
            color: #fff;
        }
        """
        self.setStyleSheet(dark_stylesheet)

        # Align text to the top of the code editor
        self.editor.SendScintilla(self.editor.SCI_SETVSCROLLBAR, 0)

        # Initialize current_file
        self.current_file = ''

    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File')
        if file_path:
            with open(file_path, "r") as f:
                self.editor.setText(f.read())
                
            global current_file
            current_file = file_path

    def save_as(self):
        global current_file  # Declare current_file as global within the method
        if current_file:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, 'Save As', self.current_file)
            if file_path:
                with open(file_path, "w") as f:
                    f.write(self.editor.text())
                
                current_file = file_path


class local:
    def run():
        subprocess.run(["python", current_file])


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
