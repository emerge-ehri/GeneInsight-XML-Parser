from sqlalchemy import Table, Column, Date, String, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Report(Base):
    __tablename__ = 'Patient_Reports'
    report_id                   = Column(Integer, primary_key=True)
    reportIdentifier            = Column(String(255))
    reportDocType               = Column(String(255))
    caseType                    = Column(String(255))
    editedBy                    = Column(String(255))
    editedBy_date               = Column(Date)
    status                      = Column(String(255))
    statusBy                    = Column(String(255))
    statusBy_date               = Column(Date)
    testType                    = Column(String(255))
    testType_codeSystem         = Column(String(255))
    testType_code               = Column(String(255))
    testType_abbr               = Column(String(255))
    genomicSource               = Column(String(255))
    genomicSource_codeSystem    = Column(String(255))
    genomicSource_code          = Column(String(255))
    genomicSource_abbr          = Column(String(255))
    indicationCode              = Column(String(255))
    indicationCode_codeSystem   = Column(String(255))
    indicationCode_code         = Column(String(255))
    indicationCode_abbr         = Column(String(255))
    labStatus                   = Column(String(255))
    localOrderNumber            = Column(String(255))
    orderDate                   = Column(Date)
    senderEncounterNumber       = Column(String(255))
    senderFacilityName          = Column(String(255))
    senderFacilityNumber        = Column(String(255))
    senderLabControlNumber      = Column(String(255))
    senderOrderNumber           = Column(String(255))
    senderPatientNumber         = Column(String(255))
    dateOfBirth                 = Column(Date)
    deidentified                = Column(String(255))
    diseaseStatus               = Column(String(255))
    firstName                   = Column(String(255))
    lastName                    = Column(String(255))
    identifier                  = Column(String(255))
    identifier_codeSystem       = Column(String(255))
    identifier_code             = Column(String(255))
    raceOrEthnicity             = Column(String(255))
    raceOrEthnicity_codeSystem  = Column(String(255))
    raceOrEthnicity_code        = Column(String(255))
    raceOrEthnicity_abbr        = Column(String(255))
    sex                         = Column(String(255))
    sex_codeSystem              = Column(String(255))
    sex_code                    = Column(String(255))
    sex_abbr                    = Column(String(255))


class InterpretedDiseases (Base):
    __tablename__ = 'Patient_Reports_InterpretedDiseases'
    disease_id                   = Column(Integer, primary_key=True)
    report_id                    = Column(Integer, ForeignKey("Patient_Reports.report_id"), nullable=False)
    interpreted_disease          = Column(String(255))
    codeSystem                   = Column(String(255))
    code                         = Column(String(255))
    valueSetAbbr                 = Column(String(255))
    name                         = Column(String(255))


class PatientDiseases (Base):
    __tablename__ = 'Patient_Reports_PatientDiseases'
    disease_id                   = Column(Integer, primary_key=True)
    report_id                    = Column(Integer, ForeignKey("Patient_Reports.report_id"), nullable=False)
    patient_disease              = Column(String(255))
    codeSystem                   = Column(String(255))
    code                         = Column(String(255))
    valueSetAbbr                 = Column(String(255))
    name                         = Column(String(255))

class Physicians(Base):
    __tablename__ = 'Patient_Reports_Physicians'
    physician_id                 = Column(Integer, primary_key=True)
    report_id                    = Column(Integer, ForeignKey("Patient_Reports.report_id"), nullable=False)
    physician                    = Column(String(255))

class ReportAssays (Base):
    __tablename__ = 'Patient_Reports_ReportAssays'
    assay_id                     = Column(Integer, primary_key=True)
    report_id                    = Column(Integer, ForeignKey("Patient_Reports.report_id"), nullable=False)
    assayVersionExternalId       = Column(String(255))
    known                        = Column(String(255))
    testCode                     = Column(String(255))
    testName                     = Column(String(255))


class ReportVariants (Base):
    __tablename__ = 'Patient_Reports_ReportVariants'
    variant_id                           = Column(Integer, primary_key=True)
    report_id                    = Column(Integer, ForeignKey("Patient_Reports.report_id"), nullable=False)
    aminoAcidChange              = Column(String(255))
    aminoAcidChangeType          = Column(String(255))
    chromosome                   = Column(String(255))
    dnaChange                    = Column(String(255))
    dnaChangeType                = Column(String(255))
    externalId                   = Column(String(255))
    geneRegion                   = Column(String(255))
    transcriptId                 = Column(String(255))
    alleleState                  = Column(String(255))
    alleleState_codeSystem       = Column(String(255))
    alleleState_code             = Column(String(255))
    alleleState_abbr             = Column(String(255)) 
    category                     = Column(String(255))
    category_codeSystem          = Column(String(255))
    category_code                = Column(String(255))
    category_abbr                = Column(String(255))
    categoryType                 = Column(String(255))
    forcedIncidental             = Column(String(255))
    geneSymbol                   = Column(String(255))
    genomicSource                = Column(String(255))
    genomicSource_codeSystem     = Column(String(255))
    genomicSource_code           = Column(String(255))
    genomicSource_abbr           = Column(String(255))
    interrogatedButNotFound      = Column(String(255))
    isSignificant                = Column(String(255))
    notInterpreted               = Column(String(255)) # Maybe use Boolean?


class NestedVariants (Base):
    __tablename__ = 'Patient_Reports_NestedVariants'
    nested_variant_id                           = Column(Integer, primary_key=True)
    report_id                    = Column(Integer, ForeignKey("Patient_Reports.report_id"), nullable=False)
    aminoAcidChange              = Column(String(255))
    aminoAcidChangeType          = Column(String(255))
    chromosome                   = Column(String(255))
    dnaChange                    = Column(String(255))
    dnaChangeType                = Column(String(255))
    externalId                   = Column(String(255))
    geneRegion                   = Column(String(255))
    transcriptId                 = Column(String(255))
    alleleState                  = Column(String(255))
    alleleState_codeSystem       = Column(String(255))
    alleleState_code             = Column(String(255))
    alleleState_abbr             = Column(String(255)) 
    category                     = Column(String(255))
    category_codeSystem          = Column(String(255))
    category_code                = Column(String(255))
    category_abbr                = Column(String(255))
    categoryType                 = Column(String(255))
    forcedIncidental             = Column(String(255))
    geneSymbol                   = Column(String(255))
    genomicSource                = Column(String(255))
    genomicSource_codeSystem     = Column(String(255))
    genomicSource_code           = Column(String(255))
    genomicSource_abbr           = Column(String(255))
    interrogatedButNotFound      = Column(String(255))
    isSignificant                = Column(String(255))
    notInterpreted               = Column(String(255)) # Maybe use Boolean?


class Specimens (Base):
    __tablename__ = 'Patient_Reports_Specimens'
    specimen_id                           = Column(Integer, primary_key=True)
    report_id                    = Column(Integer, ForeignKey("Patient_Reports.report_id"), nullable=False)
    collectionDate               = Column(Date)
    description                  = Column(String(255))
    label                        = Column(String(255))
    metastatic                   = Column(String(255))
    receivedDate                 = Column(Date)
    specimen_type                = Column(String(255))
    type_codeSystem              = Column(String(255))
    type_code                    = Column(String(255))
    type_abbr                    = Column(String(255))

