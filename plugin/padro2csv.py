#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import csv
from qgis.core import QgsDataSourceURI, QgsCredentials
from PyQt4.QtGui import QFileDialog, QInputDialog, QMessageBox, QComboBox
from PyQt4.QtCore import QSettings
import psycopg2
import psycopg2.extensions
import psycopg2.extras
from padro_estruc import padro_estruc
from ui.padrohabitants_dialog import PadroHabitantsDialog


def main(plugin_dir):
    
    global dlg, settings
    
    # Open dialog
    dlg = PadroHabitantsDialog()
    dlg.show()
       
    # Load local settings of the plugin
    setting_path = os.path.join(plugin_dir, 'config', 'padrohabitants.config')    
    settings = QSettings(setting_path, QSettings.IniFormat)
    
    # Init configuration
    init_config()


def get_connections():
    
    # Get the list of current connections
    conn_list = []
    conn_list.append('')
    qgisSettings = QSettings()
    root = '/PostgreSQL/connections'
    qgisSettings.beginGroup(root)
    for name in qgisSettings.childGroups():
        conn_list.append(name)
        qgisSettings.endGroup()
    return conn_list
    
    
def get_schemas():
    
    sql = "SELECT schema_name FROM information_schema.schemata WHERE schema_name <> 'information_schema' AND schema_name !~ E'^pg_' AND schema_name <> 'drivers' AND schema_name <> 'public' AND schema_name <> 'topology' ORDER BY schema_name" 
    elem = dlg.findChild(QComboBox, "cboSchema")
    elem.clear()    
    elem.addItem("")    
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        elem.addItem(row[0])        
    
    
def init_config():
           
    # Fill connections combo
    conn_list = get_connections()
    dlg.cboConnection.addItems(conn_list)
            
    # Get txt file path, csv file path, db connection name, table name
    TXT_NAME = settings.value('db/TXT_NAME', '')
    dlg.txtInputFilePath.setText(TXT_NAME)
    CSV_NAME = settings.value('db/CSV_NAME', '')
    dlg.txtOutputFilePath.setText(CSV_NAME)
    CONNECTION_NAME = settings.value('db/CONNECTION_NAME', '')
    index = dlg.cboConnection.findText(CONNECTION_NAME)
    dlg.cboConnection.setCurrentIndex(index)
    TABLE_NAME = settings.value('db/TABLE_NAME', '')
    dlg.txtTableName.setText(TABLE_NAME)
    
    # Set signals
    dlg.btnSelectInput.clicked.connect(select_input_file)
    dlg.btnSelectOutput.clicked.connect(select_output_file)
    dlg.cboConnection.currentIndexChanged.connect(connection_changed)
    dlg.btnAccept.clicked.connect(process)
    dlg.btnTxtToCsv.setVisible(False)
    dlg.btnCsvToPg.setVisible(False)    
    
    if index != -1:
        connection_changed()
        schema_name = settings.value('db/SCHEMA_NAME', '')
        index = dlg.cboSchema.findText(schema_name)
        dlg.cboSchema.setCurrentIndex(index)    
        
    
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
    conn_name = dlg.cboConnection.currentText()
    status = open_connection(conn_name)
    dlg.btnAccept.setEnabled(status)
    
    # Fill schemas combo
    if status:
        get_schemas()  
    
    
def select_input_file():
    os.chdir(os.getcwd())
    fileIn = QFileDialog.getOpenFileName(None, "Select input file", "", '*.txt')
    dlg.txtInputFilePath.setText(fileIn)
    fileOut = fileIn.replace(".txt", ".csv")
    dlg.txtOutputFilePath.setText(fileOut)
    fileName = os.path.basename(fileOut)
    dlg.txtTableName.setText(fileName[:-4])


def select_output_file():
    os.chdir(os.getcwd())
    fileOut = QFileDialog.getSaveFileName(None, "Select output file", "", '*.csv')
    dlg.txtOutputFilePath.setText(fileOut)
    fileName = os.path.basename(fileOut)
    dlg.txtTableName.setText(fileName[:-4])


