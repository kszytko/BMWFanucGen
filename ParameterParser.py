class ParameterParser(object):
    def __init__(self, root=None, external=None):
        self.variables = []
        self.formated = []

        if root and dir:
            self.findAndParse(root, external)

    def getAttributes(self, param_node):
        param_name = param_node.attrib.get('name', "None")
        param_type = param_node.attrib.get('type', "None")
        param_value = param_node.attrib.get('value')

        return [param_name, param_type, param_value]

    def parseNode(self, node, path=""):
        [name, typ, value] = self.getAttributes(node)

        if node.tag == 'Member':
            path += '[' + name + ']'
        elif node.tag == 'Parameter':
            if path != "":
                path += '.'
            path += name

        for child in node:
            self.parseNode(child, path)

        if value is None:
            return

        self.variables.append([path, typ, value])

    def formatSystemVariable(self, variable):
        [path, typ, value] = variable

        if typ in ["STRING"]:
            value = '"' + value + '"'
        elif typ == "BOOLEAN":
            if value.lower() == "true":
                value = "1"
            else:
                value = "0"

        self.formated.append("SETVAR " + path + " " + value)

    def formatExternalVariable(self, variable, external):
        [path, typ, value] = variable

        if typ in ["REAL", "STRING"]:
            value = '\'' + value + '\''

        self.formated.append("KCL SET VARIABLE [" + external + "] " + path + " = " + value)

    def findAndParse(self, root, external):
        nodes = root.findall("Parameter")
        for node in nodes:
            self.parseNode(node)
        self.format(external)

    def format(self, external):
        if external == "[*SYSTEM*]":
            for variable in self.variables:
                self.formatSystemVariable(variable)
        else:
            for variable in self.variables:
                self.formatExternalVariable(variable, external)

        self.variables.clear()

    def getString(self):
        return '\n'.join(self.formated) + '\n'

    def getStringWithComments(self):
        output = ""
        for el in self.formated:
            output += "PRINT \"" + el + "\"\n"
            output += el + "\n"
        return output