import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog,QWidget
import arcpy
import os
import sys

class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage,self).__init__()
        loadUi("GUI_file.ui",self)
        self.Enter1.clicked.connect(self.SelectInputs)
        self.Enter4.clicked.connect(self.SelectCountry)
        
    def SelectInputs(self):
        #user inputing location on disk
        user_input= self.plainTextEdit.toPlainText()
        arcpy.env.workspace=(user_input)
        Fclist=arcpy.ListFeatureClasses()
        self.textEdit.setText(str(Fclist))
    def SelectCountry(self):
        data = self.plainTextEdit_3.toPlainText()
        shops = self.plainTextEdit_4.toPlainText()
        country = self.plainTextEdit_5.toPlainText()
        Selection = self.plainTextEdit_6.toPlainText()
        Directory = self.plainTextEdit_9.toPlainText()
        OutputName = self.plainTextEdit_8.toPlainText()
        OutDir= arcpy.CreateUniqueName(OutputName)
        
        # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
        CountrySELECTION = arcpy.management.SelectLayerByAttribute(data, selection_type="NEW_SELECTION", where_clause = "NAME= '" + country + "'", invert_where_clause="")
        # Process: Select Layer By Location (Select Layer By Location) (management)
        PointSelection= arcpy.management.SelectLayerByLocation(in_layer=[shops], overlap_type="INTERSECT", select_features=CountrySELECTION, search_distance="", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")
        
        # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
        ShopSelection= arcpy.management.SelectLayerByAttribute(in_layer_or_view=PointSelection, selection_type="SUBSET_SELECTION", where_clause= "shop= '" + Selection + "'", invert_where_clause="")
        
        # Process: Copy Features (Copy Features) (management)
        OSMpointCopy_shp = os.path.join(Directory,OutputName)
       
        arcpy.management.CopyFeatures(in_features=ShopSelection, out_feature_class=OSMpointCopy_shp, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)            
        
       
app = QtWidgets.QApplication([]) 
win = MainPage()
win.show()
try:
    sys.exit(app.exec())
except:
    print("EXITING")