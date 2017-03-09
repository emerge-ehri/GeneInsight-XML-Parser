import sys, xml
import ConfigParser
import EmergeXMLParser


if __name__ == "__main__":
    
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    db_connection = Config.get("Database", "Connection")
    
    xml_file = sys.argv[1]

    parser = EmergeXMLParser.XMLParser(db_connection)
    #parser.create_tables(False)
    try:
        parser.parse(xml_file)
    except xml.etree.ElementTree.ParseError as e:
        print "Error. Unable to parse the XML file. It may be malformed."
        print "Error message: " + str(e)
