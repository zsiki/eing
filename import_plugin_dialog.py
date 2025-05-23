# -*- coding: utf-8 -*-
"""
/***************************************************************************

                       EING GML import/export plugin

 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-11-20
        copyright            : (C) 2024 by Tigra Kft.
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'import_plugin_dialog_base.ui'))


class ImportDialog(QtWidgets.QDialog, FORM_CLASS):
    """ Dialog to specify input gml file and output GeoPackage """
    def import_gml_path_changed(self):
        """ update gpkg field """
        self.import_gpkg_path.setFilePath(self.import_gml_path.filePath().replace(".gml", ".gpkg"))

    def accept_import(self):
        """ Custom accept method to check fields """
        if len(self.import_gpkg_path.filePath()) == 0 or \
           len(self.import_gml_path.filePath()) == 0:
            alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                          self.tr("Empty field"),
                                          self.tr("Fill both fields"))
            alert.exec_()
            return
        if not os.path.exists(self.import_gml_path.filePath()):
            alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                          self.tr("Misisng file"),
                                          self.tr("GML file does not exist"))
            alert.exec_()
            return
        if os.path.exists(self.import_gpkg_path.filePath()):
            alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                          self.tr("Existing file"),
                                          self.tr("GeoPackage already exists"))
            alert.exec_()
            return
        self.accept()

    def __init__(self, tr, parent=None):
        """Constructor."""
        super(ImportDialog, self).__init__(parent)
        self.tr = tr
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.import_gml_path.fileChanged.connect(self.import_gml_path_changed)

        # default accept function leválasztása, és saját accept (path validációval) rácsatlakoztatása
        self.button_box.accepted.disconnect(self.accept)
        self.button_box.accepted.connect(self.accept_import)
