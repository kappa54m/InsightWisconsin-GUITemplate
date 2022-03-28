import sys
import os
import traceback
import logging

from PyQt5 import QtWidgets

from view.main_window import MainWindow
import model
import controller
import config
import util


def main():
    app = QtWidgets.QApplication(sys.argv)

    ## Load configuration
    #config_path = 'config.yaml'
    #try:
    #    config.load(config_path)
    #except Exception as e:
    #    traceback.print_exc()
    #    e_dlg = QtWidgets.QMessageBox()
    #    e_dlg.setIcon(QtWidgets.QMessageBox.Critical)
    #    e_dlg.setWindowTitle("Error")
    #    e_dlg.setText("Configuration Error")
    #    e_dlg.setDetailedText("Error occurred while loading config path from '{}': {}".format(config_path, e))
    #    e_dlg.show()
    #    sys.exit(app.exec_())
    #print("Config: {}".format(config.config))
    config.uis_path = os.path.join(os.path.dirname(__file__), 'ui')

    # Initialize Model/Controller
    controller.init_model()

    win = MainWindow()

    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
