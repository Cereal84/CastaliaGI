#!/usr/bin/env python
""" Castalia Graphip Interface
	
This software allows the user to call Castalia command using a graphic interface 
 to execute the simulations that he want to do allowing he to select them from a
 list of available configurations.

	Date: 28/Jun/2013
"""

__author__ = "Alessandro Pischedda"
__email__ = "alessandro.pischedda@gmail.com"
__copyright__ = "Copyright 2009"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Alessandro Pischedda"

import sys
import re
 
try:
	# Import Qt modules
	from PyQt4 import QtCore, QtGui
except ImportError:
    print "Library PyQt4 missing, install it"


# Import the compiled UI module
from CastaliaUI import Ui_MainWindow

import subprocess


def loadConfig():
	""" read the omnet.ini file and find the configurations name. """

	try:	
		in_file = open("omnetpp.ini","r")
		file_content = in_file.read()
	except IOError:
		print "Error: can\'t find file omnetpp.ini or read data"
		sys.exit(-1)
	
	in_file.close()

	# there is always an entry called "General"
	names = ["General"]

	# find all [Config <something>] match in the
	matches = re.findall(r"Config [a-zA-Z0-9]+", file_content)
	
	# for each match we clean it in order to have only the name of the configuration
	for match in matches:
		name = match.replace("Config", "")
		name = name.replace(" ","")
		names.append(name)

	return names


# Create a class for our main window
class Main(QtGui.QMainWindow):
	def __init__(self, config_names):
		QtGui.QMainWindow.__init__(self)

		# This is always the same
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)

		# models used in the respective listView	
		self.model_available = QtGui.QStandardItemModel()
		self.model_selected = QtGui.QStandardItemModel()

		# fill the listView with all the configuration names
		self.fillConfigAvailable(config_names)

		# connect the buttons press with the correct function
		self.ui.button_add.clicked.connect(self.addConf)
		self.ui.button_remove.clicked.connect(self.rmConf)
		self.ui.button_execute.clicked.connect(self.executeCastalia)

		# set multiselection in the lists
		self.ui.list_conf_available.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		self.ui.list_conf_selected.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

	def fillConfigAvailable(self, configs):

		for conf in configs:
			# Create an item with a caption
			item = QtGui.QStandardItem(conf)
			self.model_available.appendRow(item)
		
		self.ui.list_conf_available.setModel(self.model_available)
		

	def addConf(self):
		""" add selected item to list_conf_selected """

		selected = []
		already_present = []

		# retrieve all the configuration in list_conf_available
		indexes = self.ui.list_conf_available.selectedIndexes()
		for index in indexes:
			selected.append (self.model_available.itemFromIndex(index).text() )

		# retrieve all the configuration in list_conf_selected
		# look in its model		
		row_count = self.model_selected.rowCount()
 
		for row in range(row_count):
			already_present.append(self.model_selected.item(row).text())

		# compute the new names not already presents in list_conf_selected 
		new_names = list(set(selected) - set(already_present))
		
		# add to the list_conf_selected the new names
		for name in new_names:
			# Create an item with a caption
			item = QtGui.QStandardItem(name)
			self.model_selected.appendRow(item)
		
		self.ui.list_conf_selected.setModel(self.model_selected)
		
		# un-select the list_conf_available		


	def rmConf(self):
		""" delete the selected names from list_conf_selected """

		indexes = self.ui.list_conf_selected.selectedIndexes()
		for index in indexes:
			self.model_selected.removeRow(index.row())

		self.ui.list_conf_selected.setModel(self.model_selected)
		

	def executeCastalia(self):
		""" it's time to execute Castalia to start the simulation/s """

		error = False
	
		# retrieve the number of the runs
		# print a error if is something different from a number
		try:
			runs = int( self.ui.run_number.displayText() )
		except ValueError:
			# show a dialog
			QtGui.QMessageBox.warning(self, "Warning", "Must use only integer number.")
			error = True
			

		# if there is not any configuration in "Selected" or no run number
		# print a message
		row_count = self.model_selected.rowCount()
		configs = []
		if  row_count == 0:
			QtGui.QMessageBox.warning(self, "Warning","You must selected almost one configuration.")
			error = True
		else:
			for row in range(row_count):
				configs.append( str(self.model_selected.item(row).text()) )

		# ok everythings seems fine, time to execute Castalia and wait it
		if not error:
			command = "Castalia -c "
			for i in range(len(configs)):
				if i == 0:
					command += configs[i]
				else:
					command += ","+configs[i]

			command += " -r "+str(runs)

			# disable the execute button until the simulation/s is/are not ended
			self.ui.button_execute.setDisabled(True) 

			# call and wait
			subprocess.call(command, shell=True, stderr=None, stdout=None )

			QtGui.QMessageBox.information(self, "End", "Simulations ended")

			# ok simulations ended
			self.ui.button_execute.setDisabled(False) 
			

def main():

	# retrieve all the configurations
	configs = loadConfig()

	app = QtGui.QApplication(sys.argv)
	window=Main(configs)
	window.show()
	# It's exec_ because exec is a reserved word in Python
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
