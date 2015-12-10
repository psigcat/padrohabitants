# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PadroHabitatns - A QGIS plugin
                              -------------------
        begin                : 2015-12-01
        git sha              : $Format:%H$
        copyright            : (C) 2015 by David Erill
        email                : daviderill79@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.utils import active_plugins
from qgis.gui import (QgsMessageBar)
from qgis.core import (QgsGeometry, QgsLogger)
from PyQt4.QtCore import * # @UnusedWildImport
from PyQt4.QtGui import *  # @UnusedWildImport
import os.path
import sys  
import resources_rc        # @UnusedWildImport
import padro2csv


class PadroHabitants(QObject):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        super(PadroHabitants, self).__init__()
        
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        self.pluginName = os.path.basename(self.plugin_dir)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.plugin_dir, 'i18n', 'PadroHabitants_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        
        # load local settings of the plugin
        settingFile = os.path.join(self.plugin_dir, 'config', 'padrohabitants.config')
        self.settings = QSettings(settingFile, QSettings.IniFormat)
        self.settings.setIniCodec(sys.getfilesystemencoding())
        
        # load plugin settings
        self.loadPluginSettings()            
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PadroHabitants')
    
    
    def loadPluginSettings(self):
        ''' Load plugin settings
        '''
        # Create own plugin toolbar or not?
        self.pluginToolbarEnabled = bool(int(self.settings.value('status/pluginToolbarEnabled', 0)))
        if self.pluginToolbarEnabled:
            self.toolbar = self.iface.addToolBar(u'PadroHabitants')
            self.toolbar.setObjectName(u'PadroHabitants')
            
        
    def createToolButton(self, parent, text):
        button = QToolButton(parent)
        button.setObjectName(text)
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button.setPopupMode(QToolButton.MenuButtonPopup)
        parent.addWidget(button)
        return button

        
    def createAction(self, icon_path, text, callback, parent, add_to_toolbar=True, add_to_menu=True):
        
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)    
        action.toggled.connect(callback)
        action.setCheckable(True)
        
        if add_to_toolbar:
            self.toolbar.addAction(action)
        else:
            self.iface.addToolBarIcon(action)       
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)
            
        self.actions.append(action)
        
        return action
    
        
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/PadroHabitants/icon_padrohabitants.png'
        self.actionPoint = self.createAction(icon_path, self.tr(u'CSV to PostGIS'), self.run, self.iface.mainWindow(), self.pluginToolbarEnabled)
    
    
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&infoplus'), action)
            self.iface.removeToolBarIcon(action)
            
        if self.pluginToolbarEnabled:
            # Remove the plugin menu item and icon
            #self.iface.mainWindow().removeToolBar(self.toolbar)          
            del self.toolbar
                        
    
    def run(self):
        print "HELLO"
        reload(padro2csv)
        padro2csv.main()
        #padro2csv.padro2csv("aa.txt")        


