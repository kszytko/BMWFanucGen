import unittest
from IOParser import IOParser
from xml.etree import ElementTree as et

class ConfigTestCase(unittest.TestCase):
    def assertConfig(self, input, output):
        #[port_number, phys_rack, phys_slot, phys_start]
        io = IOParser()
        configs = io.calculateConfig(input)
        self.assertEqual(configs, output)

    def test_config_is_calculate_valid_config_for_diff_rack(self):
        input = [
            [1, 1, 100, 1, 1],
            [2, 1, 100, 1, 1],
            [3, 1, 100, 1, 1],
            [4, 1, 99, 1, 1],
            [5, 1, 99, 1, 1],
            [6, 1, 99, 1, 1]]

        output = [
            [1, 3, 100, 1, 1],
            [4, 3, 99, 1, 1] ]

        self.assertConfig(input, output)


    def test_config_is_calculate_valid_config_for_diff_slot(self):
        input = [
            [1, 1, 100, 1, 1],
            [2, 1, 100, 1, 1],
            [3, 1, 100, 1, 1],
            [4, 1, 100, 2, 1],
            [5, 1, 100, 2, 1],
            [6, 1, 100, 2, 1]]

        output = [
            [1, 3, 100, 1, 1],
            [4, 3, 100, 2, 1]]

        self.assertConfig(input, output)

    def test_config_is_calculate_valid_config_for_mixed_data(self):
        input = [
            [1, 1, 100, 1, 1],
            [3, 1, 100, 1, 1],
            [2, 1, 100, 1, 1],
            [4, 1, 100, 1, 1],
            [6, 1, 100, 1, 1],
            [5, 1, 100, 1, 1]]

        output = [
            [1, 6, 100, 1, 1]]

        self.assertConfig(input, output)

    def test_config_is_calculate_valid_config_for_insert(self):
        input = [
            [1, 1, 100, 1, 1],
            [2, 1, 100, 1, 1],

            [5, 1, 100, 1, 1],
            [6, 1, 100, 1, 1],

            [3, 1, 99, 1, 1],
            [4, 1, 99, 1, 1]]

        output = [
            [1, 2, 100, 1, 1],
            [3, 2, 99, 1, 1],
            [5, 2, 100, 1, 1]
            ]

        self.assertConfig(input, output)

    def test_config_is_calculate_valid_config_for_mixed_insert(self):
        input = [
            [1, 1, 100, 1, 1],
            [2, 1, 100, 1, 1],

            [5, 1, 99, 1, 1],
            [6, 1, 99, 1, 1],

            [3, 1, 100, 1, 1],
            [4, 1, 100, 1, 1]]

        output = [
            [1, 4, 100, 1, 1],
            [5, 2, 99, 1, 1]]

        self.assertConfig(input, output)

    def test_config_is_calculate_valid_config_for_duplicates(self):
        input = [
            [1, 1, 100, 1, 1],
            [2, 1, 100, 1, 1],

            [1, 1, 100, 1, 1],
            [2, 1, 100, 1, 1],

            [3, 1, 100, 1, 1],
            [4, 1, 100, 1, 1]]

        output = [
            [1, 4, 100, 1, 1]]

        self.assertConfig(input, output)

