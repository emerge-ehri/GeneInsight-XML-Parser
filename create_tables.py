import sys
import ConfigParser
import EmergeXMLParser

# usage python create_tables.py [drop]
# Use drop to remove tables before recreating them so all data is removed

if __name__ == "__main__":
    
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    db_connection = Config.get("Database", "Connection")
    
    drop_first = False
    if (len(sys.argv) > 1 and sys.argv[1] == 'drop'):
        drop_first = True
    

    parser = EmergeXMLParser.XMLParser(db_connection)
    parser.create_tables(drop_first)
