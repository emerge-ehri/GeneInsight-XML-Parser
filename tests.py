import unittest, sys, os, pyodbc, datetime, sqlalchemy, xml
from sqlalchemy.orm import sessionmaker
import Reports, EmergeXMLParser

SQLite_test_DB = 'test_files/temp.db'
db_connection  = 'sqlite:///' + SQLite_test_DB


class TestCreateTables(unittest.TestCase):
    def setUp(self):
        self.xml_file = 'test_files/sample_report.xml'
        # delete the database
        if os.path.exists(SQLite_test_DB): os.remove(SQLite_test_DB)
        # create the parser for testing
        self.parser = EmergeXMLParser.XMLParser(db_connection)
        # create our own engine for test queries
        self.engine = sqlalchemy.create_engine(db_connection)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    # drop any existing tables before creating new, empty tables
    def test_drop_before_create(self):
        # drop the tables, then create them
        self.parser.create_tables(True)

        # queries to the tables should produce no rows since the tables were dropped before created
        rows = self.session.query(Reports.Report).count()
        self.assertEqual(rows , 0)
        rows = self.session.query(Reports.InterpretedDiseases).count()
        self.assertEqual(rows , 0)
    
    # try to create tables even if they already exist
    def test_create_without_drop(self):
        # Drop and Create new tables
        self.parser.create_tables(True)
        
        # Add some rows to the tables
        self.parser.parse(self.xml_file)
        
        # Create the tables again, but without dropping them first 
        self.parser.create_tables(False)
        
        # since the table already exist, and they weren't dropped, the rows should still be there
        rows = self.session.query(Reports.Report).count()
        self.assertEqual(rows , 1)
        rows = self.session.query(Reports.InterpretedDiseases).count()
        self.assertEqual(rows , 2)


# Test if parsing works even if the tables didn't exist
class TestNoTables(unittest.TestCase):
    def setUp(self):
        self.xml_file = 'test_files/sample_report.xml'
        # delete the database
        if os.path.exists(SQLite_test_DB): os.remove(SQLite_test_DB)
        # create the parser for testing
        self.parser = EmergeXMLParser.XMLParser(db_connection)
        # create our own engine for test queries
        self.engine = sqlalchemy.create_engine(db_connection)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
            
    def test_insert_before_tables_created(self):
        # try to parse xml before tables have been created
        # the tables should automatically be created if they didn't exist
        self.parser.parse(self.xml_file)
        self.assertTrue(Reports.Report.__table__.exists(bind=self.engine))
        
    def test_insert_if_a_table_is_missing(self):
        # drop and create new tables
        self.parser.create_tables(True)
        # drop one of the tables
        Reports.InterpretedDiseases.__table__.drop(bind=self.engine)
        self.assertFalse(Reports.InterpretedDiseases.__table__.exists(bind=self.engine))
        # try to parse xml even though a table has been dropped
        self.parser.parse(self.xml_file)
        # check to see if the table has been re-created
        self.assertTrue(Reports.InterpretedDiseases.__table__.exists(bind=self.engine))


class TestMissingValuesInXMLFile(unittest.TestCase):
    def setUp(self):
        self.xml_file = 'test_files/sample_report.xml'
        # delete the database
        if os.path.exists(SQLite_test_DB): os.remove(SQLite_test_DB)
        # create the parser for testing
        self.parser = EmergeXMLParser.XMLParser(db_connection)
        # create our own engine for test queries
        self.engine = sqlalchemy.create_engine(db_connection)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def test_something(self):
        pass



class TestMultipleChildren(unittest.TestCase):
    def setUp(self):
        self.xml_file = 'test_files/sample_report.xml'
        # delete the database
        if os.path.exists(SQLite_test_DB): os.remove(SQLite_test_DB)
        # create the parser for testing
        self.parser = EmergeXMLParser.XMLParser(db_connection)
        # create our own engine for test queries
        self.engine = sqlalchemy.create_engine(db_connection)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    def test_the_tables_can_have_multiple_children:
        

# this is probably a dumb test since I'm really just testing the xml module
# but, hey, it helped me figure out xml parse errors
class TestMalformedXML(unittest.TestCase):
    def setUp(self):
        self.xml_file = 'test_files/malformed.xml'
        # delete the database
        if os.path.exists(SQLite_test_DB): os.remove(SQLite_test_DB)
        # create the parser for testing
        self.parser = EmergeXMLParser.XMLParser(db_connection)
        
    def test_malformed(self):
        with self.assertRaises(xml.etree.ElementTree.ParseError):
            self.parser.parse(self.xml_file)


        
    

if __name__ == '__main__':
    unittest.main()
    
    
    
    
    

#         with self.assertRaises(TypeError):

 
        