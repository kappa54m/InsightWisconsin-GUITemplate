import config

from PyQt5 import QtWidgets, Qt, QtGui

from typing import Callable
import os


def get_ui_path(path):
    return os.path.join(config.uis_path, path)


def get_icon(name):
    split = os.path.splitext(name)
    if not split[1]:
        name = split[0] + ".png"
    return QtGui.QIcon(os.path.join("ui/icons", name))


def show_err_dlg(info_text, text='Error', title='Error', detailed_text=None, icon=QtWidgets.QMessageBox.Critical,
                 window_icon=None, window_icon_name=None):
    dlg = QtWidgets.QMessageBox()
    dlg.setWindowTitle(title)
    dlg.setIcon(icon)
    window_icon = window_icon or dlg.style().standardIcon(window_icon_name or Qt.QStyle.SP_MessageBoxCritical)
    dlg.setWindowIcon(window_icon)
    dlg.setText(text)
    dlg.setInformativeText(info_text)
    if detailed_text:
        dlg.setDetailedText(detailed_text)

    return dlg.exec_()


def add_scrollarea(outer_widget: QtWidgets.QWidget,
                   inner_layout_factory: Callable[[QtWidgets.QWidget], QtWidgets.QLayout]) -> QtWidgets.QScrollArea:
    scrollarea = QtWidgets.QScrollArea()
    scrollarea.setWidgetResizable(True)

    outer_layout = QtWidgets.QVBoxLayout(outer_widget)
    outer_layout.addWidget(scrollarea)

    inner_widget = QtWidgets.QWidget()
    _inner_layout = inner_layout_factory(inner_widget)
    scrollarea.setWidget(inner_widget)

    return scrollarea


def load_uic(to_, rel_path):
    from PyQt5 import uic
    return uic.loadUi(get_ui_path(rel_path), to_)
