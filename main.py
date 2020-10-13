from FileParser import FileParser
from ParameterParser import ParameterParser
from IOParser import IOParser

from ParserSaver import ParserSaver

from xml.etree import ElementTree as et


def parseBluePrint(root, file_parser, param_parser):
    application_node = root.find("Application")
    version_node = root.find("Application/Version")
    loadorder_node = root.find("Application/Version/LoadOrder")

    variable_dir = application_node.attrib.get('root')
    version = version_node.attrib.get('value')

    file_parser.findAndParse(loadorder_node)
    param_parser.findAndParse(loadorder_node, variable_dir)

    for node in loadorder_node.findall("External"):
        external = node.attrib.get('name', 'NOT_FOUND')
        param_parser.findAndParse(node, external)


def parseSAS(root, param_parser, io_parser):
    for application_node in root.findall("Application"):
        variable_dir = application_node.attrib.get('name') + "_VAR"

        param_parser.findAndParse(application_node, variable_dir)

    io_parser.findAndParse(root)


def openAndParseBluePrint():
    root = et.parse('A01.xml').getroot()
    file_parser = FileParser()
    param_parser = ParameterParser()

    parseBluePrint(root, file_parser, param_parser)

    ParserSaver("D:\output.cm", False).writeFile(file_parser).writeParam(param_parser)


def openAndParseSAS():
    root = et.parse('ST010_IR001.xml').getroot()
    param_parser = ParameterParser()
    io_parser = IOParser()

    parseSAS(root, param_parser, io_parser)
    ParserSaver("D:\sas.cm", True).clearIO().writeParam(param_parser).writeIO(io_parser)




if __name__ == '__main__':
    #openAndParseBluePrint()
    openAndParseSAS()
    pass
