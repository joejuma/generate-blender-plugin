"""
	Generate Blender Plugin Base
	v2.0.0
	For Blender v3.0.0+
	By Joseph Juma
	---------------------------------------------------------------------------
	A script for creating a basic blender plugin from a template, with basic
	info filled into the docstrings of the file.
	===========================================================================
"""

# Dependencies
import signal
import sys

# Functions
def readFile( path ):
	""" Read data from a file """
	
	fileHandle = open( path, "r", encoding="utf-8" )
	data = fileHandle.read()
	fileHandle.close()
	
	return data

def writeFile( path, data ):
	""" Write data to a file """
	
	fileHandle = open( path, "w", encoding="utf-8" )
	fileHandle.write(data)
	fileHandle.close()
	
	return

def displayOptions( options ):
	""" Display a list of options """
	for v in options:
		print(v['id'],"\n",v['description'],"\n")
	return
	
def handleSIGINT( sig, context ):
	""" Handles an interrupt signal (SIGNIT) """
	print("\nCtrl+C pressed, exiting...")
	sys.exit(0)
	return
	
	
# Constants
operatorOptions = [
	{'id':"REGISTER",'description':"Register the addon. Always start with this!"},
	{'id':"UNDO",'description':"Allows for you to undo the operator"},
	{'id':"UNDO_GROUPED",'description':"Allows you to do a single undo to effect many executions of this operator"},
	{'id':"BLOCKING",'description':"Operation blocking! It s tops anything else from using the cursor until it's done."},
	{'id':"MACRO",'description':"Is this operator a macro? Please set this!"},
	{'id':"GRAB_CURSOR",'description':"Takes hold of the mouse focus"},
	{'id':"GRAB_CURSOR_X",'description':"Grab the cursor's X axis value"},
	{'id':"GRAB_CURSOR_Y",'description':"Grab the cursor's Y axis value"},
	{'id':"PRESET",'description':"Display a default version of the operator's settings"},
	{'id':"INTERNAL",'description':"Removes the operator from search, as it's for internal blender use by ID in code and not user use!"}
]

# Note to self: probably need to update some of these descriptions later for clarity.
values = [
	{'description': "Plugin Name", 'id': "PLUGIN_NAME"},
	{'description': "Author", 'id': "AUTHOR"},
	{'description': "Repository URL(Optional)", 'id':"REPO_URL"},
	{'description': "Plugin summary", 'id':"PLUGIN_SUMMARY"},
	{'description': "Plugin Name (in Blender)", 'id':"BL_PLUGIN_NAME"},
	{'description': "Plugin Category", 'id':"BL_CATEGORY"},	# This one is a multi-select
	{'description': "Plugin Class Name (ThisStyleOnly)", 'id':"PLUGIN_CLASS_NAME"},
	{'description': "Plugin ID (ex: 'object.my_plugin')", 'id':"BL_PLUGIN_ID_NAME"},
	{'description': "Plugin Label (for searching)", 'id':"BL_PLUGIN_LABEL"},
	{'description': "Plugin Options", 'id':"BL_OPTIONS"}, # Another multi-select
	{'description': "Describe what the plugin does when it executes", 'id':"PLUGIN_EXECUTE_DESCRIPTION"}
]

# Main
if __name__ == "__main__":
	
	# Setup a SIGINT handler,
	signal.signal(signal.SIGINT, handleSIGINT)
	
	# For each value, populate a dictionary with the user's input.
	vals = {}
	for k in values:
		if(k['id'] != 'BL_OPTIONS'):
			vals[k['id']] = input((k['description'] + ":  "))
		else:
			print(k['description'])
			displayOptions(operatorOptions)
			vals[k['id']] = input("Please enter a comma separate list:\n")
	
	# Perform processing on specific values
	options = vals['BL_OPTIONS'].split(",")
	newOptions = list(map( lambda x: '"'+(x.strip())+'"', options))
	vals['BL_OPTIONS'] = ",".join(newOptions)
	
	# Load the template
	pluginCode = readFile("./blender_plugin.template")
	
	# Insert the values into the template
	for k in vals:
		p = "<%" + k + "%>"
		pluginCode = pluginCode.replace(p,vals[k])
	
	# Get user's intended filename for this plugin
	filename = input("Filename\n")
	
	# Save as a new file
	writeFile(filename, pluginCode)

	print("Plugin code generated!")