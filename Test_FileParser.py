import unittest
from FileParser import FileParser
from ParameterParser import ParameterParser

from xml.etree import ElementTree as et

class FileParamTest(unittest.TestCase):
    def assertParameters(self, input, output):
        root = et.fromstring(input)
        fp = FileParser()
        fp.parseNode(root)
        fp.format()
        self.assertEqual(fp.getString(), output)

    def test_basic_file_xml_is_parse_valid(self):
        input = "<File name = \"fileTest.vr\" location = \"MD:\" comment = \"test\" type = \"VARIABLE\"/>"
        output = "COPY fileTest.vr MD:fileTest.vr\n"
        self.assertParameters(input, output)

    def test_file_name_in_some_directory_is_parse_valid(self):
        input = "<File name = \"A01\\fileTest.vr\" location = \"MD:\" comment = \"test\" type = \"VARIABLE\"/>"
        output = "COPY A01\\fileTest.vr MD:fileTest.vr\n"
        self.assertParameters(input, output)

    def test_location_Frsu_moved_first_from_FR(self):
        input = "<File name = \"A01\\fileTest.vr\" location = \"FRSU:\" comment = \"test\" type = \"VARIABLE\"/>"
        output = "COPY A01\\fileTest.vr FR:fileTest.vr\nFRCOPY FR:fileTest.vr FRSU:fileTest.vr\n"
        self.assertParameters(input, output)


class VariableSystemParamTest(unittest.TestCase):
    def setUp(self):
        self.EXT_SYSTEM = "[*SYSTEM*]"
        self.EXT_LOCAL = "TEST"

    def assertParameters(self, input, output, external):
        root = et.fromstring(input)
        pp = ParameterParser()
        pp.parseNode(root)
        pp.format(external)
        input = pp.getString()
        self.assertEqual(input, output)

    def test_system_oneline_parameter_shour_return_valid_setvar(self):
        input = "<Parameter name = \"$PARAMETER_ONELINE\" type = \"STRING\" value = \"TEST\"/>"
        output = "SETVAR $PARAMETER_ONELINE \"TEST\"\n"
        self.assertParameters(input, output, self.EXT_SYSTEM)

    def test_system_oneline_parameter_shour_return_int_value_from_boolean(self):
        input1 = "<Parameter name = \"$PARAMETER_BOOLEAN\" type = \"BOOLEAN\" value = \"FALSE\"/>"
        input2 = "<Parameter name = \"$PARAMETER_BOOLEAN\" type = \"BOOLEAN\" value = \"TRUE\"/>"
        output1 = "SETVAR $PARAMETER_BOOLEAN 0\n"
        output2 = "SETVAR $PARAMETER_BOOLEAN 1\n"

        self.assertParameters(input1, output1, self.EXT_SYSTEM)
        self.assertParameters(input2, output2, self.EXT_SYSTEM)

class VariableExternalParamTest(unittest.TestCase):
    def setUp(self):
        self.EXT_SYSTEM = "[*SYSTEM*]"
        self.EXT_LOCAL = "TEST"

    def assertParameters(self, input, output, external):
        root = et.fromstring(input)
        pp = ParameterParser()
        pp.parseNode(root)
        pp.format(self.EXT_LOCAL)
        self.assertEqual(pp.getString(), output)

    def test_local_oneline_parameter_shour_return_valid_setvar(self):
        input = "<Parameter name = \"$PARAMETER_ONELINE\" type = \"STRING\" value = \"TEST\"/>"
        output = "KCL SET VARIABLE [TEST] $PARAMETER_ONELINE = 'TEST'\n"
        self.assertParameters(input, output, self.EXT_LOCAL)

    def test_local_oneline_parameter_shour_return_bool_value_from_boolean(self):
        input1 = "<Parameter name = \"$PARAMETER_BOOLEAN\" type = \"BOOLEAN\" value = \"FALSE\"/>"
        input2 = "<Parameter name = \"$PARAMETER_BOOLEAN\" type = \"BOOLEAN\" value = \"TRUE\"/>"
        output1 = "KCL SET VARIABLE [TEST] $PARAMETER_BOOLEAN = FALSE\n"
        output2 = "KCL SET VARIABLE [TEST] $PARAMETER_BOOLEAN = TRUE\n"

        self.assertParameters(input1, output1, self.EXT_LOCAL)
        self.assertParameters(input2, output2, self.EXT_LOCAL)


class ParametersFinderTestCase(unittest.TestCase):
    def setUp(self):
        self.EXT_SYSTEM = "[*SYSTEM*]"
        self.EXT_LOCAL = "TEST"

    def assertParameters(self, input, output, external):
        root = et.fromstring(input)
        pp = ParameterParser()
        pp.findAndParse(root, external)
        self.assertEqual(pp.getString(), output)

    def test_find_parameters_node_in_level_0(self):
        input = ''' <LoadOrder>
                        <Parameter name = "$A" type = "INTEGER" value = "1"/>
                    </LoadOrder>'''

        output = "KCL SET VARIABLE [TEST] $A = 1\n"

        self.assertParameters(input, output, "TEST")

    def test_find_parameters_node_level_1(self):
        input = ''' <LoadOrder>
                        <Parameter name = "$B">
                            <Parameter name = "$BB" type = "INTEGER" value = "1"/>
                        </Parameter>
                    </LoadOrder>'''

        output = "KCL SET VARIABLE [TEST] $B.$BB = 1\n"

        self.assertParameters(input, output, "TEST")

    def test_find_parameters_node_level_2(self):
        input = ''' <LoadOrder>
                        <Parameter name = "$C" type = "ARRAY OF STRING">
                            <Member name = "1" type = "STRING" value = "CC1"/>
                            <Member name = "2" type = "STRING" value = "CC2"/>
                        </Parameter>
                    </LoadOrder>'''

        output = '''KCL SET VARIABLE [TEST] $C[1] = 'CC1'\nKCL SET VARIABLE [TEST] $C[2] = 'CC2'\n'''

        self.assertParameters(input, output, "TEST")

    def test_find_parameters_node_level_3(self):
        input = ''' <LoadOrder>
                        <Parameter name = "$D" type = "ARRAY OF STRUCTURE">
                            <Member name = "1">
                                <Parameter name = "$F" type = "STRING" value = "FF"/>
                            </Member>
                            <Member name = "2">
                                <Parameter name = "$G" type = "STRING" value = "GG"/>
                            </Member>
                        </Parameter>
                    </LoadOrder>'''

        output = '''KCL SET VARIABLE [TEST] $D[1].$F = 'FF'\nKCL SET VARIABLE [TEST] $D[2].$G = 'GG'\n'''

        self.assertParameters(input, output, "TEST")

    def test_find_parameters_node_level_4(self):
        input = ''' <LoadOrder>
                        <Parameter name = "$E" type = "ARRAY OF STRUCTURE">
                            <Member name = "1">
                                <Parameter name = "$F" type = "ARRAY OF REAL">
                                    <Member name = "1" type = "REAL" value = "1"/>
                                    <Member name = "2" type = "REAL" value = "1"/>
                                </Parameter>
                            </Member>
                        </Parameter>
                    </LoadOrder>'''

        output = '''KCL SET VARIABLE [TEST] $E[1].$F[1] = '1'\nKCL SET VARIABLE [TEST] $E[1].$F[2] = '1'\n'''

        self.assertParameters(input, output, "TEST")



if __name__ == '__main__':
    unittest.main()
