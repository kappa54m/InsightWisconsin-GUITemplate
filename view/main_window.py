from PyQt5 import QtCore, QtWidgets

from .dishes_view import DishesView
from .project_view import ProjectView
#from .motor_ctl_view import MotorlControlView
from .view_helpers import get_icon


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.dishes_view = None
        self.project_view = None
        self.motor_ctl_view = None
        self.__init_ui()

    def __init_ui(self):
        menu_bar_h = 0  # 25
        dim = (600, 600)

        dishes_view_h = 125
        self.dishes_view = DishesView(self, dim=(dim[0], dishes_view_h))
        
        project_view_h = 450
        self.project_view = ProjectView(self, dim=(dim[0], project_view_h))
        self.project_view.setGeometry(0, dishes_view_h, dim[0], project_view_h)

        #self.motor_ctl_view = MotorControlView(self)

        self.__create_menu_bar()

        self.setGeometry(200, 200, *dim)
        self.setWindowTitle("Universal UI")
        #self.setWindowIcon(get_icon('my_icon'))
        self.setWindowModality(QtCore.Qt.WindowModal)

    def __create_menu_bar(self):
        #w_menu = self.menuBar().addMenu('&Windows')

        #w_i1 = QtWidgets.QAction('&Item1', self)
        #w_i1.setShortcut('Ctrl+Shift+C')
        #w_i1.triggered.connect(self.__cb1)

        #w_i2 = QtWidgets.QAction('&Item2', self)
        #w_i2.setShortcut('Ctrl+Alt+C')
        #w_i2.triggered.connect(self.__cb2)

        #w_menu.addActions([w_i1, w_i2])
        pass

    def __cb1(self):
        ...

    def __cb2(self):
        ...

