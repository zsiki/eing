"""
   Load layers from a GeoPackage and order by geometry type
"""
import os.path
from osgeo import ogr
from qgis.core import QgsProject

class GpkgLoader():
    """ loader class for GeoPackage
        :param iface: QGIS iface object
    """
    def __init__(self, iface, tr):
        """ initialize """
        self.iface = iface
        self.tr = tr
        self.plugin_dir = os.path.dirname(__file__)

    def load_layers(self, gpkg_path, layer_list=None):
        """ Load layers from GeoPackage

            :param gpkg_path: path to GeoPackage file
            :param layer_list: list of layer names to load
        """
        ogr.UseExceptions()
        gpkg_data_source = ogr.Open(gpkg_path)
        if layer_list is None or len(layer_list) == 0:
            # get geometry types and layer names from GeoPackage
            layers = [(l.GetGeomType(), l.GetName()) for l in gpkg_data_source]
        else:
            layers = [(l.GetGeomType(), l.GetName()) for l in gpkg_data_source
                      if l.GetName() in layer_list]
        layers.sort(reverse=True)
        for _, layer in layers:
            vlayer = self.iface.addVectorLayer(gpkg_path +
                                               "|layername=" + layer,
                                               layer, 'ogr')
            if vlayer:
                # try to load qml style
                qml_path = os.path.join(self.plugin_dir, "styles",
                                        layer + ".qml")
                if os.path.exists(qml_path):
                    vlayer.loadNamedStyle(qml_path)
                else:
                    qml_path = os.path.join(self.plugin_dir, "styles",
                                            "default.qml")
                    if os.path.exists(qml_path):
                        vlayer.loadNamedStyle(qml_path)
                # set visibility off on empty layers
                if vlayer.featureCount() == 0:
                    node = QgsProject.instance().layerTreeRoot().findLayer(vlayer.id())
                    if node:
                        node.setItemVisibilityChecked(False)
            else:
                self.iface.messageBar().pushMessage("GeoPackage",
                                                    self.tr("Cannot load layer: ")
                                                    + layer,
                                                    level = Qgis.Warning,
                                                    duration = 5)
