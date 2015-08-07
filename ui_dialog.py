# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'padrohabitants_dialog.ui'
#
# Created: Fri Aug 07 16:22:56 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_padroHabitantsDialog(object):
    def setupUi(self, padroHabitantsDialog):
        padroHabitantsDialog.setObjectName(_fromUtf8("padroHabitantsDialog"))
        padroHabitantsDialog.resize(475, 161)
        self.btnAccept = QtGui.QPushButton(padroHabitantsDialog)
        self.btnAccept.setGeometry(QtCore.QRect(390, 120, 71, 23))
        self.btnAccept.setObjectName(_fromUtf8("btnAccept"))
        self.btnSelectInput = QtGui.QPushButton(padroHabitantsDialog)
        self.btnSelectInput.setGeometry(QtCore.QRect(390, 25, 71, 23))
        self.btnSelectInput.setObjectName(_fromUtf8("btnSelectInput"))
        self.label = QtGui.QLabel(padroHabitantsDialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(padroHabitantsDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 91, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.btnSelectOutput = QtGui.QPushButton(padroHabitantsDialog)
        self.btnSelectOutput.setGeometry(QtCore.QRect(390, 75, 71, 23))
        self.btnSelectOutput.setObjectName(_fromUtf8("btnSelectOutput"))
        self.txtInputFilePath = QtGui.QTextEdit(padroHabitantsDialog)
        self.txtInputFilePath.setGeometry(QtCore.QRect(100, 20, 271, 36))
        self.txtInputFilePath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtInputFilePath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtInputFilePath.setObjectName(_fromUtf8("txtInputFilePath"))
        self.txtOutputFilePath = QtGui.QTextEdit(padroHabitantsDialog)
        self.txtOutputFilePath.setGeometry(QtCore.QRect(100, 70, 271, 36))
        self.txtOutputFilePath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtOutputFilePath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtOutputFilePath.setObjectName(_fromUtf8("txtOutputFilePath"))

        self.retranslateUi(padroHabitantsDialog)
        QtCore.QMetaObject.connectSlotsByName(padroHabitantsDialog)

    def retranslateUi(self, padroHabitantsDialog):
        padroHabitantsDialog.setWindowTitle(_translate("padroHabitantsDialog", "Dialog", None))
        self.btnAccept.setText(_translate("padroHabitantsDialog", "Aceptar", None))
        self.btnSelectInput.setText(_translate("padroHabitantsDialog", "...", None))
        self.label.setText(_translate("padroHabitantsDialog", "Fitxer entrada:", None))
        self.label_2.setText(_translate("padroHabitantsDialog", "Fitxer sortida:", None))
        self.btnSelectOutput.setText(_translate("padroHabitantsDialog", "...", None))
        self.txtInputFilePath.setHtml(_translate("padroHabitantsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None))
        self.txtOutputFilePath.setHtml(_translate("padroHabitantsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None))