def process():

    # Check if input file exists
    fileIn = dlg.txtInputFilePath.toPlainText()
    if not os.path.isfile(fileIn):
        msg = "El fitxer d'entrada indicat no existeix: \n"+fileIn
        QMessageBox.warning(None, "Fitxer no existeix", msg)
        return
    
    # Check if we have selected output file
    fileOut = dlg.txtOutputFilePath.toPlainText()
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
    file_csv = dlg.txtOutputFilePath.toPlainText()
    if file_csv == '':
        msg = "Cal especificar el fitxer CSV"
        QMessageBox.warning(None, "Fitxer CSV", msg)
        return
        
    # Check if CSV file exists
    if not os.path.isfile(file_csv):
        msg = "El fitxer especificat no existeix:\n"+file_csv
        QMessageBox.warning(None, "Fitxer CSV", msg)
        return
    
    # Get schema name
    schema_name = dlg.cboSchema.currentText()  
    if schema_name == '':
        msg = "Cal seleccionar un esquema"
        QMessageBox.warning(None, "PostGIS", msg)
        return         
        
    # Get table name to generate
    table_name = dlg.txtTableName.text()
    if table_name == '':
        msg = "Cal especificar nom de la taula a generar"
        QMessageBox.warning(None, "PostGIS", msg)
        return
        
    # Check if table_name already exists in the selected schema
    table_exists = False    
    full_table_name = schema_name+"."+table_name    
    sql = "SELECT * FROM pg_tables WHERE schemaname = '"+schema_name+"' AND tablename = '"+table_name+"'"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        table_exists = True
        msg = 'La taula {} ja existeix. Vol sobreescriure-la?'.format(full_table_name)
        reply = QMessageBox.question(None, None, msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
    # Save settings (before processing)
    settings.setValue("db/CONNECTION_NAME", dlg.cboConnection.currentText())
    settings.setValue("db/SCHEMA_NAME", schema_name)
    settings.setValue("db/TABLE_NAME", table_name)
    settings.setValue("db/TXT_NAME", dlg.txtInputFilePath.toPlainText())
    settings.setValue("db/CSV_NAME", dlg.txtOutputFilePath.toPlainText())            
        
    # Escape schema and table name
    if '"' not in schema_name:
        schema_name = '"'+schema_name+'"'
    if '"' not in table_name:
        table_name = '"'+table_name+'"'
    full_table_name = schema_name+"."+table_name  
            
    # Create new table
    if not table_exists:
        sql = "CREATE TABLE "+full_table_name+" ("
        sql2= "codi_provincia text, codi_municipi text, nom text, part_cognom1 text, cognom1 text, part_cognom2 text, cognom2 text, neix_codi_provincia text, neix_codi_municipi text, neix_any text, neix_mes text, neix_dia text, tipus_doc text, letra_estrager text, doc_identitat text, passaport text, nia text, nie text, variacio_any text, variacio_mes text, variacio_dia  text, districte text, seccio text, codi_entitat_colectiva text, codi_entitat_singular text, codi_digit_control text, codi_ncli_disseminat text, nom_entitat_singular text, nom_nucli_disseminat text, codi_via text, tipus_via text, nom_via text, altres text, tipus_numero text, numero text, numero_superior text, punt_quilometric text, hm text, bloc text, escala text, planta text, porta text, tipus_domicili text, full_padronal text, sexe text, nivell_estudis text, pais_nacionalitat text, procedencia_codi_provincia text, procedencia_codi_municipi text, procedencia_codi_consolat text)"
        sql = sql + sql2
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as ex:
            message = 'Cannot create table {} for reason:\n {} '.format(table_name, str(ex))
            QMessageBox.warning(None, "CSV import error", message)
            conn.rollback()
            return False
    else:
        sql = "DELETE FROM "+full_table_name
        cursor.execute(sql)
    
    # Open csv file for read and copy into database
    rf = open(file_csv)
    sql = "COPY "+full_table_name+" FROM STDIN WITH CSV HEADER DELIMITER AS ','"
    try:
        cursor.copy_expert(sql, rf)
        conn.commit()
    except Exception as ex:
        message = 'Cannot import CSV into table {} for reason:\n {} '.format(full_table_name, str(ex))
        QMessageBox.warning(None, "CSV import error", message)
        conn.rollback()
        return False
    
    # Final message
    QMessageBox.information(None, u"Fi procés", u"Procés finalitzat correctament")

    
# Execute script only in QGIS Python console
if __name__ == "__console__":
    main()
