from PyQt6.QtWidgets import QLabel


class ClickableLabel(QLabel):
    def __init__(self,when_clicked,msg,parent=None):
        super().__init__(msg,parent=parent)
        self._msg=msg
        self._when_clicked=when_clicked
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._when_clicked(event)
