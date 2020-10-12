class FileParser(object):
    def __init__(self):
        self.commands = []
        self.formated = []

    def getFileName(self, name):
        pos = name.rfind('\\')
        return name[pos + 1:]

    def getAttributes(self, param_node):
        file_path = param_node.attrib.get('name', "None")
        location = param_node.attrib.get('location', "None")
        file_name = self.getFileName(file_path)

        return [file_path, location, file_name]

    def parseNode(self, node):
        [file_path, location, file_name] = self.getAttributes(node)

        output_file = location + file_name

        if location == "FRSU:":
            temp_file = "FR:" + file_name
            self.commands.append(["COPY", file_path, temp_file])
            self.commands.append(["FRCOPY", temp_file, output_file])
        else:
            self.commands.append(["COPY", file_path, output_file])

    def findAndParse(self, root):
        nodes = root.findall("File")
        for node in nodes:
            self.parseNode(node)
        self.format()

    def format(self):
        for el in self.commands:
            self.formated.append(' '.join(el))

    def getString(self):
        return '\n'.join(self.formated) + '\n'

    def getStringWithComments(self):
        output = ""
        for el in self.formated:
            output += "PRINT \"" + el + "\"\n"
            output += el + "\n"
        return output
