import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication,QMainWindow,QDialog,QWidget
import arcpy
import os
import sys

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super(WelcomeWindow,self).__init__()
        loadUi("shops.ui",self)       
        self.ENTER.clicked.connect(self.SetDirectory)
        self.pushButton.clicked.connect(self.Extraction)
    #Function to get the data to work on
    def SetDirectory(self):
        Working_Directory= self.plainTextEdit.toPlainText()
        arcpy.env.workspace=(Working_Directory)
        Featurelist=arcpy.ListFeatureClasses()
        self.country_comb.addItems(Featurelist)
        self.comboBox_2.addItems(Featurelist)
    #Function to extract all shops in country
    def Extraction(self):
        countries =self.country_comb.currentText()
        shop = self.comboBox_2.currentText()
        Country = self.lineEdit_4.text()
        shopType = self.lineEdit_5.text()
        outpath = self.lineEdit.text()
        s_layer=arcpy.MakeFeatureLayer_management(shop, 'shops_layer')
        c_layer=arcpy.MakeFeatureLayer_management(countries, 'countries_layer')
        #selection by attribute
        country=arcpy.SelectLayerByAttribute_management(c_layer,'NEW_SELECTION',"NAME= '" + Country + "'")
        #selection by location
        # Process: Select Layer By Location
        shops_out = arcpy.SelectLayerByLocation_management(s_layer, "INTERSECT", country, "", "NEW_SELECTION", "NOT_INVERT")
         #selection by attribute
        SHOPS=arcpy.SelectLayerByAttribute_management(s_layer,'SUBSET_SELECTION',"shop= '" + shopType + "'")  
        #Writting selected outputs
        output=arcpy.FeatureClassToFeatureClass_conversion(SHOPS, outpath, 'shops')  
             
app = QtWidgets.QApplication([]) 
Welcome = WelcomeWindow()
Welcome.show()
sys.exit(app.exec())
