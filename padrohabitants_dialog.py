# -*- coding: utf-8 -*-
from ui_dialog import Ui_padroHabitantsDialog
from PyQt4.QtGui import QDialog


class PadroHabitantsDialog(QDialog):
     
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing:
        # self.<objectname>
        self.ui = Ui_padroHabitantsDialog()
        self.ui.setupUi(self)