from dwca.terms.field import Field
from dwca.terms.outside_term import OutsideTerm
from dwca.terms.record_level import DWCType, DWCModified, DWCLanguage, \
    DWCLicense, DWCRightsHolder, DWCAccessRights, DWCBibliographicCitation, \
    DWCReferences, DWCInstitution, DWCCollection, DWCDataset, \
    DWCInstitutionCode, DWCCollectionCode, DWCDatasetName, \
    DWCOwnerInstitutionCode, DWCBasisOfRecord, DWCInformationWithheld, \
    DWCDataGeneralizations, DWCDynamicProperties
from dwca.terms.occurrence import OccurrenceID, CatalogNumber, RecordNumber, \
    RecordedBy, RecordedByID, IndividualCount, OrganismQuantity, \
    OrganismQuantityType, OccurrenceSex, LifeStage, ReproductiveCondition, \
    Caste, Behavior, Vitality, DWCEstablishmentMeans, DWCDegreeOfEstablishment, \
    Pathway, GeoreferenceVerificationStatus, OccurrenceStatus, AssociatedMedia, \
    AssociatedOccurrences, AssociatedReferences, AssociatedTaxa, \
    OtherCatalogNumbers, OccurrenceRemarks
from dwca.terms.organism import OrganismID, OrganismName, OrganismScope, \
    AssociatedOrganisms, PreviousIdentifications, OrganismRemarks
from dwca.terms.material_entity import MaterialEntityID, Preparations, \
    Disposition, VerbatimLabel, AssociatedSequences, MaterialEntityRemarks
from dwca.terms.material_sample import MaterialSampleID
from dwca.terms.event import EventID, ParentEventID, EventType, FieldNumber, \
    EventDate, EventTime, StartDayOfYear, EndDayOfYear, DWCYear, DWCMonth, \
    DWCDay, VerbatimEventDate, Habitat, SamplingProtocol, SampleSizeValue, \
    SampleSizeUnit, SamplingEffort, FieldNotes, EventRemarks
from dwca.terms.location import LocationID, HigherGeographyID, HigherGeography, \
    Continent, WaterBody, IslandGroup, Island, Country, CountryCode, StateProvince, \
    County, Municipality, DWCLocalityTerm, VerbatimLocality, MinimumElevationInMeters, \
    MaximumElevationInMeters, VerbatimElevation, VerticalDatum, MinimumDepthInMeters, \
    MaximumDepthInMeters, VerbatimDepth, MinimumDistanceAboveSurfaceInMeters, \
    MaximumDistanceAboveSurfaceInMeters, LocationAccordingTo, LocationRemarks, \
    DecimalLatitude, DecimalLongitude, GeodeticDatum, CoordinateUncertaintyInMeters, \
    CoordinatePrecision, PointRadiusSpatialFit, VerbatimCoordinates, VerbatimLatitude, \
    VerbatimLongitude, VerbatimCoordinateSystem, VerbatimSRS, FootprintWKT, \
    FootprintSRS, FootprintSpatialFit, GeoreferencedBy, GeoreferencedDate, \
    GeoreferenceProtocol, GeoreferenceSources, GeoreferenceRemarks
from dwca.terms.geological_context import GeologicalContextID, EarliestEonOrLowestEonothem, \
    LatestEonOrHighestEonothem, EarliestEraOrLowestErathem, LatestEraOrHighestErathem, \
    EarliestPeriodOrLowestSystem, LatestPeriodOrHighestSystem, EarliestEpochOrLowestSeries, \
    LatestEpochOrHighestSeries, EarliestAgeOrLowestStage, LatestAgeOrHighestStage, \
    LowestBiostratigraphicZone, HighestBiostratigraphicZone, LithostratigraphicTerms, \
    LithostratigraphicGroup, LithostratigraphicFormation, LithostratigraphicMember, \
    LithostratigraphicBed
from dwca.terms.identification import IdentificationID, VerbatimIdentification, \
    IdentificationQualifier, TypeStatus, IdentifiedBy, IdentifiedByID, \
    DateIdentified, IdentificationReferences, IdentificationVerificationStatus, \
    IdentificationRemarks
from dwca.terms.taxon import TaxonID, ScientificNameID, AcceptedNameUsageID, ParentNameUsageID, \
    OriginalNameUsageID, NameAccordingToID, NamePublishedInID, TaxonConceptID, \
    ScientificName, AcceptedNameUsage, ParentNameUsage, OriginalNameUsage, NameAccordingTo, \
    NamePublishedIn, NamePublishedInYear, HigherClassification, Kingdom, Phylum, DWCClass, Order, \
    Superfamily, Family, Subfamily, Tribe, Subtribe, Genus, GenericName, Subgenus, \
    InfragenericEpithet, SpecificEpithet, InfraspecificEpithet, CultivarEpithet, \
    TaxonRank, VerbatimTaxonRank, ScientificNameAuthorship, VernacularName, NomenclaturalCode, \
    TaxonomicStatus, NomenclaturalStatus, TaxonRemarks
from dwca.terms.resource_relationship import ResourceRelationshipID, ResourceID, \
    RelationshipOfResourceID, RelatedResourceID, RelationshipOfResource, RelationshipAccordingTo, \
    RelationshipEstablishedDate, RelationshipRemarks
from dwca.terms.measurement_or_fact import MeasurementID, ParentMeasurementID, \
    MeasurementType, MeasurementValue, MeasurementAccuracy, MeasurementUnit, \
    MeasurementDeterminedBy, MeasurementDeterminedDate, MeasurementMethod, \
    MeasurementRemarks
from dwca.terms.chronometric_age import ChronometricAgeID, VerbatimChronometricAge, \
    ChronometricAgeProtocol, UncalibratedChronometricAge, ChronometricAgeConversionProtocol, \
    EarliestChronometricAge, EarliestChronometricAgeReferenceSystem, LatestChronometricAge, \
    LatestChronometricAgeReferenceSystem, ChronometricAgeUncertaintyInYears, \
    ChronometricAgeUncertaintyMethod, MaterialDated, MaterialDatedID, MaterialDatedRelationship, \
    ChronometricAgeDeterminedBy, ChronometricAgeDeterminedDate, ChronometricAgeReferences, \
    ChronometricAgeRemarks
