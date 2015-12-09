# -*- coding: utf-8 -*-
from PyQt4 import QtGui, uic
import os
#from qgis.utils import iface


FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'padrohabitants_dialog.ui'))


class PadroHabitantsDialog(QtGui.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(PadroHabitantsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        # set icons and tooltips to the buttons
        #self.center_PButton.setIcon(iface.actionPanToSelected().icon())  