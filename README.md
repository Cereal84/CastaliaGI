Castalia Graphic Interface
==========================

This software allows the user to call Castalia command using a graphic interface to execute the simulations that he want to do allowing he to select them from a list of available configurations.



Requirements
------------
 ------------

* Python 2.7
* PyQt4
* You have added Castalia/bin/ in your PATH env variable as explained in the Castalia manual.

Support
-------
 -------

* Castalia 3.2


Install
-------
 -------

Copy the files CastaliaGI.py and CastaliaUI.pyc in the directory /bin of Castalia.
Check if CastaliaGI.py has the execution permission, if not you add it ( i.e 
using Linux you must use chmod +x command).


Usage
-----
 -----

Open the shell and go to the directory of the particular simulation and type:

		$ CastaliaGI.py

after that a window appears. On the left you find all the configuration names stored in omnetpp.ini.
If you want execute some of them select that you are interested for and click on add button, you should see them on the right list.
Insert the number of run in the text line in the bottom of the window and click on "Execute" to start the simulations.
The "Remove" button delete the selected configuration from the right list.
 
Changes
-------
 -------

v 0.2
-----
* You can choose a configuration file different from the default one, omnetpp.ini, like -i option.


Author
------
 ------

Alessandro Pischedda


Contact
-------
 -------
alessandro.pischedda@gmail.com
