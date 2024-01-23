# Import necessary modules
import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
import arcpy
import os
import sys

# Define the main window class
class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init()
        
        # Load the user interface from the "GUI_file.ui" file
        loadUi("GUI_file.ui", self)
        
        # Connect signals to slots
        self.Enter1.clicked.connect(self.SelectInputs)
        self.Enter4.clicked.connect(self.SelectCountry)
        
    # Function to handle the user input for location on disk and list feature classes
    def SelectInputs(self):
        # User input for the location on disk
        user_input = self.plainTextEdit.toPlainText()
        
        # Set arcpy environment workspace to the specified location
        arcpy.env.workspace = user_input
        
        # Get the list of feature classes in the workspace
        Fclist = arcpy.ListFeatureClasses()
        
        # Display the list of feature classes in the textEdit widget
        self.textEdit.setText(str(Fclist))
    
    # Function to perform the selection of shops based on user input
    def SelectCountry(self):
        # Get user inputs from the plainTextEdit widgets
        data = self.plainTextEdit_3.toPlainText()
        shops = self.plainTextEdit_4.toPlainText()
        country = self.plainTextEdit_5.toPlainText()
        Selection = self.plainTextEdit_6.toPlainText()
        Directory = self.plainTextEdit_9.toPlainText()
        OutputName = self.plainTextEdit_8.toPlainText()
        
        # Create a unique output name using arcpy function
        OutDir = arcpy.CreateUniqueName(OutputName)
        
        # Select features based on attribute and location
        CountrySELECTION = arcpy.management.SelectLayerByAttribute(data, selection_type="NEW_SELECTION", where_clause="NAME= '" + country + "'", invert_where_clause="")
        PointSelection = arcpy.management.SelectLayerByLocation(in_layer=[shops], overlap_type="INTERSECT", select_features=CountrySELECTION, search_distance="", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")
        ShopSelection = arcpy.management.SelectLayerByAttribute(in_layer_or_view=PointSelection, selection_type="SUBSET_SELECTION", where_clause="shop= '" + Selection + "'", invert_where_clause="")
        
        # Copy selected features to a new location
        OSMpointCopy_shp = os.path.join(Directory, OutputName)
        arcpy.management.CopyFeatures(in_features=ShopSelection, out_feature_class=OSMpointCopy_shp, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)            

# Create the PyQt application instance
app = QtWidgets.QApplication([]) 

# Create an instance of the MainPage class
win = MainPage()

# Show the MainPage
win.show()

# Start the application event loop
try:
    sys.exit(app.exec())
except:
    print("EXITING")
