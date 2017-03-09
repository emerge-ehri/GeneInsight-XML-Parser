import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import xml.etree.ElementTree as ET
import sys, ConfigParser, pyodbc, datetime
from Reports import *

# In order to get pyodbc to work on mac, you must install unixodbc and freetds:  
# brew install unixodbc
# brew install freetds --with-unixodbc

# use the connection string from the config file to connect to the database
# Config = ConfigParser.ConfigParser()
# Config.read("config.ini")
# db_connection = Config.get("Database", "Connection")


class XMLParser:
    tables = [Report, InterpretedDiseases, PatientDiseases, ReportAssays, ReportVariants, 
                 NestedVariants, Specimens, Physicians]
                 
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.engine = sqlalchemy.create_engine(self.db_connection)
        
    def create_tables(self, drop_first):
        
        if (drop_first):
            print 'Dropping and creating tables.'
            self.__drop(self.engine, self.tables)

        self.__create(self.engine, self.tables)
        
    
    
    def parse(self, input_xml_file): 
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        if not ( Report.__table__.exists(bind=self.engine) and
                 InterpretedDiseases.__table__.exists(bind=self.engine) and
                 PatientDiseases.__table__.exists(bind=self.engine) and
                 ReportAssays.__table__.exists(bind=self.engine) and
                 ReportVariants.__table__.exists(bind=self.engine) and
                 NestedVariants.__table__.exists(bind=self.engine) and
                 Specimens.__table__.exists(bind=self.engine) ):
            self.create_tables(False)
            #raise sqlalchemy.exc.SQLAlchemyError(
            #    'One or more tables were not found.  Use create_tables.py script to create tables before parsing XML files.')
      
        # get the contents of the XML file
        tree = ET.parse(input_xml_file)
        root = tree.getroot()

        # Report Table
        report = Report(
            reportIdentifier             = self.__getValue(root, './reportIdentifier'), 
            reportDocType                = self.__getValue(root, './reportDocType'),
        #   reportDoc                    = self.__getValue(root, 'reportDoc'),  # this is the base64 PDF file
            caseType                     = self.__getValue(root, 'caseType'),
            editedBy                     = self.__getValue(root, './editedBy/value'),
            status                       = self.__getValue(root, './status'),
            statusBy                     = self.__getValue(root, './statusBy/value'),
            testType                     = self.__getValue(root, './testType/value'), 
            testType_codeSystem          = self.__getValue(root, './testType/codeSystem'), 
            testType_code                = self.__getValue(root, './testType/code'), 
            testType_abbr                = self.__getValue(root, './testType/valueSetAbbr'), 
            genomicSource                = self.__getValue(root, './genomicSource/value'), 
            genomicSource_codeSystem     = self.__getValue(root, './genomicSource/codeSystem'), 
            genomicSource_code           = self.__getValue(root, './genomicSource/code'), 
            genomicSource_abbr           = self.__getValue(root, './genomicSource/valueSetAbbr'),
            indicationCode               = self.__getValue(root, './indicationCode/value'), 
            indicationCode_codeSystem    = self.__getValue(root, './indicationCode/codeSystem'), 
            indicationCode_code          = self.__getValue(root, './indicationCode/code'), 
            indicationCode_abbr          = self.__getValue(root, './indicationCode/valueSetAbbr'),
            labStatus                    = self.__getValue(root, './labStatus'),
            localOrderNumber             = self.__getValue(root, './order/localOrderNumber'),
            senderEncounterNumber        = self.__getValue(root, './order/senderEncounterNumber'),
            senderFacilityName           = self.__getValue(root, './order/senderFacilityName'),
            senderFacilityNumber         = self.__getValue(root, './order/senderFacilityNumber'),
            senderLabControlNumber       = self.__getValue(root, './order/senderLabControlNumber'),
            senderOrderNumber            = self.__getValue(root, './order/senderOrderNumber'),
            senderPatientNumber          = self.__getValue(root, './order/senderPatientNumber'),
            deidentified                 = self.__getValue(root, './patient/deidentified'),
            diseaseStatus                = self.__getValue(root, './patient/diseaseStatus'),
            firstName                    = self.__getValue(root, './patient/firstName'),
            lastName                     = self.__getValue(root, './patient/lastName'),
            identifier                   = self.__getValue(root, './patient/identifier/value'),
            identifier_codeSystem        = self.__getValue(root, './patient/identifier/codeSystem'),
            identifier_code              = self.__getValue(root, './patient/identifier/code'),
            raceOrEthnicity              = self.__getValue(root, './patient/racesOrEthnicities//value'), 
            raceOrEthnicity_codeSystem   = self.__getValue(root, './patient/racesOrEthnicities//codeSystem'), 
            raceOrEthnicity_code         = self.__getValue(root, './patient/racesOrEthnicities//code'), 
            raceOrEthnicity_abbr         = self.__getValue(root, './patient/racesOrEthnicities//valueSetAbbr'),
            sex                          = self.__getValue(root, './patient/sex/value'), 
            sex_codeSystem               = self.__getValue(root, './patient/sex/codeSystem'), 
            sex_code                     = self.__getValue(root, './patient/sex/code'), 
            sex_abbr                     = self.__getValue(root, './patient/sex/valueSetAbbr'),
            editedBy_date                = self.__getDate(root, './editedBy/onDate'),
            statusBy_date                = self.__getDate(root, './statusBy/onDate'),
            dateOfBirth                  = self.__getDate(root, './patient/dateOfBirth'),
            orderDate                    = self.__getDate(root, './order/orderDate'),
        )
        # must commit so we can generate the auto-incremented primary key report_id which 
        # is used as the foreign key for all other tables.
        session.add(report)
        session.commit()  


        # Interpreted Diseases Table
        for disease in root.findall('./interpretedDiseases/disease'):
            interpreted_diseases =  InterpretedDiseases (
                report_id                = report.report_id,
                interpreted_disease      = self.__getValue(disease, './reportDisease/diseaseCode/value'),
                codeSystem               = self.__getValue(disease, './reportDisease/diseaseCode/codeSystem'),
                code                     = self.__getValue(disease, './reportDisease/diseaseCode/code'),
                valueSetAbbr             = self.__getValue(disease, './reportDisease/diseaseCode/valueSetAbbr'),
                name                     = self.__getValue(disease, './reportDisease/name'),
            )
            session.add(interpreted_diseases)


        # Patient Diseases Table
        for disease in root.findall('./patientDiseases/disease'):            
            patient_diseases =  PatientDiseases (
                report_id                = report.report_id,
                patient_disease          = self.__getValue(disease, './reportDisease/diseaseCode/value'),
                codeSystem               = self.__getValue(disease, './reportDisease/diseaseCode/codeSystem'),
                code                     = self.__getValue(disease, './reportDisease/diseaseCode/code'),
                valueSetAbbr             = self.__getValue(disease, './reportDisease/diseaseCode/valueSetAbbr'),
                name                     = self.__getValue(disease, './reportDisease/name'),

            )
            session.add(patient_diseases)

        for phys in root.findall('./physicians/physician'):
            physicians =  Physicians (
                report_id                = report.report_id,
                physician                = self.__getValue(phys, '.'),
            )
            session.add(physicians)
        
        # Report Assays Table
        for assay in root.findall('./reportAssays/reportAssay'):
            report_assay = ReportAssays (
                report_id                = report.report_id,
                assayVersionExternalId   = self.__getValue(assay, './/assayVersionExternalId'),
                known                    = self.__getValue(assay, './/known'),
                testCode                 = self.__getValue(assay, './/testCode'),
                testName                 = self.__getValue(assay, './/testName'),
            )
            session.add(report_assay)


        # Report Variants Table
        for variant in root.findall('./reportVariants/reportVariant'):
            report_variant = ReportVariants (
                report_id                = report.report_id,
                aminoAcidChange          = self.__getValue(variant, './/aminoAcidChange'),
                aminoAcidChangeType      = self.__getValue(variant, './/aminoAcidChangeType'),
                chromosome               = self.__getValue(variant, './/chromosome'),
                dnaChange                = self.__getValue(variant, './/dnaChange'),
                dnaChangeType            = self.__getValue(variant, './/dnaChangeType'),
                externalId               = self.__getValue(variant, './/externalId'),
                geneRegion               = self.__getValue(variant, './/geneRegion'),
                transcriptId             = self.__getValue(variant, './/transcriptId'),
                alleleState              = self.__getValue(variant, './/alleleState/value'),
                alleleState_codeSystem   = self.__getValue(variant, './/alleleState/codeSystem'),
                alleleState_code         = self.__getValue(variant, './/alleleState/code'),
                alleleState_abbr         = self.__getValue(variant, './/alleleState/valueSetAbbr'),
                category                 = self.__getValue(variant, './/category/value'),
                category_codeSystem      = self.__getValue(variant, './/category/codeSystem'),
                category_code            = self.__getValue(variant, './/category/code'),
                category_abbr            = self.__getValue(variant, './/category/valueSetAbbr'),
                categoryType             = self.__getValue(variant, './/categoryType'),
                forcedIncidental         = self.__getValue(variant, './/forcedIncidental'),
                geneSymbol               = self.__getValue(variant, './/geneSymbol'),
                genomicSource            = self.__getValue(variant, './/genomicSource/value'),
                genomicSource_codeSystem = self.__getValue(variant, './/genomicSource/codeSystem'),
                genomicSource_code       = self.__getValue(variant, './/genomicSource/code'),
                genomicSource_abbr       = self.__getValue(variant, './/genomicSource/valueSetAbbr'),
                interrogatedButNotFound  = self.__getValue(variant, './/interrogatedButNotFound'),
                isSignificant            = self.__getValue(variant, './/isSignificant'),
                notInterpreted           = self.__getValue(variant, './/notInterpreted'),
            )
            session.add(report_variant)


        # Nested Variants Table
        for variant in root.findall('./reportVariants/reportVariant//nestedVariants/reportVariant'):
            nested_variant = NestedVariants (
                report_id                = report.report_id,
                aminoAcidChange          = self.__getValue(variant, './/aminoAcidChange'),
                aminoAcidChangeType      = self.__getValue(variant, './/aminoAcidChangeType'),
                chromosome               = self.__getValue(variant, './/chromosome'),
                dnaChange                = self.__getValue(variant, './/dnaChange'),
                dnaChangeType            = self.__getValue(variant, './/dnaChangeType'),
                externalId               = self.__getValue(variant, './/externalId'),
                geneRegion               = self.__getValue(variant, './/geneRegion'),
                transcriptId             = self.__getValue(variant, './/transcriptId'),
                alleleState              = self.__getValue(variant, './/alleleState/value'),
                alleleState_codeSystem   = self.__getValue(variant, './/alleleState/codeSystem'),
                alleleState_code         = self.__getValue(variant, './/alleleState/code'),
                alleleState_abbr         = self.__getValue(variant, './/alleleState/valueSetAbbr'),
                category                 = self.__getValue(variant, './/category/value'),
                category_codeSystem      = self.__getValue(variant, './/category/codeSystem'),
                category_code            = self.__getValue(variant, './/category/code'),
                category_abbr            = self.__getValue(variant, './/category/valueSetAbbr'),
                categoryType             = self.__getValue(variant, './/categoryType'),
                forcedIncidental         = self.__getValue(variant, './/forcedIncidental'),
                geneSymbol               = self.__getValue(variant, './/geneSymbol'),
                genomicSource            = self.__getValue(variant, './/genomicSource/value'),
                genomicSource_codeSystem = self.__getValue(variant, './/genomicSource/codeSystem'),
                genomicSource_code       = self.__getValue(variant, './/genomicSource/code'),
                genomicSource_abbr       = self.__getValue(variant, './/genomicSource/valueSetAbbr'),
                interrogatedButNotFound  = self.__getValue(variant, './/interrogatedButNotFound'),
                isSignificant            = self.__getValue(variant, './/isSignificant'),
                notInterpreted           = self.__getValue(variant, './/notInterpreted'),
            )
            session.add(nested_variant)


        # Specimens Table
        for specimen in root.findall('./specimens/specimen'):
            specimens = Specimens (
                report_id       = report.report_id, 
                collectionDate  = self.__getDate(specimen, './/collectionDate'),
                receivedDate    = self.__getDate(specimen, './/receivedDate'),
                description     = self.__getValue(specimen, './/description'),
                label           = self.__getValue(specimen, './/label'),
                metastatic      = self.__getValue(specimen, './/metastatic'),
                specimen_type   = self.__getValue(specimen, './/type/value'),
                type_codeSystem = self.__getValue(specimen, './/type/codeSystem'),
                type_code       = self.__getValue(specimen, './/type/code'),
                type_abbr       = self.__getValue(specimen, './/type/valueSetAbbr'),
            )
            session.add(specimens)
        session.commit()
        


 
        
    def __getValue(self, elem, xpath):
        value = None
        if elem.find(xpath) is not None:
            value = elem.find(xpath).text
        return value
      
    # Parse the dates:
    # This assumes the XML file will always use the format:
    # 2014-11-24 17:41:07.477 UTC
    # Only the date (not the time) is used
    def __getDate(self, elem, xpath):
        date = None
        str = elem.find(xpath)
        if str is not None:
            date = datetime.datetime.strptime(str.text.split(" ")[0], "%Y-%m-%d").date()
        return date
        
    def __drop(self, engine, tables):
        # drop the first table last since all the other tables have 
        # foreign keys referencing it
        primary_table = tables[0]
        for table in tables[1:]:
            table.__table__.drop(bind=engine, checkfirst=True)
        primary_table.__table__.drop(bind=engine, checkfirst=True)
            
    def __create(self, engine, tables):
        for table in tables:
            table.__table__.create(bind=engine, checkfirst=True)
        
 
            




