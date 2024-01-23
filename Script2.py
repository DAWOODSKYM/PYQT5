# Import necessary modules
import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
import arcpy
import os
import sys

# Define the main window class
class WelcomeWindow(QMainWindow):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        
        # Load the user interface from the "shops.ui" file
        loadUi("shops.ui", self)       
        
        # Connect signals to slots
        self.ENTER.clicked.connect(self.SetDirectory)
        self.pushButton.clicked.connect(self.Extraction)

    # Function to set the working directory and populate feature lists
    def SetDirectory(self):
        # Get the working directory from the plain text edit widget
        Working_Directory = self.plainTextEdit.toPlainText()
        
        # Set the arcpy environment workspace to the specified directory
        arcpy.env.workspace = Working_Directory
        
        # Get the list of feature classes in the workspace
        Featurelist = arcpy.ListFeatureClasses()
        
        # Populate the combo boxes with the list of feature classes
        self.country_comb.addItems(Featurelist)
        self.comboBox_2.addItems(Featurelist)

    # Function to perform the extraction based on user input
    def Extraction(self):
        # Get selected values from UI elements
        countries = self.country_comb.currentText()
        shop = self.comboBox_2.currentText()
        Country = self.lineEdit_4.text()
        shopType = self.lineEdit_5.text()
        outpath = self.lineEdit.text()
        
        # Create feature layers for the selected country and shop
        s_layer = arcpy.MakeFeatureLayer_management(shop, 'shops_layer')
        c_layer = arcpy.MakeFeatureLayer_management(countries, 'countries_layer')
        
        # Select the specified country by attribute
        country = arcpy.SelectLayerByAttribute_management(c_layer, 'NEW_SELECTION', "NAME= '" + Country + "'")
        
        # Select shops within the selected country using location-based selection
        shops_out = arcpy.SelectLayerByLocation_management(s_layer, "INTERSECT", country, "", "NEW_SELECTION", "NOT_INVERT")
        
        # Select shops of the specified type by attribute
        SHOPS = arcpy.SelectLayerByAttribute_management(s_layer, 'SUBSET_SELECTION', "shop= '" + shopType + "'")
        
        # Write the selected shops to a new feature class in the specified output path
        output = arcpy.FeatureClassToFeatureClass_conversion(SHOPS, outpath, 'shops')

# Create the PyQt application instance
app = QtWidgets.QApplication([]) 

# Create an instance of the WelcomeWindow class
Welcome = WelcomeWindow()

# Show the WelcomeWindow
Welcome.show()

# Start the application event loop
sys.exit(app.exec())
