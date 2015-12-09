#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import csv
from qgis.core import QgsDataSourceURI
from PyQt4.QtGui import QFileDialog, QInputDialog, QMessageBox
from PyQt4.QtCore import QSettings
import psycopg2
import psycopg2.extensions
import psycopg2.extras
from padro_estruc import padro_estruc
from padrohabitants_dialog import PadroHabitantsDialog


def main():
    
    # Open dialog
    global dlg, settings, SCHEMA_NAME
    SCHEMA_NAME = "data"
    dlg = PadroHabitantsDialog()
    dlg.show()
       
    # Load local settings of the plugin
    settingFile = os.path.join(os.getcwd(), 'config', 'padrohabitants.config')
    settings = QSettings(settingFile, QSettings.IniFormat)
    
    # Init configuration
    init_config()
    
    # Set signals
    dlg.ui.btnSelectInput.clicked.connect(select_input_file)
    dlg.ui.btnSelectOutput.clicked.connect(select_output_file)
    dlg.ui.cboConnection.currentIndexChanged.connect(connection_changed)
    dlg.ui.btnAccept.clicked.connect(process)
    dlg.ui.btnTxtToCsv.setVisible(False)
    dlg.ui.btnCsvToPg.setVisible(False)


def get_connections():
    
    # get the list of current connections
    conn_list = []
    conn_list.append('')
    qgisSettings = QSettings()
    root = '/PostgreSQL/connections'
    qgisSettings.beginGroup(root)
    for name in qgisSettings.childGroups():
        conn_list.append(name)
        qgisSettings.endGroup()
    return conn_list
    
    
def init_config():
    
    # Fill connections combo
    conn_list = get_connections()
    dlg.ui.cboConnection.addItems(conn_list)
        
    # Get txt file path, csv file path, db connection name, table name
    TXT_NAME = settings.value('db/TXT_NAME', '')
    dlg.ui.txtInputFilePath.setText(TXT_NAME)
    CSV_NAME = settings.value('db/CSV_NAME', '')
    dlg.ui.txtOutputFilePath.setText(CSV_NAME)
    CONNECTION_NAME = settings.value('db/CONNECTION_NAME', '')
    index = dlg.ui.cboConnection.findText(CONNECTION_NAME)
    dlg.ui.cboConnection.setCurrentIndex(index)
    TABLE_NAME = settings.value('db/TABLE_NAME', '')
    dlg.ui.txtTableName.setText(TABLE_NAME)
    
    
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
            return False
        
        # unlock credentials... but not add to cache
        # wait to verify that connection is ok to add into the cache
        QgsCredentials.instance().unlock()
    
    # add user and password if not set in the previous setConnection 
    uri.setConnection(DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PWD, int(SSL_MODE))
    
    # Try to connect
    global conn, cursor
    try:
        conn = psycopg2.connect(uri.connectionInfo().encode('utf-8'))
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except Exception as ex:
        message = 'Can not connect to connection named: {} for reason: {} '.format(name, str(ex))
        QMessageBox.warning(None, "Connection error", message)
        return False
    else:
        # last credential were ok, so record them in the cache
        QgsCredentials.instance().lock()
        QgsCredentials.instance().put(connInfo, DATABASE_USER, DATABASE_PWD)
        QgsCredentials.instance().unlock()
        return True
            
    
# Signals
def connection_changed():
    
    # Try to connect. If failed disable Accept button    
    value = dlg.ui.cboConnection.currentText()
    status = open_connection(value)
    dlg.ui.btnAccept.setEnabled(status)
    
    
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
    dlg.ui.txtTableName.setText(fileName[:-4])


def process():

    # Check if input file exists
    fileIn = dlg.ui.txtInputFilePath.toPlainText()
    if not os.path.isfile(fileIn):
        msg = "El fitxer d'entrada indicat no existeix: \n"+fileIn
        QMessageBox.warning(None, "Fitxer no existeix", msg)
        return
    
    # Check if we have selected output file
    fileOut = dlg.ui.txtOutputFilePath.toPlainText()
    if fileOut == '':
        msg = "Cal especificar un fitxer de sortida"
        QMessageBox.warning(None, "Fitxer de sortida", msg)
        return
    
    # TXT file to CSV
    padro2csv(fileIn, fileOut)
    
    # CSV file to PostGIS
    csv2postgis()
    
    
