from FileParser import FileParser
from ParameterParser import ParameterParser
from IOParser import IOParser
from xml.etree import ElementTree as et

HEADER_FILES = '''
PRINT \"#############################\"
PRINT \"#   LOAD FILES              #\"
PRINT \"#############################\"
'''

HEADER_VARIABLE = '''
PRINT \"#############################\"
PRINT \"#   LOAD VARIABLES          #\"
PRINT \"#############################\"
'''

def parseBluePrint(root, fileParser, paramParser):
    application_node = root.find("Application")
    version_node = root.find("Application/Version")
    loadorder_node = root.find("Application/Version/LoadOrder")

    variable_dir = application_node.attrib.get('root')
    version = version_node.attrib.get('value')

    fileParser.findAndParse(loadorder_node)
    paramParser.findAndParse(loadorder_node, variable_dir)

    for node in loadorder_node.findall("External"):
        external = node.attrib.get('name', 'NOT_FOUND')
        paramParser.findAndParse(node, external)

def parseSASXML(root, paramParser, ioParser):
    for application_node in root.findall("Application"):
        variable_dir = application_node.attrib.get('name') + "_VAR"

        paramParser.findAndParse(application_node, variable_dir)

        ioDevice_node = application_node.find("IO_Setup/Profinet/Device")
        ioParser.findAndParse(ioDevice_node)


class CMFile(object):
    def __init__(self, path):
        self.file = open(path, "w")

    def printCM(self, text):
        self.file.write(text)
        self.file.write('\n')

    def makeParameter(self, parameterParser):
        self.printCM(HEADER_VARIABLE)
        self.printCM(parameterParser.getString())
        #self.printCM(parameterParser.getStringWithComments())

    def makeFile(self, fileParser):
        self.printCM(HEADER_FILES)
        self.printCM("MKDIR FR:GIF")
        self.printCM("SPEP_OFF")
        self.printCM(fileParser.getString())
        #self.printCM(fileParser.getStringWithComments())
        self.printCM("SPEP_ON")

    def makeIO(self, ioParser):
        self.printCM("IO")
        self.printCM(ioParser.getString())
        #self.printCM(ioParser.getStringWithComments())

    def make(self, parameterParser = None, ioParser = None, fileParser = None):
        if fileParser:
            self.makeFile(fileParser)
        if parameterParser:
            self.makeParameter(parameterParser)
        if ioParser:
            self.makeIO(ioParser)

    def __del__(self):
        self.file.close()

def parseA01():
    root = et.parse('A01.xml').getroot()
    fileParser = FileParser()
    paramParser = ParameterParser()

    parseBluePrint(root, fileParser, paramParser)
    CMFile('D:\output.cm').make(paramParser, None, fileParser)

def parseSAS():
    root = et.parse('ST010_IR001.xml').getroot()
    paramParser = ParameterParser()
    ioParser = IOParser()

    parseSASXML(root, paramParser, ioParser)
    CMFile('D:\sas.cm').make(paramParser, ioParser)


if __name__ == '__main__':
    #parseA01()
    parseSAS()
