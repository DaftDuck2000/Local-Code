import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QInputDialog, QVBoxLayout, QHBoxLayout, QFileSystemModel, QTreeView, QWidget
from PyQt5.QtGui import QIcon
import PyQt5.QtCore as QtCore
from PyQt5.Qsci import QsciScintilla, QsciLexerPython

welcome = os.path.join("Icons", "Welcome.txt")
global current_file
current_file = "none"

supported_langs = [
    "txt",
    "py",
]



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


        # ------------------------------------ Menu Bar ------------------------------- #


        # Create a menu bar
        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu('File')

        # New File
        new_file_action = QAction('New File', self)
        new_file_action.triggered.connect(self.new_file)
        file_menu.addAction(new_file_action)


        # Open File
        open_action = QAction('Open File', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Open Folder
        open_folder_action = QAction('Open Folder', self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)


        #Save
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)


        # Save As
        save_as_action = QAction('Save As', self)
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)

        # # Create Edit menu
        # edit_menu = menubar.addMenu('Edit')
        # undo_action = QAction('Undo', self)
        # edit_menu.addAction(undo_action)

        # Run Menu
        run_menu = menubar.addMenu("Run")

        # Run Local
        run_local = QAction("Run Locally", self)
        run_local.triggered.connect(self.run)
        run_menu.addAction(run_local)

        # # Run remotely
        # run_server = QAction("Run on Server", self)
        # run_menu.addAction(run_server)


        # View Menu
        view_menu = menubar.addMenu("View")
        
        find_action = QAction("Find", self)
        find_action.triggered.connect(self.find)
        view_menu.addAction(find_action)


        # ------------------------------------ Code Editor window ------------------------ #


        # Calculate the width and height of the code editor
        editor_width = int(screen_geometry.width() * 0.67)  # 2/3 of the screen width
        editor_height = int(screen_geometry.height() * 0.85)

        # Add a layout to contain the directory viewer and the code editor
        layout = QHBoxLayout()

        # Add a directory viewer
        self.directory_viewer = QTreeView(self)
        self.directory_viewer.setRootIsDecorated(False)
        self.directory_viewer.setHeaderHidden(True)
        self.directory_viewer.clicked.connect(self.open_clicked_file)
        layout.addWidget(self.directory_viewer)

        # Add a code editor
        self.editor = QsciScintilla(self)
        self.editor.setMarginWidth(0, 50)  # Set width for line numbers margin
        self.editor.setMarginLineNumbers(0, True)  # Show line numbers
        self.editor.setGeometry(0, 0, editor_width, editor_height)
        layout.addWidget(self.editor, 2)  # Set the stretch factor to 2 to take up 2/3 of the space
        self.editor.setLexer(QsciLexerPython())


        # Set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

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
        
        QsciScintilla QScrollBar:vertical {
            background-color: #333;
            color: #fff;
            width: 15px;
        }
        QsciScintilla QScrollBar:horizontal {
            background-color: #333;
            color: #fff;
            height: 15px;
        }
        QsciScintilla QWidget {
            color: #fff;
            background-color: #333;
            font-family: Courier New;
            font-size: 12pt;
        }
        
        """
        self.setStyleSheet(dark_stylesheet)
        
        editor_textarea_stylesheet = """
        QsciScintilla QWidget {
            background-color: #333;
            color: #fff;
            font-family: Courier New;
            font-size: 12pt;
        }
        """
        self.editor.SendScintilla(self.editor.SCI_STYLESETSIZE, 1, 12)  # Set font size
        self.editor.setStyleSheet(editor_textarea_stylesheet)


        # Align text to the top of the code editor
        self.editor.SendScintilla(self.editor.SCI_SETVSCROLLBAR, 0)

        # Initialize current_file
        self.current_file = ''
        
        with open(welcome, "r") as f:
            self.editor.setText(f.read())

        # Populate directory viewer
        self.populate_directory_viewer()

    def populate_directory_viewer(self):
        model = QFileSystemModel()
        model.setRootPath(QtCore.QDir.rootPath())
        self.directory_viewer.setModel(model)
        self.directory_viewer.setRootIndex(model.index(os.path.abspath('.')))
        
        # Set dark mode stylesheet for the directory viewer
        directory_stylesheet = """
        QTreeView {
            background-color: #333;
            color: #fff;
        }
        QTreeView::item {
            padding: 5px;
        }
        QTreeView::item:selected {
            background-color: #555;
            color: #fff;
        }
        """
        self.directory_viewer.setStyleSheet(directory_stylesheet)
        
    def set_directory_viewer(self, folder_path):
        model = QFileSystemModel()
        model.setRootPath(folder_path)
        self.directory_viewer.setModel(model)
        self.directory_viewer.setRootIndex(model.index(folder_path))
        
        # Set dark mode stylesheet for the directory viewer
        directory_stylesheet = """
        QTreeView {
            background-color: #333;
            color: #fff;
        }
        QTreeView::item {
            padding: 5px;
        }
        QTreeView::item:selected {
            background-color: #555;
            color: #fff;
        }
        """
        self.directory_viewer.setStyleSheet(directory_stylesheet)

    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File')
        try:
            extension = file_path.split(".") # Get the file extension
            
            if extension[1] in supported_langs:    
                with open(file_path, "r") as f:
                    self.editor.setText(f.read())

                global current_file
                current_file = file_path
        except Exception as e:
            print(e)

              
    def open_folder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, 'Open Folder')
        if folder_path:
            self.set_directory_viewer(folder_path)

    def save_as(self):
        global current_file # Declare current_file as global within the method
        if current_file:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, 'Save As', self.current_file)
            if file_path:
                with open(file_path, "w") as f:
                    f.write(self.editor.text())
            
                current_file = file_path

    def save(self):
        global current_file
        if current_file == "none":
            self.save_as()
        elif current_file:	
            with open(current_file, "w") as f:
                f.write(self.editor.text())
    
    def new_file(self):
        global current_file
        if not current_file == "none":
            self.save()
        self.editor.setText("# New File #")
        current_file = "none"
            
            
    def find(self):
        # Create an input dialog to get user input
        find_text, ok = QInputDialog.getText(self, 'Find', 'Enter text to find:')
        if ok:
            # Set the cursor position to the beginning of the document
            self.editor.setCursorPosition(0, 0)

            # Find the text
            found = self.editor.findFirst(find_text, False, False, False, False)
            
            # If text is found
            if isinstance(found, tuple):  # Check if found is a tuple
                # Get the position of the found text
                start_position = found[0]
                end_position = start_position + len(find_text)

                # Select the found text
                self.editor.setSelection(start_position, 0, end_position, 0)

    def open_clicked_file(self, index):
        model = self.directory_viewer.model()
        file_path = model.filePath(index)
        try:
            if os.path.isfile(file_path):
                extension = file_path.split(".") # Get the file extension
                
                if extension[1] in supported_langs:
                    with open(file_path, "r") as f:
                        self.editor.setText(f.read())

                    global current_file
                    current_file = file_path
        except Exception as e:
            print(e)


    def run(self):
        self.save()
        subprocess.run(["python", current_file])
        


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