def padro2csv(fileIn, fileOut=None):
    
    # Open file for read txt (from padro habitants)
    rf = open(fileIn)
    
    askQuestion = False
    if fileOut == None:
        askQuestion = False
        fileOut = fileIn.replace(".txt", ".csv")

    # Openfile to write csv
    with open(fileOut, 'wb') as wf:
        writer = csv.writer(wf)
        writer.writerow(zip(*padro_estruc[1])[3])
        # read lines from txt
        for line in rf.readlines():
            line = line.decode("UTF8")
            row = []
            # Iterate over all features
            for campos in padro_estruc[1]:
                ini = campos[0]-1 # offset
                fin = ini + campos[1] # longitud
                valor = line[ini:fin].strip().encode("UTF8") # valor
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


def csv2postgis():
    
    # Get CSV file
    fileCsv = dlg.ui.txtOutputFilePath.toPlainText()
    if fileCsv == '':
        msg = "Cal especificar el fitxer CSV"
        QMessageBox.warning(None, "Fitxer CSV", msg)
        return
        
    # Check if CSV file exists
    if not os.path.isfile(fileCsv):
        msg = "El fitxer especificat no existeix:\n"+fileCsv
        QMessageBox.warning(None, "Fitxer CSV", msg)
        return
    
    # Get table name to generate
    tableName = dlg.ui.txtTableName.text()
    if tableName == '':
        msg = "Cal especificar nom de la taula a generar"
        QMessageBox.warning(None, "PostGIS", msg)
        return
        
    # Check if tableName already exists
    # We deal with schema name and ""
    tableExists = False
    aux = tableName
    index = aux.find(".")
    if index > -1:
        aux = aux[index+1:]
        print aux
    aux = aux.replace('"', '')
    sql = "SELECT * FROM pg_tables WHERE tablename = '"+aux+"'"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        tableExists = True
        msg = 'La taula {} ja existeix. Vol sobreescriure-la?'.format(tableName)
        reply = QMessageBox.question(None, None, msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.No:
            return False
        
    # Escape table name
    if '"' not in tableName:
        tableName = '"'+tableName+'"'
        
    # Prefix schema only if not set in tableName
    if '.' not in tableName:
        tableName = SCHEMA_NAME+"."+tableName
        
    # Create new table
    if not tableExists:
        sql = "CREATE TABLE "+tableName+" ("
        sql2= "codi_provincia text, codi_municipi text, nom text, part_cognom1 text, cognom1 text, part_cognom2 text, cognom2 text, neix_codi_provincia text, neix_codi_municipi text, neix_any text, neix_mes text, neix_dia text, tipus_doc text, letra_estrager text, doc_identitat text, passaport text, nia text, nie text, variacio_any text, variacio_mes text, variacio_dia  text, districte text, seccio text, codi_entitat_colectiva text, codi_entitat_singular text, codi_digit_control text, codi_ncli_disseminat text, nom_entitat_singular text, nom_nucli_disseminat text, codi_via text, tipus_via text, nom_via text, altres text, tipus_numero text, numero text, numero_superior text, punt_quilometric text, hm text, bloc text, escala text, planta text, porta text, tipus_domicili text, full_padronal text, sexe text, nivell_estudis text, pais_nacionalitat text, procedencia_codi_provincia text, procedencia_codi_municipi text, procedencia_codi_consolat text)"
        sql = sql + sql2
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as ex:
            message = 'Cannot create table {} for reason:\n {} '.format(tableName, str(ex))
            QMessageBox.warning(None, "CSV import error", message)
            conn.rollback()
            return False
    else:
        sql = "DELETE FROM "+tableName
        cursor.execute(sql)
    
    # Open csv file for read and copy into database
    rf = open(fileCsv)
    sql = "COPY "+tableName+" FROM STDIN WITH CSV HEADER DELIMITER AS ','"
    try:
        cursor.copy_expert(sql, rf)
        conn.commit()
    except Exception as ex:
        message = 'Cannot import CSV into table {} for reason:\n {} '.format(tableName, str(ex))
        QMessageBox.warning(None, "CSV import error", message)
        conn.rollback()
        return False
        
    # Save settings
    settings.setValue("db/CONNECTION_NAME", dlg.ui.cboConnection.currentText())
    settings.setValue("db/TABLE_NAME", tableName)
    settings.setValue("db/TXT_NAME", dlg.ui.txtInputFilePath.toPlainText())
    settings.setValue("db/CSV_NAME", dlg.ui.txtOutputFilePath.toPlainText())    
    
    # Final message
    QMessageBox.information(None, u"Fi procés", u"Procés finalitzat correctament")

    
# Execute script only in QGIS Python console
if __name__ == "__console__":
    main()
