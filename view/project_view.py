from typing import List
import os

from PyQt5 import QtWidgets, QtCore

from config import lg
import controller
from .view_helpers import show_err_dlg, add_scrollarea, load_uic


class ProjectView(QtWidgets.QGroupBox, controller.DataChangeHandler):
    def __init__(self, parent, dim):
        super().__init__(parent)
        controller.register_data_change_handler(self)
        self.__init_ui(dim=dim)

    def __init_ui(self, dim):
        load_uic(self, "project_view.ui")

        self.btn_clear.clicked.connect(self.__on_clear)
        self.btn_load.clicked.connect(self.__on_load)
        self.btn_save.clicked.connect(self.__on_save)

    def on_project_loaded(self, old_project_data, new_project_data):
        # Update spinboxes here
        # if new_project_data is None, set "default" values

        lg.debug("ProjectView - on_project_loaded")
        pass

    def __on_clear(self):
        lg.debug("clear button clicked")

    def __on_load(self):
        lg.debug("load button clicked")
        # TODO pick file from file picker
        fp = ""

        # Originator not passed as argument, so change handler will be invoked on this UI element
        controller.load_project(fp)

    def __on_save(self):
        lg.debug("save button clicked")