class ConfigTestCaseXML(unittest.TestCase):
    def assertConfig(self, input, output):
        root = et.fromstring(input)
        io = IOParser()
        io.findAndParse(root)
        self.assertEqual(io.getString(), output)

    def test_parsing_port_digital_is_valid(self):
        input = '''
        <IN>
              <ioport portType="1" portNumber="1" physStart="1" comment="PLC_di_01" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 01" DescriptionEN="PLC user input 01" />
              <ioport portType="1" portNumber="2" physStart="2" comment="PLC_di_02" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 02" DescriptionEN="PLC user input 02" />
              <ioport portType="1" portNumber="3" physStart="3" comment="PLC_di_03" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 03" DescriptionEN="PLC user input 03" />
              <ioport portType="1" portNumber="4" physStart="4" comment="PLC_di_04" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 04" DescriptionEN="PLC user input 04" />
              <ioport portType="1" portNumber="5" physStart="5" comment="PLC_di_05" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 05" DescriptionEN="PLC user input 05" />
              <ioport portType="1" portNumber="6" physStart="6" comment="PLC_di_06" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 06" DescriptionEN="PLC user input 06" />
              <ioport portType="1" portNumber="7" physStart="7" comment="PLC_di_07" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 07" DescriptionEN="PLC user input 07" />
              <ioport portType="1" portNumber="8" physStart="8" comment="PLC_di_08" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 08" DescriptionEN="PLC user input 08" />
              <ioport portType="1" portNumber="9" physStart="9" comment="PLC_di_09" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 09" DescriptionEN="PLC user input 09" />
              <ioport portType="1" portNumber="10" physStart="10" comment="PLC_di_10" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 10" DescriptionEN="PLC user input 10" />
        </IN>
'''

        output = "DIOASG 1 1 10 100 1 1 1\n"
        self.assertConfig(input, output)

    def test_parsing_port_digital_IO_is_valid(self):
        input = '''
        <TESt>
              <ioport portType="1" portNumber="1" physStart="1" comment="PLC_di_01" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 01" DescriptionEN="PLC user input 01" />
              <ioport portType="1" portNumber="2" physStart="2" comment="PLC_di_02" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 02" DescriptionEN="PLC user input 02" />
              <ioport portType="1" portNumber="3" physStart="3" comment="PLC_di_03" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 03" DescriptionEN="PLC user input 03" />
              <ioport portType="1" portNumber="4" physStart="4" comment="PLC_di_04" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 04" DescriptionEN="PLC user input 04" />
              <ioport portType="1" portNumber="5" physStart="5" comment="PLC_di_05" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 05" DescriptionEN="PLC user input 05" />
              <ioport portType="2" portNumber="6" physStart="6" comment="PLC_di_06" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 06" DescriptionEN="PLC user input 06" />
              <ioport portType="2" portNumber="7" physStart="7" comment="PLC_di_07" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 07" DescriptionEN="PLC user input 07" />
              <ioport portType="2" portNumber="8" physStart="8" comment="PLC_di_08" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 08" DescriptionEN="PLC user input 08" />
              <ioport portType="2" portNumber="9" physStart="9" comment="PLC_di_09" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 09" DescriptionEN="PLC user input 09" />
              <ioport portType="2" portNumber="10" physStart="10" comment="PLC_di_10" physRack="100" physSlot="1" DescriptionDE="SPS Anwender Eingang 10" DescriptionEN="PLC user input 10" />
        </TESt>
'''

        output = "DIOASG 1 1 5 100 1 1 1\nDIOASG 2 6 5 100 1 2 6\n"
        self.assertConfig(input, output)

    def test_parsing_port_group_IN_valid(self):
        input = '''
           <TESt>
              <ioport portType="18" portNumber="1" physStart="65" numbOfPorts="8" comment="PLC_gi_UserNum" physRack="100" physSlot="9"/>
              <ioport portType="18" portNumber="2" physStart="73" numbOfPorts="8" comment="PLC_gi_TypeNum" physRack="100" physSlot="9" />
         </TESt>
'''

        output = "DIOASG 18 1 8 100 9 1 65\nDIOASG 18 2 8 100 9 1 73\n"
        self.assertConfig(input, output)

    def test_parsing_port_group_OUT_valid(self):
        input = '''
           <TESt>
                <ioport portType="19" portNumber="1" physStart="65" numbOfPorts="8" comment="PLC_go_UserNum" physRack="100" physSlot="9" />
                <ioport portType="19" portNumber="2" physStart="73" numbOfPorts="8" comment="PLC_go_TypeNum" physRack="100" physSlot="9" />
            </TESt>
'''

        output = "DIOASG 19 1 8 100 9 2 65\nDIOASG 19 2 8 100 9 2 73\n"
        self.assertConfig(input, output)


if __name__ == '__main__':
    unittest.main()
