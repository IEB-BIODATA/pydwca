from __future__ import annotations

import re
from typing import List, Type

from dwca.classes import DataFile, DataFileType
from dwca.terms import Field, TaxonID, ScientificNameID, AcceptedNameUsageID, ParentNameUsageID, OriginalNameUsageID, \
    NameAccordingToID, NamePublishedInID, TaxonConceptID, ScientificName, AcceptedNameUsage, ParentNameUsage, \
    OriginalNameUsage, NameAccordingTo, NamePublishedIn, NamePublishedInYear, HigherClassification, Kingdom, Phylum, \
    DWCClass, Order, Superfamily, Family, Subfamily, Tribe, Subtribe, Genus, GenericName, Subgenus, \
    InfragenericEpithet, SpecificEpithet, InfraspecificEpithet, CultivarEpithet, TaxonRank, VerbatimTaxonRank, \
    ScientificNameAuthorship, VernacularName, NomenclaturalCode, TaxonomicStatus, NomenclaturalStatus, TaxonRemarks

try:
    import pandas as pd
except ImportError:
    pd = None


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

    def __filter_by_taxa__(self, taxa_field: Type[Field], taxa_name: str, taxa: List[str]) -> None:
        assert taxa_field.URI in self.fields, f"{taxa_name} must be in fields of this class to use this feature."
        complete_taxa = set(taxa)
        try:
            df = self.pandas
            taxa_id = df.loc[
                df[(df[ScientificName.name()].isin(taxa)) & (df[TaxonRank.name()].str.lower() == taxa_name.lower())].index,
                TaxonID.name()
            ]
            for taxon in taxa_id:
                complete_taxa.update(self.all_synonyms(taxon, get_names=True))
            parents = set()
            for taxon in taxa_id:
                parents.update(self.get_parents(taxon))
            name = taxa_field.name()
            df = df[df[name].isin(complete_taxa) | df[TaxonID.name()].isin(parents)]
            self.pandas = df
        except ImportError:
            taxa_id = [
                getattr(
                    self.__get_entry__(**{
                        ScientificName.name(): taxon,
                        f"{TaxonRank.name()}__case_insensitive": taxa_name
                    }), TaxonID.name()
                ) for taxon in taxa
            ]
            for taxon in taxa_id:
                complete_taxa.update(self.all_synonyms(taxon, get_names=True))
            parents = set()
            for taxon in taxa_id:
                parents.update(self.get_parents(taxon))

            def filter_taxa(entry: DataFile.Entry) -> bool:
                return getattr(entry, taxa_field.name()) in complete_taxa or getattr(entry, TaxonID.name()) in parents

            self.__entries__ = list(filter(filter_taxa, self.__entries__))
        return

    def filter_by_kingdom(self, kingdoms: List[str]) -> None:
        """
        Filter data by a valid kingdoms.

        Parameters
        ----------
        kingdoms : List[str]
            Kingdom names to filter data.

        Returns
        -------
        None
        """
        return self.__filter_by_taxa__(Kingdom, "Kingdom", kingdoms)

    def filter_by_phylum(self, phyla: List[str]) -> None:
        """
        Filter data by a valid phylum.

        Parameters
        ----------
        phyla : List[str]
            Phylum names to filter data.

        Returns
        -------
        None
        """
        return self.__filter_by_taxa__(Phylum, "Phylum", phyla)

    def filter_by_class(self, classes: List[str]) -> None:
        """
        Filter data by a valid class.

        Parameters
        ----------
        classes : List[str]
            Class names to filter data.

        Returns
        -------
        None
        """
        return self.__filter_by_taxa__(DWCClass, "Class", classes)

    def get_parents(self, taxa_id: str) -> List[str]:
        """
        Get a list of taxa ids of the parent of the taxa.

        Parameters
        ----------
        taxa_id : str
            A :class:`dwca.terms.taxon.TaxonID` to look for parents.

        Returns
        -------
        List[str]
            List of taxa ids.
        """
        parent_taxa = list()
        try:
            df = self.pandas
            current_taxa = df[df[TaxonID.name()] == taxa_id]
            if len(current_taxa) != 1:
                raise ValueError(f"{taxa_id} not found in data file.")
            while len(current_taxa) == 1:
                new_parent_found = current_taxa[ParentNameUsageID.name()].iloc[0]
                if pd.notna(new_parent_found) and new_parent_found != "":
                    parent_taxa.append(new_parent_found)
                current_taxa = df[df[TaxonID.name()] == new_parent_found]
        except ImportError:
            entry = self.__get_entry__(**{TaxonID.name(): taxa_id})
            if entry is None:
                raise ValueError(f"{taxa_id} not found in data file.")
            current = entry
            while current is not None:
                new_parent_found = getattr(current, ParentNameUsageID.name())
                if new_parent_found is not None and new_parent_found != "":
                    parent_taxa.append(new_parent_found)
                current = self.__get_entry__(**{TaxonID.name(): new_parent_found})
        return parent_taxa

    def all_synonyms(self, taxa_id: str, get_names: bool = False) -> List[str]:
        """
        Get a list of all valid names of a taxon.

        Parameters
        ----------
        taxa_id : str
            A :class:`dwca.terms.taxon.TaxonID` value.
        get_names : bool
            Whether to get :class:`dwca.terms.taxon.ScientificName` or :class:`dwca.terms.taxon.TaxonID`.

        Returns
        -------
        List[str]
            A list of :class:`dwca.terms.taxon.TaxonID`.
        """
        try:
            df = self.pandas
            current_taxa = df[df[TaxonID.name()] == taxa_id]
            if len(current_taxa) != 1:
                raise ValueError(f"{taxa_id} not found in data file.")
            accepted_name = current_taxa.iloc[0][AcceptedNameUsageID.name()]
            return list(
                df[df[AcceptedNameUsageID.name()] == accepted_name][
                    ScientificName.name() if get_names else TaxonID.name()
                ]
            )
        except ImportError:
            entry = self.__get_entry__(**{TaxonID.name(): taxa_id})
            if entry is None:
                raise ValueError(f"{taxa_id} not found in data file.")
            accepted_name = getattr(entry, AcceptedNameUsageID.name())
            synonyms = self.__get_entries__(**{AcceptedNameUsageID.name(): accepted_name})
            field = ScientificName.name() if get_names else TaxonID.name()
            return [getattr(synonymous, field) for synonymous in synonyms]

    def __get_entry__(self, **kwargs) -> DataFile.Entry | None:
        for candid in self.__entries__:
            found = True
            for key, value in kwargs.items():
                found &= Taxon.__compare__(candid, key, value)
                if not found:
                    break
            if found:
                return candid
        return None

    def __get_entries__(self, **kwargs) -> List[DataFile.Entry]:
        results = list()
        for candid in self.__entries__:
            found = True
            for key, value in kwargs.items():
                found &= Taxon.__compare__(candid, key, value)
                if not found:
                    break
            if found:
                results.append(candid)
        return results

    @staticmethod
    def __compare__(candid: DataFile.Entry, key: str, value: str) -> bool:
        match = re.match(r"(\w+)__case_insensitive$", key)
        if match:
            return getattr(candid, match.group(1)).lower() == value.lower()
        else:
            return getattr(candid, key) == value
