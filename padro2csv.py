#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import csv
from PyQt4.QtGui import QFileDialog, QInputDialog, QMessageBox
from padro_estruc import padro_estruc
from padrohabitants_dialog import PadroHabitantsDialog


def main():
    
    # Ask user to select input file
    global dlg
    dlg = PadroHabitantsDialog()
    dlg.show()
        
    dlg.ui.btnSelectInput.clicked.connect(select_input_file)
    dlg.ui.btnSelectOutput.clicked.connect(select_output_file)
    dlg.ui.btnAccept.clicked.connect(process)


def select_input_file():
    os.chdir(os.getcwd())
    fileIn = QFileDialog.getOpenFileName(None, "Select input file", "", '*.txt')
    dlg.ui.txtInputFilePath.setText(fileIn)
    fileOut = fileIn.replace(".txt", ".csv")
    dlg.ui.txtOutputFilePath.setText(fileOut)
    fileName = os.path.basename(fileOut)
    dlg.ui.txtTableName.setText(fileName[:-4])


def select_output_file():
    os.chdir(os.getcwd())
    fileOut = QFileDialog.getSaveFileName(None, "Select output file", "", '*.csv')
    dlg.ui.txtOutputFilePath.setText(fileOut)
    fileName = os.path.basename(fileOut)
    dlg.ui.txtTableName.setText( fileName[:-4])


def process():

    # Check if input file exists
    fileIn = dlg.ui.txtInputFilePath.toPlainText()
    if not os.path.isfile(fileIn):
        msg = "El fitxer d'entrada indicat no existeix: \n"+fileIn
        QMessageBox.warning(None, "Fitxer no existeix", msg)
        return
    fileOut = dlg.ui.txtOutputFilePath.toPlainText()
    if fileOut == '':
        msg = "Cal especificar un fitxer de sortida"
        QMessageBox.warning(None, "Fitxer de sortida", msg)
        return
    
    padro2csv(fileIn, fileOut)
    
    
def padro2csv(fileIn, fileOut=None):
    
    # Open file for read txt (from padro habitants)
    rf = open(fileIn)
    
    askQuestion = True
    if fileOut == None:
        askQuestion = False
        fileOut = fileIn.replace(".txt", ".csv")
	
	# Openfile to write csv
    with open(fileOut, 'wb') as wf:
        writer = csv.writer(wf)
        writer.writerow(zip(*padro_estruc[1])[3])
        # read lines from txt
        for line in rf.readlines():
            row = []
            # Iterate over all features
            for campos in padro_estruc[1]:
                ini = campos[0]-1 # offset
                fin = ini + campos[1] # longitud
                valor = line[ini:fin].strip() # valor
                row.append(valor)
            # write text into csv file
            writer = csv.writer(wf)
            writer.writerow(row[0:len(padro_estruc[1])])
        # close input file handle
        rf.close()

	# close output file handle
	wf.close()

    # Final message
    if askQuestion:
        msg = u"Exportació completada correctament. Voleu obrir el fitxer generat (s/n)?"
        reply = QMessageBox.question(None, 'Obrir fitxer?', msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.startfile(fileOut)


# Execute script only in QGIS Python console
if __name__ == "__console__":
    main()
