from xml.etree import ElementTree as et


class IOParser(object):
    def getAttributes(self, param_node):
        #<ioport portType="20" portNumber="1" physStart="1" comment="" physRack="35" physSlot="1" DescriptionDE="" DescriptionEN="" />
        portType        = param_node.attrib.get('portType', 0)
        portNumber      = param_node.attrib.get('portNumber', 0)
        physStart       = param_node.attrib.get('physStart', 0)
        comment         = param_node.attrib.get('comment', 0)
        physRack        = param_node.attrib.get('physRack', 0)
        physSlot        = param_node.attrib.get('physSlot', 0)
        DescriptionEN   = param_node.attrib.get('DescriptionEN', 0)

        return [portType, portNumber, physStart, comment, physRack, physSlot, DescriptionEN]

    def parseNode(self, node):
        [file_path, location, file_name] = self.getAttributes(node)
        pass

    def findAndParse(self, root):
        digital_node = root.find("Digital")
        group_node = root.find("Group")

        for node in digital_node.find("IN"):
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