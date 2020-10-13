from xml.etree import ElementTree as et

# <ioport portType="20" portNumber="1"  physStart="1"                   comment=""
# physRack="35"  physSlot="1" DescriptionDE="" DescriptionEN="" />
# <ioport portType="19" portNumber="12" physStart="609" numbOfPorts="8" comment="grp_go_Num"
# physRack="100" physSlot="1" DescriptionDE="Handlings Nummer" DescriptionEN="Gripper number" />


class IOParser(object):
    def __init__(self):
        self.ioports = []
        self.formated = []

        self.digital_inputs_configs = []
        self.digital_outputs_configs = []
        self.group_inputs_configs = []
        self.group_outputs_configs = []

    @staticmethod
    def getAttributes(param_node) -> dict:
        attributes_dict = dict(
            port_type=int(param_node.attrib.get('portType', 0)),
            port_number=int(param_node.attrib.get('portNumber', 0)),
            phys_start=int(param_node.attrib.get('physStart', 0)),
            comment=param_node.attrib.get('comment', "None"),
            numb_of_ports=int(param_node.attrib.get('numbOfPorts', 0)),
            phys_rack=int(param_node.attrib.get('physRack', 0)),
            phys_slot=int(param_node.attrib.get('physSlot', 0)),
            description_en=param_node.attrib.get('DescriptionEN', "None")
        )

        return attributes_dict

    def getGroupConfig(self, port):
        port_number = port['port_number']
        numb_of_ports = port['numb_of_ports']
        phys_rack = port['phys_rack']
        phys_slot = port['phys_slot']
        phys_start = port['phys_start']

        return [port_number, numb_of_ports, phys_rack, phys_slot, phys_start]



    def getConfig(self, port):
        port_number = port['port_number']
        phys_rack = port['phys_rack']
        phys_slot = port['phys_slot']
        phys_start = port['phys_start']

        return [port_number, 1, phys_rack, phys_slot, phys_start]

    def hasSameRackAndSlots(self, signal, config):
        if signal[2:4] == config[2:4]:
            return True
        return False

    def isSignalNextValid(self, signal, config):
        start = config[0]
        count = config[1]
        next = start + count

        if signal[0] == next:
            return True
        return False

    def isSignalDuplicate(self, signal, config):
        start = config[0]
        count = config[1]
        end = start + count

        if signal[0] >=  start and signal[0] <= end:
            return True
        return False

    def calculateConfig(self, ports):
        #[port_number, port_number_count, phys_rack, phys_slot, phys_start]
        configs = []
        sorted_ports = sorted(ports, key=lambda x: x[0])
        for port in sorted_ports:
            found = False

            for config in configs:
                if self.hasSameRackAndSlots(port, config):
                    if self.isSignalNextValid(port, config):
                        config[1] += 1
                        found = True
                    elif self.isSignalDuplicate(port, config):
                        found = True

            if not found:
                configs.append(port)

        return configs


    def findAndParse(self, root):
        nodes = root.findall(".//ioport")
        self.ioports = [self.getAttributes(node) for node in nodes]

        digital_inputs = [self.getConfig(port) for port in self.ioports if port['port_type'] == 1]
        digital_outputs = [self.getConfig(port) for port in self.ioports if port['port_type'] == 2]
        group_inputs = [self.getGroupConfig(port) for port in self.ioports if port['port_type'] == 18]
        group_outputs = [self.getGroupConfig(port) for port in self.ioports if port['port_type'] == 19]

        self.digital_inputs_configs = self.calculateConfig(digital_inputs)
        self.digital_outputs_configs = self.calculateConfig(digital_outputs)
        self.group_inputs_configs = group_inputs
        self.group_outputs_configs = group_outputs

        self.format()

    def print(self):
        for ioport in self.ioports:
            str_data = [str(el) for el in list(ioport.values())]
            formated = ' '.join(str_data)
            self.formated.append(formated)

    def join(self, lista):
        return ' '.join(str(x) for x in lista)

    def format(self):
        for el in self.digital_inputs_configs:
            self.formated.append("DIOASG " + self.join([1, el[0], el[1], el[2], el[3], 1, el[4]]))
        for el in self.digital_outputs_configs:
            self.formated.append("DIOASG " + self.join([2, el[0], el[1], el[2], el[3], 2, el[4]]))
        for el in self.group_inputs_configs:
            self.formated.append("DIOASG " + self.join([18, el[0], el[1], el[2], el[3], 1, el[4]]))
        for el in self.group_outputs_configs:
            self.formated.append("DIOASG " + self.join([19, el[0], el[1], el[2], el[3], 2, el[4]]))

    def getString(self):
        return '\n'.join(self.formated) + '\n'

    def getStringWithComments(self):
        output = ""
        for el in self.formated:
            output += "PRINT \"" + el + "\"\n"
            output += el + "\n"
        return output
