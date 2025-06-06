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
    os.path.dirname(__file__), 'export_plugin_dialog_base.ui'))


class ExportDialog(QtWidgets.QDialog, FORM_CLASS):

    def export_gpkg_path_changed(self):
        self.export_gml_path.setFilePath(self.export_gpkg_path.filePath().replace(".gpkg", ".gml"))

    def accept_export(self):
        if os.path.exists(self.export_gpkg_path.filePath()):
            self.accept()
        else:
            alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                          self.tr("Missing file"),
                                          self.tr("GeoPackage to be exported not found"))
            alert.exec_()

    def __init__(self, tr, parent=None):
        """Constructor."""
        super(ExportDialog, self).__init__(parent)
        self.tr = tr
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.export_gpkg_path.fileChanged.connect(self.export_gpkg_path_changed)

        # default accept function leválasztása, és saját accept (path validációval) rácsatlakoztatása
        self.button_box.accepted.disconnect(self.accept)
        self.button_box.accepted.connect(self.accept_export)
