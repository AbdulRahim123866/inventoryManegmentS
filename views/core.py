from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout

from constant import const
from views.style import GENERAL_QPushButton_STYLESHEET


class MainApp(QWidget):
    def __init__(self,user=None,parent=None):
        super(MainApp,self).__init__()
        self.__init_ui()
        self.user=user
        self._parent=parent


        layout=QGridLayout()

        #back button
        self.back_button=QPushButton("Back")
        self.back_button.clicked.connect(self.return_login)
        self.back_button.setStyleSheet(GENERAL_QPushButton_STYLESHEET)
        layout.addWidget(self.back_button,0,0)


        # horisantal_layout=QVBoxLayout()






        self.setLayout(layout)
    def return_login(self):
        self._parent.show()
        self.hide()


    def __init_ui(self):
        self.setWindowTitle(const.APP_NAME+"main page")
        height = 600
        width = 600
        self.resize(width, height)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

        self.setMinimumWidth(width)
        self.setMaximumWidth(width)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    main = MainApp(user=None, parent=None)
    main.show()

    sys.exit(app.exec())
