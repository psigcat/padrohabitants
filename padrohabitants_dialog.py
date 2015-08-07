# -*- coding: utf-8 -*-
from ui_dialog import Ui_padroHabitantsDialog


class PadroHabitantsDialog(QtGui.QDialog):
     
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing:
        # self.<objectname>
        self.ui = Ui_padroHabitantsDialog()
        self.ui.setupUi(self)