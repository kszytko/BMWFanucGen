from FileParser import FileParser
from ParameterParser import ParameterParser
from IOParser import IOParser

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

HEADER_IO = '''
PRINT \"#############################\"
PRINT \"#   LOAD IO                 #\"
PRINT \"#############################\"
'''


class ParserSaver(object):
    def __init__(self, file_path: str, make_comments: bool):
        self.file = open(file_path, "w")
        self.make_comments = make_comments

    def printCM(self, text):
        self.file.write(text)
        self.file.write('\n')
        return self

    def writeParam(self, parameter_parser: ParameterParser):
        self.printCM(HEADER_VARIABLE)
        if self.make_comments:
            self.printCM(parameter_parser.getStringWithComments())
        else:
            self.printCM(parameter_parser.getString())
        return self

    def writeFile(self, file_parser: FileParser):
        self.printCM(HEADER_FILES)
        self.printCM("MKDIR FR:GIF")
        self.printCM("SPEP_OFF")
        if self.make_comments:
            self.printCM(file_parser.getStringWithComments())
        else:
            self.printCM(file_parser.getString())
        self.printCM("SPEP_ON")
        return self

    def writeIO(self, io_parser: IOParser):
        self.printCM(HEADER_IO)
        if self.make_comments:
            self.printCM(io_parser.getStringWithComments())
        else:
            self.printCM(io_parser.getString())
        return self

    def clearIO(self):
        self.printCM(HEADER_IO)
        self.printCM("SPEP_OFF")
        self.printCM("DIOASG 1 1 8000 0 0 0 0")
        self.printCM("DIOASG 2 1 8000 0 0 0 0")

        for i in range(20):
            self.printCM("DIOASG 18 " + str(i) + " 0 0 0 0 0")
        for i in range(20):
            self.printCM("DIOASG 19 " + str(i) + " 0 0 0 0 0")
        self.printCM("SPEP_ON")
        return self

    def __del__(self):
        self.file.close()

