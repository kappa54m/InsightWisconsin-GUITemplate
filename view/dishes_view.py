import os
from typing import List, Callable

from PyQt5 import QtWidgets, QtGui, QtCore

import controller
from util import list_to_csv, csv_to_list
from config import lg
from .view_helpers import show_err_dlg, add_scrollarea


class DishesView(QtWidgets.QWidget, controller.DataChangeHandler):
    SUPPORTED_EXTS = ('.BMP', '.GIF', '.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.TIFF', '.XBM')

    def __init__(self, parent, dim):
        super().__init__(parent)
        controller.register_data_change_handler(self)
        self.image_paths = []
        self.__init_ui(dim=dim)

    def __init_ui(self, dim):
        self.setMinimumSize(*dim)

        thumbs_view_dim = dim[0], dim[1]# - self.enlarged_iv.height() - self.src_view.height()
        self.thumbs_view = ThumbnailsView(self, dim=thumbs_view_dim)
        self.thumbs_view.setGeometry(0, 0, *thumbs_view_dim)

        self.thumbs_view.on_thumbnail_selected = self.__on_thumbnail_selected

    #def on_imgs_change(self, old_data_paths, new_data_paths, old_src_paths, new_src_paths):
    #    self.__update_image_paths(update_ui=True)
    def on_project_loaded(self, old_project_data, new_project_data):
        lg.debug("DishesView - project loaded")

    def __on_thumbnail_selected(self, thumb_idx, thumb_img_path):
        lg.debug("DishesView - thumb {} selected {}".format(thumb_idx, thumb_img_path))
        #self.enlarged_iv.show_image(thumb_img_path)

    def __update_image_paths(self, update_ui=False, idx=0):
        ...

    def __update_ui(self, idx=0):
        if len(self.image_paths) > 0:
            #self.enlarged_iv.show_image(self.image_paths[idx])
            self.thumbs_view.set_thumb_images(self.image_paths)
            self.thumbs_view.highlight_thumbnail_at(idx)
        else:
            #self.enlarged_iv.clear_image()
            self.thumbs_view.clear_thumbnail_images()


#class EnlargedImageView(QtWidgets.QLabel, controller.DataChangeHandler):
#    def __init__(self, parent):
#        super().__init__(parent)
#        self.on_urls_drop: Callable[[QtGui.QDropEvent], None] = lambda _: None
#        self.__init_ui()
#
#    def __init_ui(self):
#        self.setAcceptDrops(True)
#        self.setScaledContents(True)
#
#    def dragEnterEvent(self, e):
#        if e.mimeData().hasUrls():
#            e.accept()
#        else:
#            e.ignore()
#
#    def dropEvent(self, e: QtGui.QDropEvent):
#        self.on_urls_drop(e)
#
#    def show_image(self, fp):
#        self.setPixmap(QtGui.QPixmap(fp))
#
#    def clear_image(self):
#        self.setPixmap(QtGui.QPixmap(None))


class ThumbnailsView(QtWidgets.QWidget, controller.DataChangeHandler):
    def __init__(self, parent, dim):
        super().__init__(parent)
        self.thumb_imgs: List[ThumbnailImage] = []
        self.on_thumbnail_selected: Callable[[int, str], None] = lambda _i, _fp: None
        self.__init_ui(dim)

    def __init_ui(self, dim):
        self.setMinimumSize(*dim)

        self.scrollarea = add_scrollarea(self, lambda w: QtWidgets.QHBoxLayout(w))
        self.hbox: QtWidgets.QHBoxLayout = self.scrollarea.widget().layout()
        self.hbox.setSpacing(0)

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        degrees = e.angleDelta().y() if not e.angleDelta().isNull() else 0
        degrees *= -1
        self.scrollarea.horizontalScrollBar().setValue(degrees + self.scrollarea.horizontalScrollBar().value())

        e.accept()

    def add_thumb_img(self, img_fp):
        thumb_img = ThumbnailImage(self)
        thumb_img.set_image(img_fp)

        thumb_img_idx = len(self.thumb_imgs)

        def thumb_img_on_select():
            self.highlight_thumbnail_at(thumb_img_idx)
            self.on_thumbnail_selected(thumb_img_idx, img_fp)

        thumb_img.on_selected = thumb_img_on_select

        self.hbox.addWidget(thumb_img)
        self.thumb_imgs.append(thumb_img)

    def set_thumb_images(self, img_fps):
        self.clear_thumbnail_images()

        for img_fp in img_fps:
            self.add_thumb_img(img_fp)

    def clear_thumbnail_images(self):
        for i in reversed(range(self.hbox.count())):
            self.hbox.itemAt(i).widget().deleteLater()
        self.thumb_imgs.clear()

    def highlight_thumbnail_at(self, idx):
        for i, thumb_img in enumerate(self.thumb_imgs):
            thumb_img.highlight(i == idx)


class ThumbnailImage(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.image_path = ''
        self.on_selected: Callable = lambda: None
        self.__init_ui()

    def __init_ui(self):
        self.setMargin(2)
        self.mousePressEvent = self.__on_mouse_press

    def set_image(self, fp):
        self.image_path = fp
        pixmap = QtGui.QPixmap(fp)
        thumb_h = int(1.5 * self.height())
        thumb_w = thumb_h
        pixmap = pixmap.scaled(thumb_w, thumb_h, QtCore.Qt.KeepAspectRatio)
        self.setPixmap(pixmap)

    def highlight(self, do_highlight=True):
        if do_highlight:
            self.setStyleSheet("border: 1px solid black;")
        else:
            self.setStyleSheet("")

    def __on_mouse_press(self, e: QtGui.QMouseEvent):
        self.on_selected()

