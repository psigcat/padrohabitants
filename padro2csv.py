#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import csv
from PyQt4.QtGui import QFileDialog, QInputDialog, QMessageBox
from PyQt4.QtCore import QSettings
import psycopg2
import psycopg2.extensions
from padro_estruc import padro_estruc
from padrohabitants_dialog import PadroHabitantsDialog


def main():
    
    # Ask user to select input file
    global dlg
    dlg = PadroHabitantsDialog()
    dlg.show()
    fill_combo()
        
    dlg.ui.btnSelectInput.clicked.connect(select_input_file)
    dlg.ui.btnSelectOutput.clicked.connect(select_output_file)
    dlg.ui.btnAccept.clicked.connect(process)
    dlg.ui.cboConnection.currentIndexChanged.connect(connection_changed)


def get_connections():
    # get the list of current connections
    conn_list = []
    settings = QSettings()
    root = '/PostgreSQL/connections'
    settings.beginGroup(root)
    for name in settings.childGroups():
        conn_list.append(name)
        settings.endGroup()
    return conn_list
    
    
def fill_combo():
    conn_list = get_connections()
    dlg.ui.cboConnection.addItems(conn_list)
    
    
def open_connection(name):
    # look for connection data in QGIS configration
    # get connection data
    qgisSettings = QSettings()
    
    root = "/PostgreSQL/connections/"+name+"/"
    DATABASE_HOST = qgisSettings.value(root+"host", '')
    DATABASE_NAME = qgisSettings.value(root+"database", '')
    DATABASE_PORT = qgisSettings.value(root+"port", '')
    DATABASE_USER = qgisSettings.value(root+"username", '')
    DATABASE_PWD = qgisSettings.value(root+"password", '')
    SSL_MODE = qgisSettings.value(root+"sslmode", QgsDataSourceURI.SSLdisable)
    
    # get realm of the connection (realm don't have use ry pwd)
    # realm is the connectioInfo from QgsDataSourceURI
    uri = QgsDataSourceURI()
    uri.setConnection(DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, '',  '', int(SSL_MODE))
    connInfo = uri.connectionInfo()
    
    # get credentials if at least there's no PWD
    if not DATABASE_PWD:
        # get credentials and mutate cache => need lock
        QgsCredentials.instance().lock()

        (ok, DATABASE_USER, DATABASE_PWD) = QgsCredentials.instance().get(connInfo, DATABASE_USER, DATABASE_PWD)
        if not ok:
            QgsCredentials.instance().unlock()
            message = 'Refused or Can not get credentials for realm: {} '.format(connInfo)
            QMessageBox.warning(None, "Connection error", message)
            return
        
        # unlock credentials... but not add to cache
        # wait to verify that connection is ok to add into the cache
        QgsCredentials.instance().unlock()
    
    # add user and password if not set in the previous setConnection 
    uri.setConnection(DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PWD, int(SSL_MODE))
    
    # connect
    try:
        connection = psycopg2.connect(uri.connectionInfo().encode('utf-8'))
    except Exception as ex:
        message = 'Can not connect to connection named: {} for reason: {} '.format(name, str(ex))
        QMessageBox.warning(None, "Connection error", message)
        return
    else:
        # last credential were ok, so record them in the cache
        QgsCredentials.instance().lock()
        QgsCredentials.instance().put(connInfo, DATABASE_USER, DATABASE_PWD)
        QgsCredentials.instance().unlock()
            
    
# Signals
def connection_changed():
    value = dlg.ui.cboConnection.currentText()
    # Try to connect. If failed disable Accept button
    open_connection(value)
    
    
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
