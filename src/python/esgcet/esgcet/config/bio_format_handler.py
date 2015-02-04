"""-*- Python -*-
Format handler template.

To create a format handler:

    - Modify the methods in CustomFormatHandler as needed. See the documentation
      for FormatHandler class.
      
      Note: The handler class name is arbitrary, provided it matches
      the setup.py 'handler' entry point of the esgcet.format_handlers group.

      Note: This template extends the default netCDF/Cdunif handler. To start
      from scratch, inherit from FormatHandler instead, and implement
      the methods.
      
    - Install the handler package:

        python setup.py --verbose install
        
    - In esg.ini, associate the format and handler name, e.g.:

        [project:my_project]
        ...
        format_handler = <format_handler_name>
"""
from esgcet.exceptions import *
import esgcet.messaging
from esgcet.config import FormatHandler

class BioFormatHandler(FormatHandler):

    def __init__(self, file, path):
        self.file = file
        self.path = path

    @staticmethod
    def open(path, mode='r'):
        """
        Open a file.

        Returns an instance of the format handler. 

        path
          String path name.

        mode
          String mode. Since only mode='r' (read-only) is currently used, it is optional.
        """
        f = open(path, mode=mode)

        return BioFormatHandler(f, path)

    @staticmethod
    def getFormatDescription():
        """Get a desription of the format.

        Returns a string format descriptions.

        """
        return "ascii-tabular"

    def close(self):
        """
        Close the file.
        """
        self.file.close()
    
    def inquireVariableList(self):
        """
        Inquire the variable names.

        Returns a list of string variable names.
        """
        print self.path

        if "Cases" in self.path:
            return ["Cases"]
        elif "Incidence" in self.path:
            return ["Incidence"]
        else:
#            warning("Unknown variable name in " + self.path)
            return []

    def inquireVariableDimensions(self, variableName):
        """
        Inquire the dimension names of a variable.

        Returns a list of string dimension names of the variable.
        """
        return ["location","time"]

    def inquireAttributeList(self, variableName=None):
        """
        Inquire global or variable attribute names.

        Returns a list of attribute names.

        variableName
          String variable name. If None, return the global attribute list.
        """
        return []

    def getAttribute(self, attributeName, variableName, *args):
        """
        Get the value of a global or variable attribute.

        Returns the attribute value, as an int, float, or 1-d numpy array.

        attributeName
          String name of the attribute.

        variableName:
          String name of the variable. If None, get a global attribute.

        args
          optional default value if the attribute is not found.
        """
        return None

    def hasVariable(self, variableName):
        """
        Returns True iff a file has the given variable.

        variableName:
          String name of the variable.
        """
        if variableName in ["Cases", "Deaths", "Incidence"]:
            return True
        else:
            return False

    def hasAttribute(self, attributeName, variableName=None):
        """
        Returns True iff a file or variable has an attribute.

        attributeName
          String name of the attribute.

        variableName:
          String name of the variable. If None, check a global attribute.
        """
        return None

    def inquireVariableShape(self, variableName):
        """
        Get the shape of the variable multidimensional array.

        Returns a tuple of ints.

        variableName
          String name of the variable.
        """
        return [1,1]

    def getVariable(self, variableName, index=None):
        """
        Get the value of the variable.

        Returns a numpy array.

        variableName
          String name of the variable.

        index
          Integer index to select along the first dimension. If None, return all values.
          
        """
        return []

