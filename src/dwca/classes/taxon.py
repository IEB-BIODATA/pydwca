from __future__ import annotations

import re
from typing import List, Type, Any, Union, Set, Iterable
from warnings import warn

from dwca.classes import DataFile, DataFileType
from dwca.terms import Field, TaxonID, ScientificNameID, AcceptedNameUsageID, ParentNameUsageID, OriginalNameUsageID, \
    NameAccordingToID, NamePublishedInID, TaxonConceptID, ScientificName, AcceptedNameUsage, ParentNameUsage, \
    OriginalNameUsage, NameAccordingTo, NamePublishedIn, NamePublishedInYear, HigherClassification, Kingdom, Phylum, \
    DWCClass, Order, Superfamily, Family, Subfamily, Tribe, Subtribe, Genus, GenericName, Subgenus, \
    InfragenericEpithet, SpecificEpithet, InfraspecificEpithet, CultivarEpithet, TaxonRank, VerbatimTaxonRank, \
    ScientificNameAuthorship, VernacularName, NomenclaturalCode, TaxonomicStatus, NomenclaturalStatus, TaxonRemarks
from xml_common.utils import OptionalTqdm

try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import polars as pl
except ImportError:
    pl = None


class Taxon(DataFile):
    """
    A group of organisms considered by taxonomists to form a homogeneous unit.

    Parameters
    ----------
    _id : int
        Unique identifier for the core entity.
    files : str
        File location, in the archive, this is inside the `zip` file.
    fields : List[Field]
        A list of the Field (columns) in the Core data entity.
    data_file_type: DataFileType
        The Data File Type in the Darwin Core Archive.
    encoding : str, optional
        Encoding of the file location (`files` parameter), default is "utf-8".
    lines_terminated_by : str, optional
        Delimiter of lines on the file, default `"\\\\n"`.
    fields_terminated_by : str, optional
        Delimiter of the file (cells) on the file, default `","`.
    fields_enclosed_by : str, optional
        Specifies the character used to enclose (mark the start and end of) each field, default empty `""`.
    ignore_header_lines : int, optional
        Ignore headers at the start of document, can be one line or a list of them, default 0 (first line).
    """
    URI = DataFile.URI + "Taxon"
    __field_class__ = DataFile.__field_class__ + [
        TaxonID, ScientificNameID, AcceptedNameUsageID,
        ParentNameUsageID, OriginalNameUsageID,
        NameAccordingToID, NamePublishedInID, TaxonConceptID,
        ScientificName, AcceptedNameUsage, ParentNameUsage,
        OriginalNameUsage, NameAccordingTo, NamePublishedIn,
        NamePublishedInYear, HigherClassification, Kingdom,
        Phylum, DWCClass, Order, Superfamily, Family,
        Subfamily, Tribe, Subtribe, Genus, GenericName,
        Subgenus, InfragenericEpithet, SpecificEpithet,
        InfraspecificEpithet, CultivarEpithet, TaxonRank,
        VerbatimTaxonRank, ScientificNameAuthorship,
        VernacularName, NomenclaturalCode, TaxonomicStatus,
        NomenclaturalStatus, TaxonRemarks,
    ]

    def __init__(
            self, _id: int, files: str,
            fields: List[Field],
            data_file_type: DataFileType = DataFileType.CORE,
            encoding: str = "utf-8",
            lines_terminated_by: str = "\n",
            fields_terminated_by: str = ",",
            fields_enclosed_by: str = "",
            ignore_header_lines: int = 0,
    ) -> None:
        super().__init__(
            _id, files, fields, data_file_type, encoding,
            lines_terminated_by, fields_terminated_by,
            fields_enclosed_by, ignore_header_lines,
        )
        return

    def _filter_by_taxa_(
            self,
            taxa_field: Type[Field],
            taxa_name: str,
            taxa: List[str],
            filter_with_rank: bool = True,
            fuzzy_threshold: float = -1,
    ) -> None:
        assert taxa_field.URI in self.fields, f"{taxa_name} must be in fields of this class to use this feature."
        tqdm = OptionalTqdm(total=100)
        tqdm.set_descriptor(desc="Getting Taxon ID")
        if fuzzy_threshold > 0:
            try:
                from rapidfuzz import process
            except ImportError:
                raise ImportError("Install rapidfuzz to use this feature.")
        try:
            df = self.pandas
            if fuzzy_threshold < 0:
                mask = df[ScientificName.name_cls()].isin(taxa)
            else:
                tqdm.reset(total=len(df))
                def process_with_bar(x: str) -> float:
                    tqdm.update()
                    return process.extractOne(x, taxa)[1]
                matches = df[ScientificName.name_cls()].apply(process_with_bar)
                mask = matches >= fuzzy_threshold
            if filter_with_rank:
                mask &= df[TaxonRank.name_cls()].str.lower() == taxa_name.lower()
            taxa_id = df[mask][TaxonID.name_cls()]
        except ImportError:
            tqdm.reset(total=len(taxa))
            taxa_id = list()
            if filter_with_rank:
                for taxon in taxa:
                    taxon_found = self.__get_entry__(**{
                        ScientificName.name_cls(): taxon,
                        f"{TaxonRank.name_cls()}__case_insensitive": taxa_name
                    }, fuzzy_threshold=fuzzy_threshold)
                    if taxon_found is not None:
                        taxa_id.append(getattr(taxon_found, TaxonID.name_cls()))
                    tqdm.update()
            else:
                for taxon in taxa:
                    taxon_found = self.__get_entry__(**{ScientificName.name_cls(): taxon}, fuzzy_threshold=fuzzy_threshold)
                    if taxon_found is not None:
                        taxa_id.append(getattr(taxon_found, TaxonID.name_cls()))
                    tqdm.update()
            tqdm.reset(total=100)
        tqdm.update(n=10)
        postfix = {"Exact match found": len(taxa_id)}
        tqdm.set_postfix(ordered_dict=postfix)
        tqdm.set_descriptor(desc="Getting synonyms")
        complete_taxa = self.all_synonyms(taxa_id, get_names=True)
        postfix["Synonyms found"] = len(complete_taxa) - len(taxa_id)
        taxa_id = self.all_synonyms(taxa_id)
        tqdm.set_postfix(ordered_dict=postfix)
        tqdm.update(n=40)
        tqdm.set_descriptor(desc="Getting parents")
        parents = self.get_parents(taxa_id)
        parents.update(self.all_synonyms(parents))
        postfix["Parents found"] = len(parents)
        tqdm.set_postfix(ordered_dict=postfix)
        tqdm.update(n=40)
        tqdm.set_descriptor(desc=f"Filtering {taxa_name}")
        try:
            df = self.pandas
            name = taxa_field.name_cls()
            mask = df[TaxonID.name_cls()].isin(parents) | df[TaxonID.name_cls()].isin(taxa_id)
            if filter_with_rank:
                mask |= df[name].isin(complete_taxa)
            df = df[mask]
            self.pandas = df
        except ImportError:
            if filter_with_rank:
                def filter_taxa(entry: DataFile.Entry) -> bool:
                    return (getattr(entry, taxa_field.name_cls()) in complete_taxa or
                            getattr(entry, TaxonID.name_cls()) in parents or
                            getattr(entry, TaxonID.name_cls()) in taxa_id)
            else:
                def filter_taxa(entry: DataFile.Entry) -> bool:
                    return (getattr(entry, TaxonID.name_cls()) in parents or
                            getattr(entry, TaxonID.name_cls()) in taxa_id)
            self.__entries__ = list(filter(filter_taxa, self.__entries__))
        postfix["Total filtered"] = len(self)
        tqdm.set_postfix(ordered_dict=postfix)
        tqdm.update(n=10)
        tqdm.close()
        return

    def filter_by_kingdom(self, kingdoms: List[str], fuzzy_threshold: float = -1) -> None:
        """
        Filter data by a valid kingdoms.

        Parameters
        ----------
        kingdoms : List[str]
            Kingdom names to filter data.
        fuzzy_threshold : float, optional
            If given any value > 0 it will use Levenshtein Distance with that threshold instead of exact match.
        """
        return self._filter_by_taxa_(Kingdom, "Kingdom", kingdoms, fuzzy_threshold=fuzzy_threshold)

    def filter_by_phylum(self, phyla: List[str], fuzzy_threshold: float = -1) -> None:
        """
        Filter data by a valid phylum.

        Parameters
        ----------
        phyla : List[str]
            Phylum names to filter data.
        fuzzy_threshold : float, optional
            If given any value > 0 it will use Levenshtein Distance with that threshold instead of exact match.
        """
        return self._filter_by_taxa_(Phylum, "Phylum", phyla, fuzzy_threshold=fuzzy_threshold)

    def filter_by_class(self, classes: List[str], fuzzy_threshold: float = -1) -> None:
        """
        Filter data by a valid class.

        Parameters
        ----------
        classes : List[str]
            Class names to filter data.
        fuzzy_threshold : float, optional
            If given any value > 0 it will use Levenshtein Distance with that threshold instead of exact match.
        """
        return self._filter_by_taxa_(DWCClass, "Class", classes, fuzzy_threshold=fuzzy_threshold)

    def filter_by_order(self, orders: List[str], fuzzy_threshold: float = -1) -> None:
        """
        Filter data by a valid order.

        Parameters
        ----------
        orders : List[str]
            Order names to filter data.
        fuzzy_threshold : float, optional
            If given any value > 0 it will use Levenshtein Distance with that threshold instead of exact match.
        """
        return self._filter_by_taxa_(Order, "Order", orders, fuzzy_threshold=fuzzy_threshold)

    def filter_by_family(self, families: List[str], fuzzy_threshold: float = -1) -> None:
        """
        Filter data by a valid family.

        Parameters
        ----------
        families : List[str]
            Family names to filter data.
        fuzzy_threshold : float, optional
            If given any value > 0 it will use Levenshtein Distance with that threshold instead of exact match.
        """
        return self._filter_by_taxa_(Family, "Family", families, fuzzy_threshold=fuzzy_threshold)

    def filter_by_genus(self, genera: List[str], fuzzy_threshold: float = -1) -> None:
        """
        Filter data by a valid genus.

        Parameters
        ----------
        genera : List[str]
            Class names to filter genus.
        fuzzy_threshold : float, optional
            If given any value > 0 it will use Levenshtein Distance with that threshold instead of exact match.
        """
        return self._filter_by_taxa_(Genus, "Genus", genera, fuzzy_threshold=fuzzy_threshold)

    def filter_by_species(self, species: List[str], fuzzy_threshold: float = -1) -> None:
        """
        Filer data by species or any rank taxonomy below (subspecies, variety, form, etc.).

        In contrast with the other `filter_by_` taxonomy methods, this one filter
        the taxonomic data using the scientific name field :class:`dwca.terms.taxon.ScientificName`.

        .. warning:: Because of that, use this method with precautions.
           If a scientific name of a rank above species (genus, order,
           etc...) is used, it could result in unexpected behaviour.

        Parameters
        ----------
        species : List[str]
            Scientific Name of species (or rank below) to filter data.
        fuzzy_threshold : float, optional
            If given any value > 0 it will use Levenshtein Distance with that threshold instead of exact match.
        """
        return self._filter_by_taxa_(ScientificName, "Species", species, filter_with_rank=False, fuzzy_threshold=fuzzy_threshold)

    def get_parents(self, taxa_id: List[str]) -> Set[str]:
        """
        Get a list of taxa ids of the parent of the list taxa id provided.

        Parameters
        ----------
        taxa_id : List[str]
            A list of :class:`dwca.terms.taxon.TaxonID` to look for parents.

        Returns
        -------
        Set[str]
            Set of taxa ids.
        """
        parent_taxa = set()
        try:
            df = self.pandas
            current_taxa = self.__get_rows__(taxa_id)
            while len(current_taxa) > 0:
                new_found_parents = current_taxa[ParentNameUsageID.name_cls()]
                new_found_parents = new_found_parents[
                    pd.notna(new_found_parents) &
                    (new_found_parents != "")
                ]
                parent_taxa.update(list(new_found_parents))
                current_taxa = df[df[TaxonID.name_cls()].isin(new_found_parents)]
        except ImportError:
            entries = self.__get_rows__(taxa_id)
            current_taxa = entries.copy()
            while len(current_taxa) > 0:
                new_found_parents = [getattr(current, ParentNameUsageID.name_cls()) for current in current_taxa]
                new_found_parents = list(filter(
                    lambda current: current != "" and current is not None,
                    new_found_parents
                ))
                parent_taxa.update(new_found_parents)
                current_taxa = self.__get_entries__(**{f"{TaxonID.name_cls()}__isin": new_found_parents})
        return parent_taxa

    def all_synonyms(self, taxa_id: Iterable[str], get_names: bool = False) -> List[str]:
        """
        Get a list of all valid names of a list of taxa.

        Parameters
        ----------
        taxa_id : Iterable[str]
            A list (or iterable) of :class:`dwca.terms.taxon.TaxonID` value.
        get_names : bool
            Whether to get :class:`dwca.terms.taxon.ScientificName` or :class:`dwca.terms.taxon.TaxonID`.

        Returns
        -------
        List[str]
            A list of :class:`dwca.terms.taxon.TaxonID`.
        """
        try:
            df = self.pandas
            current_taxa = self.__get_rows__(taxa_id)
            accepted_names = current_taxa[AcceptedNameUsageID.name_cls()]
            return list(
                df[df[AcceptedNameUsageID.name_cls()].isin(accepted_names)][
                    ScientificName.name_cls() if get_names else TaxonID.name_cls()
                ]
            )
        except ImportError:
            entries = self.__get_rows__(taxa_id)
            accepted_names = [getattr(entry, AcceptedNameUsageID.name_cls()) for entry in entries]
            synonyms = self.__get_entries__(**{f"{AcceptedNameUsageID.name_cls()}__isin": accepted_names})
            field = ScientificName.name_cls() if get_names else TaxonID.name_cls()
            return [getattr(synonymous, field) for synonymous in synonyms]

    def __get_rows__(self, taxa_id: Iterable[str]) -> Union[pd.DataFrame, List[DataFile.Entry]]:
        try:
            df = self.pandas
            current_taxa = df[df[TaxonID.name_cls()].isin(taxa_id)]
            if len(current_taxa) != len(taxa_id):
                candidates = pd.Series(taxa_id)
                not_present = candidates[~candidates.isin(df[TaxonID.name_cls()])]
                warn(f"{', '.join(list(not_present))} not found in data file.", category=RuntimeWarning)
            return current_taxa
        except ImportError:
            entries = self.__get_entries__(**{f"{TaxonID.name_cls()}__isin": taxa_id})
            if len(entries) != len(taxa_id):
                found_taxa = [getattr(entry, TaxonID.name_cls()) for entry in entries]
                not_present = list(filter(lambda candid: candid not in found_taxa, taxa_id))
                warn(f"{', '.join(not_present)} not found in data file.", category=RuntimeWarning)
            return entries

    def __get_entry__(self, fuzzy_threshold: float =-1, **kwargs) -> DataFile.Entry | None:
        for candid in self.__entries__:
            found = True
            for key, value in kwargs.items():
                found &= Taxon.__compare__(candid, key, value, fuzzy_threshold=fuzzy_threshold)
                if not found:
                    break
            if found:
                return candid
        return None

    def __get_entries__(self, fuzzy_threshold: float =-1, **kwargs) -> List[DataFile.Entry]:
        results = list()
        for candid in self.__entries__:
            found = True
            for key, value in kwargs.items():
                found &= Taxon.__compare__(candid, key, value, fuzzy_threshold=fuzzy_threshold)
                if not found:
                    break
            if found:
                results.append(candid)
        return results

    @staticmethod
    def __compare__(candid: DataFile.Entry, key: str, value: Any, fuzzy_threshold: float = -1) -> bool:
        match = re.match(r"(\w+)__case_insensitive$", key)
        if match:
            if fuzzy_threshold > 0:
                from rapidfuzz import fuzz
                ratio = fuzz.ratio(getattr(candid, match.group(1)).lower(), value.lower())
                return ratio >= fuzzy_threshold
            return getattr(candid, match.group(1)).lower() == value.lower()
        match = re.match(r"(\w+)__isin$", key)
        if match:
            if fuzzy_threshold > 0:
                from rapidfuzz import process
                _, ratio = process.extractOne(getattr(candid, match.group(1)), value)
                return ratio >= fuzzy_threshold
            return getattr(candid, match.group(1)) in value
        if fuzzy_threshold > 0:
            from rapidfuzz import fuzz
            ratio = fuzz.ratio(getattr(candid, key), value)
            if getattr(candid, key) == "Rtfkiaicpdng (Abifwvxqn) gurqtwpof f. prczacpvtdtu 'xzhgezqpaorp'":
                import sys
                print(candid, key, value, ratio, file=sys.stderr)
            return ratio >= fuzzy_threshold
        return getattr(candid, key) == value
