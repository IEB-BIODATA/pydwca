from typing import List

from dwca.terms import Field


class TaxonID(Field):
    """
    An identifier for the set of Taxon information.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/taxonID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ScientificNameID(Field):
    """
    An identifier for the nomenclatural (not taxonomic) details of a scientific name.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/scientificNameID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class AcceptedNameUsageID(Field):
    """
    An identifier for the name usage of the taxon.

    This term should be used for synonyms or misapplied names
    to refer to the taxonID of a Taxon record that represents
    the accepted (botanical) or valid (zoological) name. For
    Darwin Core Archives the related record should be present
    locally in the same archive.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/acceptedNameUsageID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ParentNameUsageID(Field):
    """
    An identifier for the name usage f the direct, most proximate higher-rank parent taxon.

    The name usage, documented meaning of the name according
    to a source, of the direct, most proximate higher-rank
    parent taxon (in a classification) of the most specific
    element of the Scientific Name.
    This term should be used for accepted names to refer to
    the taxonID of a Taxon record that represents the next
    higher taxon rank in the same taxonomic classification.
    For Darwin Core Archives the related record should be
    present locally in the same archive.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/parentNameUsageID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class OriginalNameUsageID(Field):
    """
    An identifier for the name usage in which the terminal term was originally established.

    This term should be used to refer to the taxonID of a
    Taxon record that represents the usage of the terminal
    element of the scientificName as originally established
    under the rules of the associated nomenclaturalCode.
    For example, for names governed by the ICNafp, this
    term would establish the relationship between a record
    representing a subsequent combination and the record
    for its corresponding basionym. Unlike basionyms,
    however, this term can apply to scientific names
    at all ranks. For Darwin Core Archives the related
    record should be present locally in the same archive.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/originalNameUsageID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class NameAccordingToID(Field):
    """
    An identifier for the source in which the specific taxon concept circumscription is defined or implied.

    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/nameAccordingToID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class NamePublishedInID(Field):
    """
    An identifier for the publication in which the scientificName was originally established.

    Under the rules of the associated Nomenclatural Code.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/namePublishedInID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class TaxonConceptID(Field):
    """
    An identifier for the taxonomic concept to which the record refers.

    Not for the nomenclatural details of a Taxon.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/taxonConceptID"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ScientificName(Field):
    """
    The full scientific name, with authorship and date information if known.

    When forming part of an Identification, this should be the name
    in the lowest level taxonomic rank that can be determined.
    This term should not contain identification qualifications,
    which should instead be supplied in the identificationQualifier
    term.
    When applied to an Organism or Occurrence, this term should be
    used to represent the scientific name that was applied to the
    associated Organism in accordance with the Taxon to which it
    was or is currently identified. Names should be compliant to
    the most recent nomenclatural code. For example, names of
    hybrids for algae, fungi and plants should follow the rules
    of the International Code of Nomenclature for algae, fungi,
    and plants (Schenzhen Code Articles H.1, H.2 and H.3). Thus,
    use the multiplication sign × (Unicode U+00D7, HTML ×) to
    identify a hybrid, not x or X, if possible.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/scientificName"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class AcceptedNameUsage(Field):
    """
    The full name, with authorship and date information if known, of the Taxon.

    The full scientific name, with authorship and date
    information if known, of the accepted (botanical)
    or valid (zoological) name in cases where the
    provided Scientific Name is considered by the
    reference indicated in the ``According To`` property,
    or of the content provider, to be a synonym or misapplied
    name. When applied to an Organism or an Occurrence, this
    term should be used in cases where a content provider
    regards the provided Scientific Name to be inconsistent
    with the taxonomic perspective of the content provider.
    For example, there are many discrepancies within specimen
    collections and observation datasets between the recorded
    name (e.g., the most recent identification from an expert
    who examined a specimen, or a field identification for an
    observed Organism), and the name asserted by the content
    provider to be taxonomically accepted.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/acceptedNameUsage"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ParentNameUsage(Field):
    """
    The direct, most proximate higher-rank parent Taxon of the most specific element of the Scientific Name.

    The full name, with authorship and date information
    if known, of the direct, most proximate higher-rank
    parent Taxon (in a classification) of the most specific
    element of the Scientific Name.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/parentNameUsage"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class OriginalNameUsage(Field):
    """
    The taxon name as it originally appeared when first established.

    The taxon name, with authorship and date information if
    known, as it originally appeared when first established
    under the rules of the associated Nomenclatural Code. The
    basionym (botany) or basonym (bacteriology) of the
    Scientific Name or the senior/earlier homonym for
    replaced names. For example, for names governed by the
    ICNafp, this term would indicate the basionym of a record
    representing a subsequent combination. Unlike basionyms,
    however, this term can apply to scientific names at all ranks.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/originalNameUsage"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class NameAccordingTo(Field):
    """
    The reference to the source in which the specific taxon concept circumscription is defined or implied.

    Traditionally signified by the Latin "sensu" or "sec."
    (from secundum, meaning "according to"). For taxa that
    result from identifications, a reference to the keys,
    monographs, experts and other sources should be given.
    This term provides context to the Scientific Name. Together
    with the Scientific Name, separated by sensu or sec., it
    forms the taxon concept label, which may be seen as having
    the same relationship to ``Taxon Concept ID`` as, for example,
    Accepted Name Usage has to ``Accepted Name Usage ID``. When
    not provided, in Taxon Core data sets the Name According To
    can be taken to be the data set. In this case the data set
    mostly provides sufficient context to infer the delimitation
    of the taxon and its relationship with other taxa. In Occurrence
    Core data sets, when not provided, Name According To can be
    an underlying taxonomy of the data set, e.g. `Plants of the
    World Online <http://powo.science.kew.org/>`_ for vascular
    plant records in iNaturalist (in which case it should be
    provided), or, which is the case for most Preserved Specimen
    data sets, the Identification, in which case there is no
    further context.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/nameAccordingTo"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class NamePublishedIn(Field):
    """
    A reference for the publication in which the Scientific Name was originally established.

    Established under the rules of the associated Nomenclatural Code.
    A citation of the first publication of the name in its given
    combination, not the basionym / original name. Recombinations
    are often not published in zoology, in which case Name Published In
    should be empty.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/namePublishedIn"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class NamePublishedInYear(Field):
    """
    The four-digit year in which the Scientific Name was published.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/namePublishedInYear"
    TYPE = int

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class HigherClassification(Field):
    """
    A list of taxa names terminating at the rank immediately superior to the referenced Taxon.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/higherClassification"
    TYPE = List[str]

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Kingdom(Field):
    """
    The full scientific name of the kingdom in which the Taxon is classified.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/kingdom"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Phylum(Field):
    """
    The full scientific name of the phylum or division in which the Taxon is classified.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/phylum"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class DWCClass(Field):
    """
    The full scientific name of the class in which the Taxon is classified.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/class"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Order(Field):
    """
    The full scientific name of the order in which the Taxon is classified.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/order"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Superfamily(Field):
    """
    The full scientific name of the superfamily in which the Taxon is classified.

    A taxonomic category subordinate to an order and
    superior to a family. According to ICZN article
    29.2, the suffix `-oidea` is used for a
    superfamily name.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/superfamily"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Family(Field):
    """
    The full scientific name of the family in which the Taxon is classified.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/family"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Subfamily(Field):
    """
    The full scientific name of the subfamily in which the Taxon is classified.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/subfamily"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Tribe(Field):
    """
    The full scientific name of the tribe in which the Taxon is classified.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/tribe"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Subtribe(Field):
    """
    The full scientific name of the subtribe in which the Taxon is classified.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/subtribe"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Genus(Field):
    """
    The full scientific name of the genus in which the Taxon is classified.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/genus"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class GenericName(Field):
    """
    The genus part of the Scientific Name without authorship.

    For synonyms the accepted genus and the genus
    part of the name may be different. The term ``Generic Name`` should
    be used together with ``Specific Epithet`` to form a binomial
    and with Infraspecific Epithet to form a trinomial. The
    term Generic Name should only be used for combinations.
    Uninomials of generic rank do not have a Generic Name.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/genericName"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class Subgenus(Field):
    """
    The full scientific name of the subgenus in which the Taxon is classified.

    Values should include the genus to avoid homonym confusion.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/subgenus"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class InfragenericEpithet(Field):
    """
    The infrageneric part of a binomial name at ranks above species but below genus.

    The term ``Infrageneric Epithet`` should be used in
    conjunction with ``Generic Name``, ``Specific Epithet``,
    ``Infraspecific Epithet``, ``Taxon Rank`` and
    ``Scientific Name Authorship`` to represent the
    individual elements of the complete ``Scientific Name``.
    It can be used to indicate the subgenus placement of a
    species, which in zoology is often given in parentheses.
    Can also be used to share infrageneric names such as
    botanical sections (e.g., `Vicia sect. Cracca`).
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/infragenericEpithet"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class SpecificEpithet(Field):
    """
    The name of the first or species epithet of the Scientific Name.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/specificEpithet"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class InfraspecificEpithet(Field):
    """
    The name of the lowest or terminal infraspecific epithet of the Scientific Name, excluding any rank designation.

    In botany, name strings in literature and identifications may
    have multiple infraspecific ranks. According to the International
    Code of Nomenclature for algae, fungi, and plants (Schenzhen
    Code Articles 6.7 & Art. 24.1), valid names only have two epithets,
    with the lowest rank being the ``Infraspecific Epithet``. For
    example: the ``Infraspecific Epithet`` in the string `Indigofera
    charlieriana subsp. sessilis var. scaberrima is scaberrima` and
    the ``Scientific Name`` is `Indigofera charlieriana var. scaberrima
    (Schinz) J.B.Gillett.` Use ``Verbatim Identification`` for the
    full name string used in an Identification.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/infraspecificEpithet"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class CultivarEpithet(Field):
    """
    Part of the name of a cultivar, cultivar group or grex that follows the Scientific Name.

    According to the Rules of the Cultivated Plant Code, a cultivar
    name consists of a botanical name followed by a cultivar epithet.
    The value given as the ``Cultivar Epithet`` should exclude any
    quotes. The term ``Taxon Rank`` should be used to indicate which
    type of cultivated plant name (e.g. cultivar, cultivar group,
    grex) is concerned. This epithet, including any enclosing
    apostrophes or suffix, should be provided in ``Scientific Name``
    as well.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/cultivarEpithet"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class TaxonRank(Field):
    """
    The taxonomic rank of the most specific name in the Scientific Name.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/taxonRank"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class VerbatimTaxonRank(Field):
    """
    The taxonomic rank of the most specific name in the Scientific Name as it appears in the original record.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/verbatimTaxonRank"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class ScientificNameAuthorship(Field):
    """
    The authorship information for the Scientific Name formatted.

    Name formatted according to the conventions of
    the applicable ``Nomenclatural Code``.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/scientificNameAuthorship"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class VernacularName(Field):
    """
    A common or vernacular name.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/vernacularName"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return


