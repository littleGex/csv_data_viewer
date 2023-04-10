import os
import sys
import logging
import pwd
import pandas as pd
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QAction, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings
from pathlib import Path
from definitions import ROOT_PATH, START, VERSION


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class Datatable(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(Datatable, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(),
                                    index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class Showcsv(QMainWindow):
    def __init__(self, parent=None):
        super(Showcsv, self).__init__(parent)
        logging.info(START)
        logging.info(f"CSV data viewer version - {VERSION}")
        # Check if correct argument number provided
        if len(sys.argv) == 1:
            self.dataIn = None
        elif len(sys.argv) == 2:
            self.dataIn = self.is_csv_file(Path(sys.argv[1]))
        else:
            logging.error("Incorrect arguments provided - "
                          "closing ui")
            sys.exit()

        # Load dialog ui
        uic.loadUi(os.path.join(ROOT_PATH, 'ui/main.ui'), self)

        self.model = None

        self.settings = QSettings('r2d2DV', 'r2d2DV')
        logging.info(f"Session file: "
                     f"{QSettings.fileName(self.settings)}")
        # Re-establish personal settings
        self.restore_session()
        # Set button functions
        self.set_buttons()
        # Load menu
        self.set_menu()
        # Run GUI
        if self.dataIn:
            self.run()
        else:
            self.browse_gen()

    def restore_session(self):
        """
        This function attempts to reload user personal
        preferences.
        """
        if self.settings.contains("theme_selection"):
            with open(self.settings.value
                          ('theme_selection')) as file:
                style = file.read()
            self.setStyleSheet(style)
            logging.info(f"Restoring "
                         f"{self.settings.value('theme_selection')} "
                         f"display settings")

    def set_menu(self):
        # set up windows menubar
        main_menu = self.menuBar()
        main_menu.setNativeMenuBar(False)  # needed for mac

        file_menu = main_menu.addMenu("File")
        settings = file_menu.addMenu("Settings")
        data_menu = main_menu.addMenu("Data")

        themes = settings.addMenu('Themes')

        quit_app = QAction("Quit", self)
        quit_app.setShortcut("Ctrl+Q")
        quit_app.setStatusTip("Click to Exit")
        file_menu.addAction(quit_app)
        quit_app.triggered.connect(self.app_close)

        dark_grey = QAction("Dark Grey", self)
        themes.addAction(dark_grey)
        dark_grey.triggered.connect(self.grey_sheet)

        dark_orange = QAction("Dark Orange", self)
        themes.addAction(dark_orange)
        dark_orange.triggered.connect(self.orange_sheet)

        default = QAction("Default", self)
        themes.addAction(default)
        default.triggered.connect(self.default_sheet)

        load_data = QAction("load csv", self)
        load_data.setStatusTip("Load another data source")
        data_menu.addAction(load_data)
        load_data.triggered.connect(self.browse_gen)

    def set_buttons(self):
        # Add function to exit button
        self.exit_button.released.connect(self.app_close)
    
    def run(self):
        """
        This function attempts to load the data and present
        in ui.
        """
        # Load csv as dataframe
        df = self.get_df(self.dataIn)
        print(df)
        # Set data model
        self.model = Datatable(df)
        # Load data to tableview widget
        self.tableView.setModel(self.model)
        # Set column widths to match data
        self.tableView.resizeColumnsToContents()
        # Show csv filename for reference
        self.file_line.setText(str(self.dataIn))

    def app_close(self):
        """
        This function is used to close the GUI.
        """
        logging.info("Closing CSV data viewer session")
        self.close()

    def browse_gen(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.\
            getOpenFileName(self,
                            "Pick R2D2 data source",
                            "",
                            "CSV Files (*.csv)",
                            options=options)
        self.dataIn = self.is_csv_file(Path(file_name))
        self.run()

    def default_sheet(self):
        css_file = os.path.join(ROOT_PATH, 'src/themes/default.css')
        with open(css_file) as file:
            style = file.read()
        self.setStyleSheet(style)
        self.settings.setValue('theme_selection',
                               css_file)

    def grey_sheet(self):
        css_file = os.path.join(ROOT_PATH, 'src/themes/darkGrey.css')
        with open(css_file) as file:
            style = file.read()
        self.setStyleSheet(style)
        self.settings.setValue('theme_selection',
                               css_file)

    def orange_sheet(self):
        css_file = os.path.join(ROOT_PATH, 'src/themes/darkOrange.css')
        with open(css_file) as file:
            style = file.read()
        self.setStyleSheet(style)
        self.settings.setValue('theme_selection',
                               css_file)

    @staticmethod
    def is_csv_file(filepath: Path):
        """
        This function checks whether the filename provided is a
        valid file and whether it is of the required csv format.

        :param filepath: R2D2 get output csv path
        :return: Valid file path
        """
        if filepath.is_file():
            if filepath.suffix == '.csv':
                logging.info(f"Loading CSV file {filepath}")
                return filepath
            else:
                logging.error("File not required .csv format")
                sys.exit()
        else:
            logging.error("No valid file provided")
            sys.exit()

    @staticmethod
    def get_df(csv):
        """
        This function attempts to load the csv into a dataframe.

        :param csv: Source csv file
        :return: Dataframe of source csv file
        """
        return pd.read_csv(csv, sep=";")


# ======================================================================
if __name__ == "__main__":
    print(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('../ui/images/r2.png'))
    window = Showcsv()
    window.show()
    sys.exit(app.exec_())
