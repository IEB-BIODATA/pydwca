import unittest

from lxml import etree as et

from eml.resources.distribution import EMLOnline
from eml.types import EMLTextType
from test_xml.test_xml import TestXML


class TestOnline(TestXML):
    DEFAULT_TAGS = {
        "{http://www.w3.org/XML/1998/namespace}lang": "eng",
        "scope": "document",
        "function": "download",
    }

    def test_parse_invalid(self):
        text_xml = """
<online>
    <onlineDescription>An invalid example</onlineDescription>
    <url function="download">http://data.org/getdata?id=98332</url>
    <connection>
        <references>1</references>
    </connection>
    <connectionDefinition>
        <references>1</references>
    </connectionDefinition>
</online>
        """
        self.assertRaises(
            ValueError,
            EMLOnline.from_string,
            text_xml
        )

    def test_parse_invalid_two_connection(self):
        text_xml = """
<online>
    <onlineDescription>An invalid example</onlineDescription>
    <connection>
        <references>1</references>
    </connection>
    <connectionDefinition>
        <references>1</references>
    </connectionDefinition>
</online>
        """
        self.assertRaises(
            ValueError,
            EMLOnline.from_string,
            text_xml
        )

    def test_parse_url(self):
        text_xml = """
<online>
    <url>http://data.org/getdata?id=98332</url>
</online>
        """
        online = EMLOnline.from_string(text_xml)
        self.assertIsNone(online.online_description, "Online description from nowhere")
        self.assertEqual("http://data.org/getdata?id=98332", online.url, "Error on parse url")
        self.assertEqual(EMLOnline.FunctionType.DOWNLOAD, online.url_function, "Error on parse url function")
        self.assertIsNone(online.connection, "Connection from nowhere")
        self.assertIsNone(online.connection_definition, "Connection definition from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), online.to_element(), "Error on to element")

    def test_parse_url_with_function(self):
        text_xml = """
<online>
    <onlineDescription>An example with url</onlineDescription>
    <url function="information">http://data.org/getdata?id=98332</url>
</online>
        """
        online = EMLOnline.from_string(text_xml)
        self.assertEqual("http://data.org/getdata?id=98332", online.url, "Error on parse url")
        self.assertEqual(EMLOnline.FunctionType.INFORMATION, online.url_function, "Error on parse url function")
        self.assertIsNone(online.connection, "Connection from nowhere")
        self.assertIsNone(online.connection_definition, "Connection definition from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), online.to_element(), "Error on to element")

    def test_parse_connection_referencing(self):
        text_xml = """
<online>
    <onlineDescription>An connection example</onlineDescription>
    <connection>
        <references>1</references>
    </connection>
</online>
        """
        online = EMLOnline.from_string(text_xml)
        self.assertIsNone(online.url, "URL from nowhere")
        self.assertEqual(
            EMLOnline.Connection(
                _id="1",
                referencing=True,
            ),
            online.connection,
            "Connection wrong parse"
        )
        self.assertIsNone(online.connection_definition, "Connection definition from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), online.to_element(), "Error on to element")

    def test_parse_connection_conn_definition(self):
        text_xml = """
<online>
    <onlineDescription>An connection example</onlineDescription>
    <connection>
        <connectionDefinition>
            <references>1</references>
        </connectionDefinition>
    </connection>
</online>
        """
        online = EMLOnline.from_string(text_xml)
        self.assertIsNone(online.url, "URL from nowhere")
        self.assertEqual(
            EMLOnline.ConnectionDefinition(
                _id="1",
                referencing=True,
            ),
            online.connection.connection_definition,
            "Connection wrong parse"
        )
        self.assertIsNone(online.connection_definition, "Connection definition from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), online.to_element(), "Error on to element")

    def test_parse_connection_parameters(self):
        text_xml = """
<online>
    <onlineDescription>An connection example</onlineDescription>
    <connection>
        <parameter>
            <name>hostname</name>
            <value>nceas.ucsb.edu</value>
        </parameter>
        <parameter>
            <name>port</name>
            <value>1234</value>
        </parameter>
    </connection>
</online>
        """
        online = EMLOnline.from_string(text_xml)
        self.assertIsNone(online.url, "URL from nowhere")
        self.assertEqual(
            2,
            len(online.connection.parameters),
            "Connection wrong parse"
        )
        self.assertEqual(
            ("hostname", "nceas.ucsb.edu"),
            online.connection.parameters[0],
            "Connection first parameter wrong parse"
        )
        self.assertEqual(
            ("port", "1234"),
            online.connection.parameters[1],
            "Connection second parameter wrong parse"
        )
        self.assertIsNone(online.connection_definition, "Connection definition from nowhere")
        self.assertEqualTree(et.fromstring(text_xml), online.to_element(), "Error on to element")

    def test_parse_connection_definition_scheme(self):
        text_xml = """
<online>
    <onlineDescription>Connection definition example</onlineDescription>
    <connectionDefinition>
        <schemeName system="http://knb.ecoinformatics.org/knb/">metacat</schemeName>
    </connectionDefinition>
</online>
        """
        online = EMLOnline.from_string(text_xml)
        self.assertIsNone(online.url, "URL from nowhere")
        self.assertIsNone(online.connection, "Connection from nowhere")
        self.assertEqual(
            "metacat",
            online.connection_definition.scheme_name,
            "Connection definition incorrect parse"
        )
        self.assertEqual(
            "http://knb.ecoinformatics.org/knb/",
            online.connection_definition.scheme_name.system,
            "Connection definition incorrect parse system"
        )
        self.assertEqualTree(et.fromstring(text_xml), online.to_element(), "Error on to element")

    def test_parse_connection_definition_description(self):
        description = ('The metacat application protocol. Applications '
                       'must first log into metacat by sending an HTTP '
                       'POST request in http-url-encoded format with the '
                       'parameters action, username, and password. Action '
                       'must be set to "login". If authentication is '
                       'successful, the metacat server will respond with '
                       'a session cookie. All future requests should '
                       'include the session cookie in the HTTP header. '
                       'To retrieve an object, the client then would send '
                       'an HTTP POST in http-url-encoded format, with an '
                       'action parameter set to "get" and the docid '
                       'parameter set to the identifier for the desired '
                       'object.  The response will either be an XML '
                       'document or a multipart-form-encoded response '
                       'containing data.')
        text_xml = f"""
<online>
    <onlineDescription>Connection definition example</onlineDescription>
    <connectionDefinition>
        <description>
            <para>{description}</para>
        </description>
    </connectionDefinition>
</online>
        """
        online = EMLOnline.from_string(text_xml)
        self.assertIsNone(online.url, "URL from nowhere")
        self.assertIsNone(online.connection, "Connection from nowhere")
        self.assertEqual(
            EMLTextType(paragraphs=[description]),
            online.connection_definition.description,
            "Connection definition incorrect parse"
        )
        self.assertEqualTree(et.fromstring(text_xml), online.to_element(), "Error on to element")

    def test_parse_connection_definition_parameter(self):
        definition = ('The fully qualified name of the internet host that '
                      'is providing the metacat service, as would be '
                      'returned by a Domain Name System (DNS) query.')
        text_xml = f"""
<online>
    <onlineDescription>Connection definition example</onlineDescription>
    <connectionDefinition>
        <parameterDefinition>
            <name>hostname</name>
            <definition>{definition}</definition>
            <defaultValue>metacat.nceas.ucsb.edu</defaultValue>
        </parameterDefinition>
    </connectionDefinition>
</online>
        """
        online = EMLOnline.from_string(text_xml)
        self.assertIsNone(online.url, "URL from nowhere")
        self.assertIsNone(online.connection, "Connection from nowhere")
        self.assertEqual(
            EMLOnline.ParameterDefinition(
                name="hostname",
                definition=definition,
                default_value="metacat.nceas.ucsb.edu",
            ),
            online.connection_definition.parameters[0],
            "Connection definition incorrect parse"
        )
        self.assertEqualTree(et.fromstring(text_xml), online.to_element(), "Error on to element")

    def test_parameter_definition_operations(self):
        definition = ('The fully qualified name of the internet host that '
                      'is providing the metacat service, as would be '
                      'returned by a Domain Name System (DNS) query.')
        param1 = EMLOnline.ParameterDefinition(
            name="hostname",
            definition=definition
        )
        param2 = EMLOnline.ParameterDefinition(
            name="port",
            definition="The port in which to connect."
        )
        self.assertNotEqual(param1, param2, "Different parameter equal")
        self.assertNotEqual(3, param2, "Different types equal")
        self.assertRaises(
            TypeError, param2.__gt__, 4
        )
        self.assertGreaterEqual(param2, param1, "hostname > port")
        self.assertRaises(
            TypeError, param2.__lt__, 4
        )
        self.assertLessEqual(param1, param2, "port < hostname")

    def test_conn_definition_equal(self):
        conn_def_1 = EMLOnline.ConnectionDefinition(_id="1", referencing=True)
        conn_def_2 = EMLOnline.ConnectionDefinition(_id="1", referencing=True)
        self.assertEqual(conn_def_1, conn_def_2, "Equal elements not equal")
        self.assertNotEqual(4, conn_def_2, "Different types equal")

    def test_conn_equal(self):
        conn_1 = EMLOnline.Connection(_id="1", referencing=True)
        conn_2 = EMLOnline.Connection(_id="1", referencing=True)
        self.assertEqual(conn_1, conn_2, "Equal elements not equal")
        self.assertNotEqual(4, conn_2, "Different types equal")

    def test_parse_none(self):
        self.assertIsNone(EMLOnline.parse(None, {}), "EML Online from nowhere")


if __name__ == '__main__':
    unittest.main()