class NomenclaturalCode(Field):
    """
    The nomenclatural code (or codes in the case of an ambiregnal name) under which the Scientific Name is constructed.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/nomenclaturalCode"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class TaxonomicStatus(Field):
    """
    The status of the use of the Scientific Name as a label for a taxon.

    Requires taxonomic opinion to define the
    scope of a Taxon. Rules of priority then
    are used to define the taxonomic status
    of the nomenclature contained in that
    scope, combined with the experts' opinion.
    It must be linked to a specific taxonomic
    reference that defines the concept.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/taxonomicStatus"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class NomenclaturalStatus(Field):
    """
    The status related to the original publication of the name.

    The status related to the original publication
    of the name and its conformance to the relevant
    rules of nomenclature. It is based essentially
    on an algorithm according to the business rules
    of the code. It requires no taxonomic opinion.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    vocabulary: str, optional
        An URI for a vocabulary that the source values for this Field are based on.
    """
    URI = "http://rs.tdwg.org/dwc/terms/nomenclaturalStatus"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, vocabulary: str = None) -> None:
        super().__init__(index, default, vocabulary)
        return


class TaxonRemarks(Field):
    """
    Comments or notes about the taxon or name.
    
    Parameters
    ----------
    index : int | str
        Specifies the position of the column in the row.
    default: TYPE, optional
        Specifies a value to use if one is not supplied.
    """
    URI = "http://rs.tdwg.org/dwc/terms/taxonRemarks"
    TYPE = str

    def __init__(self, index: int | str, default: TYPE = None, **kwargs) -> None:
        super().__init__(index, default, None)
        return
