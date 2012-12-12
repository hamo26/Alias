'''
Created on Jan 22, 2012

@author: Hamid
'''

import subprocess
import os
import xml.dom.minidom as minidom
import sys

class AliasCommand(object):
    """Base command object with arguments.
       Decided to abstract into class to possibly allow forking in the near future."""
    
    def __init__ (self, 
                  command, 
                  path, 
                  commandArgs):
        self.__command = command
        self.__path = path
        self.__command_args = commandArgs
    
    def executeCommand(self):
        self.__command_args.insert(0,self.__command)
        self.__command_args.append(sys.argv[2:])
        sys.stdout.flush()
        subprocess.call(self.__command_args,shell=True,)

class ExceptionConstants:
    ERROR_PARSING_XML  = "Error parsing xml file"
    DUPLICATE_ALIAS    = "Found more than one matching alias"
    ALIAS_NOT_FOUND    = "Alias not found"
    CONFIG_NOT_FOUND   = "xml configuration file not found"

class DomConstants:
    FILE_PATH     = "path"
    DEFAULT_PATH  = "."
    ALIAS_NAME    = "name"
    ALIAS_COMMAND = "command"
    ARGUMENT      = "arg"
    DEFAULT_PATH  = "alias_config.xml"
    
class DomHelper (object):
    """Helper class to parse DOM"""
    
    def __init__ (self, path=DomConstants.DEFAULT_PATH):
        try:
            self.__dom = minidom.parse(path, None)
        except Exception as e:
            print ExceptionConstants.ERROR_PARSING_XML , e
            os._exit(0)
    
    def getAlias (self, alias):
        matchingAlias = self.__dom.getElementsByTagName(alias)
        
        if matchingAlias.length > 1:
            raise Exception(ExceptionConstants.DUPLICATE_ALIAS)
        elif(matchingAlias is None):
            raise Exception(ExceptionConstants.ALIAS_NOT_FOUND)
        
        return self.__constructCommand(matchingAlias[0])
    
    def __constructCommand(self, alias):
        command = AliasCommand(alias.getAttribute(DomConstants.ALIAS_COMMAND), 
                               alias.getAttribute(DomConstants.FILE_PATH),
                               self.__populateArguments(alias))
        return command
    
    def __populateArguments(self, alias):
        arguments = []
        for argument in alias.getElementsByTagName(DomConstants.ARGUMENT):
            arguments.append(argument.firstChild.data)
        return arguments
        
                

if __name__ == '__main__':
    """Future improvement would be to use optparse"""
    for file_path in os.getenv("PATH").split(";"):
        xmlConfiguration = os.path.join(file_path, DomConstants.DEFAULT_PATH)
        if os.path.exists(xmlConfiguration):
            dom = DomHelper(xmlConfiguration)
            alias = dom.getAlias(sys.argv[1])
            alias.executeCommand()
            os._exit(0)
            
    raise Exception(ExceptionConstants.CONFIG_NOT_FOUND)
    