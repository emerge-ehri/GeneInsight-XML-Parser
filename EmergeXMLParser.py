import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import xml.etree.ElementTree as ET
import sys, ConfigParser, pyodbc, datetime
import Reports

# In order to get pyodbc to work on mac, you must install unixodbc and freetds:  
# brew install unixodbc
# brew install freetds --with-unixodbc

# use the connection string from the config file to connect to the database
# Config = ConfigParser.ConfigParser()
# Config.read("config.ini")
# db_connection = Config.get("Database", "Connection")


class XMLParser:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.engine = sqlalchemy.create_engine(self.db_connection)
        
    
    def create_tables(self, drop_tables):
        if (drop_tables):
            print 'Dropping and creating tables.'
            Reports.InterpretedDiseases.__table__.drop(bind=self.engine, checkfirst=True)
            Reports.PatientDiseases.__table__.drop(bind=self.engine, checkfirst=True)
            Reports.ReportAssays.__table__.drop(bind=self.engine, checkfirst=True)
            Reports.ReportVariants.__table__.drop(bind=self.engine, checkfirst=True)
            Reports.NestedVariants.__table__.drop(bind=self.engine, checkfirst=True)
            Reports.Specimens.__table__.drop(bind=self.engine, checkfirst=True)
            Reports.Physicians.__table__.drop(bind=self.engine, checkfirst=True)
            Reports.Report.__table__.drop(bind=self.engine, checkfirst=True)

        Reports.Report.__table__.create(bind=self.engine, checkfirst=True)
        Reports.InterpretedDiseases.__table__.create(bind=self.engine, checkfirst=True)
        Reports.PatientDiseases.__table__.create(bind=self.engine, checkfirst=True)
        Reports.ReportAssays.__table__.create(bind=self.engine, checkfirst=True)
        Reports.Physicians.__table__.create(bind=self.engine, checkfirst=True)
        Reports.ReportVariants.__table__.create(bind=self.engine, checkfirst=True)
        Reports.NestedVariants.__table__.create(bind=self.engine, checkfirst=True)
        Reports.Specimens.__table__.create(bind=self.engine, checkfirst=True)
        
    
    
    def parse(self, input_xml_file): 
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        if not ( Reports.Report.__table__.exists(bind=self.engine) and
                 Reports.InterpretedDiseases.__table__.exists(bind=self.engine) and
                 Reports.PatientDiseases.__table__.exists(bind=self.engine) and
                 Reports.ReportAssays.__table__.exists(bind=self.engine) and
                 Reports.ReportVariants.__table__.exists(bind=self.engine) and
                 Reports.NestedVariants.__table__.exists(bind=self.engine) and
                 Reports.Specimens.__table__.exists(bind=self.engine) ):
            self.create_tables(False)
            #raise sqlalchemy.exc.SQLAlchemyError(
            #    'One or more tables were not found.  Use create_tables.py script to create tables before parsing XML files.')
      
        # get the contents of the XML file
        tree = ET.parse(input_xml_file)
        root = tree.getroot()

        # Report Table
        report = Reports.Report(
            reportIdentifier             = self.getValue(root, './reportIdentifier'), 
            reportDocType                = self.getValue(root, './reportDocType'),
        #   reportDoc                    = self.getValue(root, 'reportDoc'),  # this is the base64 PDF file
            caseType                     = self.getValue(root, 'caseType'),
            editedBy                     = self.getValue(root, './editedBy/value'),
            status                       = self.getValue(root, './status'),
            statusBy                     = self.getValue(root, './statusBy/value'),
            testType                     = self.getValue(root, './testType/value'), 
            testType_codeSystem          = self.getValue(root, './testType/codeSystem'), 
            testType_code                = self.getValue(root, './testType/code'), 
            testType_abbr                = self.getValue(root, './testType/valueSetAbbr'), 
            genomicSource                = self.getValue(root, './genomicSource/value'), 
            genomicSource_codeSystem     = self.getValue(root, './genomicSource/codeSystem'), 
            genomicSource_code           = self.getValue(root, './genomicSource/code'), 
            genomicSource_abbr           = self.getValue(root, './genomicSource/valueSetAbbr'),
            indicationCode               = self.getValue(root, './indicationCode/value'), 
            indicationCode_codeSystem    = self.getValue(root, './indicationCode/codeSystem'), 
            indicationCode_code          = self.getValue(root, './indicationCode/code'), 
            indicationCode_abbr          = self.getValue(root, './indicationCode/valueSetAbbr'),
            labStatus                    = self.getValue(root, './labStatus'),
            deidentified                 = self.getValue(root, './patient/deidentified'),
            diseaseStatus                = self.getValue(root, './patient/diseaseStatus'),
            firstName                    = self.getValue(root, './patient/firstName'),
            lastName                     = self.getValue(root, './patient/lastName'),
            identifier                   = self.getValue(root, './patient/identifier/value'),
            identifier_codeSystem        = self.getValue(root, './patient/identifier/codeSystem'),
            identifier_code              = self.getValue(root, './patient/identifier/code'),
            raceOrEthnicity              = self.getValue(root, './patient/racesOrEthnicities//value'), 
            raceOrEthnicity_codeSystem   = self.getValue(root, './patient/racesOrEthnicities//codeSystem'), 
            raceOrEthnicity_code         = self.getValue(root, './patient/racesOrEthnicities//code'), 
            raceOrEthnicity_abbr         = self.getValue(root, './patient/racesOrEthnicities//valueSetAbbr'),
            sex                          = self.getValue(root, './patient/sex/value'), 
            sex_codeSystem               = self.getValue(root, './patient/sex/codeSystem'), 
            sex_code                     = self.getValue(root, './patient/sex/code'), 
            sex_abbr                     = self.getValue(root, './patient/sex/valueSetAbbr'),
            editedBy_date                = self.getDate(root, './editedBy/onDate'),
            statusBy_date                = self.getDate(root, './statusBy/onDate'),
            dateOfBirth                  = self.getDate(root, './patient/dateOfBirth'),
        )
        # must commit so we can generate the auto-incremented primary key report_id which 
        # is used as the foreign key for all other tables.
        session.add(report)
        session.commit()  


        # Interpreted Diseases Table
        for disease in root.findall('./interpretedDiseases/disease'):
            interpreted_diseases =  Reports.InterpretedDiseases (
                report_id                = report.report_id,
                interpreted_disease      = self.getValue(disease, './reportDisease/diseaseCode/value'),
                codeSystem               = self.getValue(disease, './reportDisease/diseaseCode/codeSystem'),
                code                     = self.getValue(disease, './reportDisease/diseaseCode/code'),
                valueSetAbbr             = self.getValue(disease, './reportDisease/diseaseCode/valueSetAbbr'),
                name                     = self.getValue(disease, './reportDisease/name'),
            )
            session.add(interpreted_diseases)


        # Patient Diseases Table
        for disease in root.findall('./patientDiseases/disease'):            
            patient_diseases =  Reports.PatientDiseases (
                report_id                = report.report_id,
                patient_disease          = self.getValue(disease, './reportDisease/diseaseCode/value'),
                codeSystem               = self.getValue(disease, './reportDisease/diseaseCode/codeSystem'),
                code                     = self.getValue(disease, './reportDisease/diseaseCode/code'),
                valueSetAbbr             = self.getValue(disease, './reportDisease/diseaseCode/valueSetAbbr'),
                name                     = self.getValue(disease, './reportDisease/name'),

            )
            session.add(patient_diseases)

        for phys in root.findall('./physicians/physician'):
            physicians =  Reports.Physicians (
                report_id                = report.report_id,
                physician                = self.getValue(phys, '.'),
            )
            session.add(physicians)
        
        # Report Assays Table
        for assay in root.findall('./reportAssays/reportAssay'):
            report_assay = Reports.ReportAssays (
                report_id                = report.report_id,
                assayVersionExternalId   = self.getValue(assay, './/assayVersionExternalId'),
                known                    = self.getValue(assay, './/known'),
                testCode                 = self.getValue(assay, './/testCode'),
                testName                 = self.getValue(assay, './/testName'),
            )
            session.add(report_assay)


        # Report Variants Table
        for variant in root.findall('./reportVariants/reportVariant'):
            report_variant = Reports.ReportVariants (
                report_id                = report.report_id,
                aminoAcidChange          = self.getValue(variant, './/aminoAcidChange'),
                aminoAcidChangeType      = self.getValue(variant, './/aminoAcidChangeType'),
                chromosome               = self.getValue(variant, './/chromosome'),
                dnaChange                = self.getValue(variant, './/dnaChange'),
                dnaChangeType            = self.getValue(variant, './/dnaChangeType'),
                externalId               = self.getValue(variant, './/externalId'),
                geneRegion               = self.getValue(variant, './/geneRegion'),
                transcriptId             = self.getValue(variant, './/transcriptId'),
                alleleState              = self.getValue(variant, './/alleleState/value'),
                alleleState_codeSystem   = self.getValue(variant, './/alleleState/codeSystem'),
                alleleState_code         = self.getValue(variant, './/alleleState/code'),
                alleleState_abbr         = self.getValue(variant, './/alleleState/valueSetAbbr'),
                category                 = self.getValue(variant, './/category/value'),
                category_codeSystem      = self.getValue(variant, './/category/codeSystem'),
                category_code            = self.getValue(variant, './/category/code'),
                category_abbr            = self.getValue(variant, './/category/valueSetAbbr'),
                categoryType             = self.getValue(variant, './/categoryType'),
                forcedIncidental         = self.getValue(variant, './/forcedIncidental'),
                geneSymbol               = self.getValue(variant, './/geneSymbol'),
                genomicSource            = self.getValue(variant, './/genomicSource/value'),
                genomicSource_codeSystem = self.getValue(variant, './/genomicSource/codeSystem'),
                genomicSource_code       = self.getValue(variant, './/genomicSource/code'),
                genomicSource_abbr       = self.getValue(variant, './/genomicSource/valueSetAbbr'),
                interrogatedButNotFound  = self.getValue(variant, './/interrogatedButNotFound'),
                isSignificant            = self.getValue(variant, './/isSignificant'),
                notInterpreted           = self.getValue(variant, './/notInterpreted'),
            )
            session.add(report_variant)


        # Nested Variants Table
        for variant in root.findall('./reportVariants/reportVariant/nestedVariants'):
            nested_variant = Reports.NestedVariants (
                report_id                = report.report_id,
                aminoAcidChange          = self.getValue(variant, './/aminoAcidChange'),
                aminoAcidChangeType      = self.getValue(variant, './/aminoAcidChangeType'),
                chromosome               = self.getValue(variant, './/chromosome'),
                dnaChange                = self.getValue(variant, './/dnaChange'),
                dnaChangeType            = self.getValue(variant, './/dnaChangeType'),
                externalId               = self.getValue(variant, './/externalId'),
                geneRegion               = self.getValue(variant, './/geneRegion'),
                transcriptId             = self.getValue(variant, './/transcriptId'),
                alleleState              = self.getValue(variant, './/alleleState/value'),
                alleleState_codeSystem   = self.getValue(variant, './/alleleState/codeSystem'),
                alleleState_code         = self.getValue(variant, './/alleleState/code'),
                alleleState_abbr         = self.getValue(variant, './/alleleState/valueSetAbbr'),
                category                 = self.getValue(variant, './/category/value'),
                category_codeSystem      = self.getValue(variant, './/category/codeSystem'),
                category_code            = self.getValue(variant, './/category/code'),
                category_abbr            = self.getValue(variant, './/category/valueSetAbbr'),
                categoryType             = self.getValue(variant, './/categoryType'),
                forcedIncidental         = self.getValue(variant, './/forcedIncidental'),
                geneSymbol               = self.getValue(variant, './/geneSymbol'),
                genomicSource            = self.getValue(variant, './/genomicSource/value'),
                genomicSource_codeSystem = self.getValue(variant, './/genomicSource/codeSystem'),
                genomicSource_code       = self.getValue(variant, './/genomicSource/code'),
                genomicSource_abbr       = self.getValue(variant, './/genomicSource/valueSetAbbr'),
                interrogatedButNotFound  = self.getValue(variant, './/interrogatedButNotFound'),
                isSignificant            = self.getValue(variant, './/isSignificant'),
                notInterpreted           = self.getValue(variant, './/notInterpreted'),
            )
            session.add(report_variant)


        # Specimens Table
        for specimen in root.findall('./specimens/specimen'):
            specimens = Reports.Specimens (
                report_id       = report.report_id, 
                collectionDate  = self.getDate(specimen, './/collectionDate'),
                receivedDate    = self.getDate(specimen, './/receivedDate'),
                description     = self.getValue(specimen, './/description'),
                label           = self.getValue(specimen, './/label'),
                metastatic      = self.getValue(specimen, './/metastatic'),
                specimen_type   = self.getValue(specimen, './/type/value'),
                type_codeSystem = self.getValue(specimen, './/type/codeSystem'),
                type_code       = self.getValue(specimen, './/type/code'),
                type_abbr       = self.getValue(specimen, './/type/valueSetAbbr'),
            )
            session.add(specimens)
        session.commit()
        
        
    def getValue(self, elem, xpath):
        value = None
        if elem.find(xpath) is not None:
            value = elem.find(xpath).text
        return value
      
    # Parse the dates:
    # This assumes the XML file will always use the format:
    # 2014-11-24 17:41:07.477 UTC
    # Only the date (not the time) is used
    def getDate(self, elem, xpath):
        date = None
        str = elem.find(xpath).text
        if str is not None:
            date = datetime.datetime.strptime(str.split(" ")[0], "%Y-%m-%d").date()
        return date
        
 
            




