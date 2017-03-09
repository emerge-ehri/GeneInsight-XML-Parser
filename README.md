# GeneInsight XML Parser for eMerge Network

This code parses the genetic return of results XML report from GeneInsight
into a relational database.

The XML file is parsed into 8 tables.  The *Report* table is the main table
and represents the root of the XML file. The other 7 tables represent nodes that can have one or more children in the XML file.  


### Tables:

* Report
* InterpretedDiseases
* PatientDiseases
* ReportAssays
* ReportVariants
* NestedVariants
* Specimens
* Physicians


### Instructions:

 
* Modify `config_example.ini` to include your database connection.
  This value will include the server name, database, your username, 
  and password.  Go to this site for more information on  
  [configuring sqlalchemy](http://docs.sqlalchemy.org/en/latest/core/engines.html)
  for MSSQL, MySQL, Postgres, etc.
* Rename config_example.ini to config.ini
* Run this command to parse the file and insert it into you database:<br> 
  `python parse_xml_file.py report.xml`

The tables will be created automatically, but you can also 
create the empty tables by using `create_tables.py`.  More importantly, 
if the tables already
exist, and you want to completely remove them and recreate them, use 
`python create_tables.py drop`.  This is useful for initially testing 
the parser on your xml files.

**Notes:**

* You will need to install python packages `sqlalchemy` and `pyodbc`.
* In order to get pyodbc to work on mac (and probably linux), you need to
  install unixodbc and freetds.  On Mac, these commands are:<br> 
`brew install unixodbc`<br>
`brew install freetds --with-unixodbc`
* An easy way to test without having to connect to a SQL database is to use
  SQLite.  The default connection in the config_example.ini file is set to 
  `sqlite:///my_database.db` which will create a database file in the current directory.
