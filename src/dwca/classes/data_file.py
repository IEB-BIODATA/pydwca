from __future__ import annotations

import os
import shutil
import sys
import tempfile
import warnings
from abc import ABC
from copy import deepcopy
from enum import Enum
from typing import List, Dict, Type, Tuple, BinaryIO, Generator, Any
from warnings import warn

from lxml import etree as et

from dwca.terms import Field, DWCType, DWCModified, DWCLanguage, DWCLicense, DWCRightsHolder, DWCAccessRights, \
    DWCBibliographicCitation, DWCReferences, DWCInstitution, DWCCollection, DWCDataset, DWCInstitutionCode, \
    DWCCollectionCode, DWCDatasetName, DWCOwnerInstitutionCode, DWCBasisOfRecord, DWCInformationWithheld, \
    DWCDataGeneralizations, DWCDynamicProperties, OutsideTerm, DWCSource
from xml_common import XMLObject
from xml_common.utils import iterate_with_bar, type_to_pl, format_to_sql

try:
    import pandas as pd
except Exception:
    pd = None
try:
    import polars as pl
except Exception:
    pl = None


class DataFileType(Enum):
    """
    Type of data file in the Darwin Core Archive.
    """
    CORE = 0
    EXTENSION = 1


class DataFile(XMLObject, ABC):
    """
    Abstract class representing the class of data represented by each row in a data entity.

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
        Number of lines to ignore at the start of document. Default 0 lines.
    """
    URI = "http://rs.tdwg.org/dwc/terms/"
    """str: Unified Resource Identifier (URI) for the term identifying the class of data."""
    __field_class__ = [
        DWCType, DWCModified, DWCLanguage, DWCLicense, DWCRightsHolder,
        DWCAccessRights, DWCBibliographicCitation, DWCReferences,
        DWCInstitution, DWCCollection, DWCDataset, DWCInstitutionCode,
        DWCCollectionCode, DWCDatasetName, DWCOwnerInstitutionCode,
        DWCBasisOfRecord, DWCInformationWithheld, DWCDataGeneralizations,
        DWCDynamicProperties, DWCSource
    ]

    class Entry:
        def __init__(self, **kwargs) -> None:
            for key, value in kwargs.items():
                setattr(self, key, value)
            return

        def to_dict(self) -> Dict:
            return self.__dict__

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
        super().__init__()
        self.__id__ = _id
        self.__files__ = files
        self.__type__ = data_file_type
        self.__fields__ = fields
        self.__check_fields__()
        self.__encoding__ = encoding
        self.__lines_end__ = lines_terminated_by
        self.__fields_end__ = fields_terminated_by
        self.__fields_enclosed__ = fields_enclosed_by
        self.__ignore_header_lines__ = ignore_header_lines
        self.PRINCIPAL_TAG = self.__type__.name.lower()
        self.__entries__: List[DataFile.Entry] = list()
        self.__data__ = None
        self.__lazy__ = False
        self.__temp_file__ = ""
        self.__sql__ = ""
        self.__primary_key__ = None
        self.__core_field__ = self.__type__ == DataFileType.CORE
        self.__observers__: List[Tuple[int, DarwinCoreArchive]] = list()
        return

    @property
    def id(self) -> int:
        """int: Column to be identified as primary key"""
        return self.__id__

    @property
    def uri(self) -> str:
        """str: Unified Resource Identifier (URI) for the term."""
        return self.URI

    @property
    def filename(self) -> str:
        """str: Filename of the Data File entity."""
        return self.__files__

    def is_lazy(self) -> bool:
        """
        Check if data file load its data as a Lazy Frame.

        Returns
        -------
        bool
            True when file read as a Lazy Frame, False otherwise.
        """
        return self.__lazy__

    @property
    def fields(self) -> List[str]:
        """List[str]: List of terms of this data file."""
        return [field.uri for field in self.__fields__]

    @property
    def name(self) -> str:
        """str: The name of the field."""
        names = self.uri.split("/")
        if len(names) > 1:
            return names[-1]
        else:
            return names[0]

    def add_field(self, field: Field) -> None:
        """
        Add a field to this Data File.

        Parameters
        ----------
        field : Field
            A :class:`dwca.terms.field.Field` object.

        Returns
        -------
        None
        """
        if field.index != len(self.__fields__):
            warn(f"Field must be added at the end of current data, setting index to {len(self.__fields__)}")
            field.index = len(self.__fields__)
        field.__namespace__ = self.__namespace__
        self.__fields__.append(field)
        if self.is_lazy():
            self.__data__ = self.__data__.with_columns(
                pl.lit(
                    None if field.default is None else field.default
                ).alias(field.name)
            )
        elif len(self.__entries__) > 0:
            self.__data__ = None
            for entry in self.__entries__:
                setattr(entry, field.name, None if field.default is None else field.default)
        return

    @property
    def pandas(self) -> pd.DataFrame:
        """pandas.DataFrame: Data of this DataFile as pandas.DataFrame."""
        if self.__data__ is None:
            self.as_pandas()
        return self.__data__

    @pandas.setter
    def pandas(self, df: pd.DataFrame) -> None:
        assert len(self.__data__.columns) == len(df.columns)
        self.__data__ = df
        self.__entries__.clear()
        for _, row in df.iterrows():
            self.__entries__.append(DataFile.Entry(**row.to_dict()))
        for i, observer in self.__observers__:
            if self.__type__ == DataFileType.CORE:
                observer.core = self
            else:  # self.__type__ == DataFileType.EXTENSION
                observer.extensions[i] = self
        return

    @property
    def polars(self) -> pl.DataFrame:
        """polars.DataFrame: Data of this DataFile as polars.DataFrame."""
        if self.__data__ is None or self.is_lazy():
            self.as_polars()
        return self.__data__

    @property
    def sql_table(self) -> str:
        """str: Data file as CREATE TABLE sql statement."""
        if len(self.__sql__) == 0:
            self.generate_sql_table()
        return self.__sql__

    @property
    def insert_sql(self) -> Generator[str, Tuple[Any]]:
        """
        Generate the INSERT INTO sql statement and the values to be inserted.
        """
        if self.__type__ == DataFileType.EXTENSION and not self.__core_field__:
            raise RuntimeError("`set_core_field` must be called before `insert_sql` in Extension DataFile.")
        statement = f"INSERT INTO \"{self.name}\" (\n"
        columns = list()
        types = list()
        for i, field in enumerate(self.__fields__):
            columns.append(f"\"{field.name}\"")
            types.append("%s")
        statement += ",\n".join(columns)
        statement += "\n) VALUES ("
        statement += ", ".join(types)
        statement += ")\n"
        if self.is_lazy():
            for i in range(len(self)):
                tmp = self.__data__.slice(i, 1).collect()
                yield statement, tuple([
                    format_to_sql(tmp.select(field.name).item(), field.TYPE)
                    for field in self.__fields__
                ])
                del tmp
        for entry in self.__entries__:
            yield statement, tuple([
                format_to_sql(getattr(entry, field.name), field.TYPE)
                for field in self.__fields__
            ])

    def _register_darwin_core_(self, _on: int, dwca: DarwinCoreArchive) -> None:
        self.__observers__.append((_on, dwca))
        return

    def __len__(self) -> int:
        if self.__data__ is not None:
            try:
                return len(self.__data__)
            except TypeError:
                return self.__data__.select(pl.len()).collect().item() - self.__ignore_header_lines__
        else:
            return len(self.__entries__)

    @classmethod
    def get_term_class(cls, element: et.Element) -> Type[Field]:
        """
        Extract the Python ``class`` term from an XML element instance.

        Parameters
        ----------
        element : lxml.etree.Element
            XML element instance.

        Returns
        -------
        Type[Field]
            The Python ``class`` representing the term name.
        """
        for field_class in cls.__field_class__:
            if element.get("term") == field_class.URI:
                return field_class
        warn(f"{element.get('term')} not in expected namespace for "
             f"{cls.URI} class. "
             f"Some functionalities may not be available.")
        return OutsideTerm

    @classmethod
    def parse_kwargs(cls, element: et.Element, nmap: Dict) -> Dict:
        """
        Parse an `lxml.etree.Element` into the DataFile parameters.

        Parameters
        ----------
        element : `lxml.etree.Element`
            An XML `Element`.
        nmap : Dict
            Dictionary of prefix:uri.

        Returns
        -------
        Dict
            The Parameters of any DataFile.
        """
        fields = list()
        for field_tree in element.findall("field", namespaces=nmap):
            try:
                fields.append(cls.get_term_class(field_tree).parse(field_tree, nmap))
            except TypeError as e:
                warn(f"Error on field {et.tostring(field_tree)}: {e}", category=SyntaxWarning)
                pass
        assert len(fields) >= 1, "A Data File must contain at least one field"
        df_type = DataFileType[et.QName(element).localname.upper()]
        if df_type == DataFileType.CORE:
            element_id = element.find("id", nmap)
        else:  # df_type == DataFileType.EXTENSION:
            element_id = element.find("coreid", nmap)
        _id = int(element_id.get("index"))
        fields_enclosed_by = element.get("fieldsEnclosedBy", "")
        return {
            "_id": _id,
            "files": element.find("files", namespaces=nmap).find("location", namespaces=nmap).text,
            "fields": fields,
            "data_file_type": df_type,
            "encoding": element.get("encoding", "utf-8"),
            "lines_terminated_by": cls.__format_escape__(element.get("linesTerminatedBy", "\n")),
            "fields_terminated_by": cls.__format_escape__(element.get("fieldsTerminatedBy", ",")),
            "fields_enclosed_by": element.get("fieldsEnclosedBy", ""),
            "ignore_header_lines": int(element.get("ignoreHeaderLines", 0)),
        }

    @staticmethod
    def __format_escape__(characters: str) -> str:
        return characters.replace(
            "\\n", "\n"
        ).replace(
            "\\r", "\r"
        ).replace(
            "\\t", "\t"
        )

    @staticmethod
    def __unformat_escape__(characters: str) -> str:
        return characters.replace(
            "\n", "\\n"
        ).replace(
            "\r", "\\r"
        ).replace(
            "\t", "\\t"
        )

    @classmethod
    def parse(cls, element: et.Element, nmap: Dict) -> DataFile | None:
        """
        Parse an `lxml.etree.Element` into a concrete DataFile object.

        Parameters
        ----------
        element : `lxml.etree.Element`
            An XML `Element`.
        nmap : Dict
            Dictionary of prefix:uri.

        Returns
        -------
        DataFile
            An instance of a concrete DataFile class.
        """
        if element is None:
            return None
        kwargs = cls.parse_kwargs(element, nmap)
        data_file = cls(**kwargs)
        data_file.__namespace__ = nmap
        return data_file

    def to_element(self) -> et.Element:
        """
        Generate a XML `Element` instance

        Returns
        -------
        `lxml.etree.Element`
            XML `Element` instance
        """
        element = super().to_element()
        element.set("rowType", self.uri)
        element.set("encoding", self.__encoding__)
        element.set("linesTerminatedBy", self.__unformat_escape__(self.__lines_end__))
        element.set("fieldsTerminatedBy", self.__unformat_escape__(self.__fields_end__))
        element.set("fieldsEnclosedBy", self.__fields_enclosed__)
        element.set("ignoreHeaderLines", str(self.__ignore_header_lines__))
        if self.__type__ == DataFileType.CORE:
            element_id = self.object_to_element("id")
        else:  # self.__type__ == DataFileType.EXTENSION:
            element_id = self.object_to_element("coreid")
        element_id.set("index", str(self.id))
        element.append(element_id)
        files = self.object_to_element("files")
        location = self.object_to_element("location")
        location.text = self.filename
        files.append(location)
        element.append(files)
        for field in self.__fields__:
            if self.__type__ == DataFileType.EXTENSION and field.index == self.id:
                continue
            field_element = field.to_element()
            element.append(field_element)
        return element

    @classmethod
    def check_principal_tag(cls, tag: str, nmap: Dict) -> None:
        """
        Overwrite due to different possible tags.

        Parameters
        ----------
        tag : str
            Actual tag.
        nmap : Dict
            Namespace.
        """
        pass

    def __check_fields__(self) -> None:
        extension = self.__type__ == DataFileType.EXTENSION
        ordered_fields: List[Field] = [None] * (len(self.__fields__) + extension)
        for field in self.__fields__:
            try:
                if ordered_fields[field.index] is not None:
                    raise AssertionError(f'"index={field.index}" declared twice.')
                ordered_fields[field.index] = field
            except IndexError:
                pass
        if extension:
            if ordered_fields[self.id] is None:
                ordered_fields[self.id] = OutsideTerm(self.id, "")
            else:
                ordered_fields.pop()
        nones = [str(i) for i, item in enumerate(ordered_fields) if item is None]
        if len(nones) > 0:
            raise AssertionError(f'Index {"".join(nones)} not declared.')
        self.__fields__ = ordered_fields
        return

    def read_file(self, content: str, source_file: BinaryIO = None, lazy: bool = False, _no_interaction: bool = False) -> None:
        """
        Read the content of the file specified in `files` parameters (:meth:`filename`).

        Parameters
        ----------
        content : str
            Content of the file
        source_file : BinaryIO, optional
            File to read in case of laziness.
        lazy : bool, optional
            Read the file in lazy evaluation mode. Default `False`.
        _no_interaction : bool, optional
            Not to show progress bar if library `tqdm` is installed. Default `False`.
        """
        if lazy:
            try:
                import polars as pl
                with tempfile.NamedTemporaryFile(delete=False) as file:
                    shutil.copyfileobj(source_file, file)
                    self.__data__ = pl.scan_csv(
                        file.name,
                        has_header=False,
                        skip_rows=self.__ignore_header_lines__,
                        separator=self.__fields_end__,
                        quote_char=None,
                        schema={field.name: type_to_pl(field.TYPE, lazy=True) for field in self.__fields__},
                        encoding=self.__encoding__.lower().replace("-", ""),
                    )
                    self.__lazy__ = True
                    self.__temp_file__ = file.name
                    warn("Reading in lazy evaluation mode generates a temporal file, make sure to call close() to "
                         "delete it")
            except ImportError:
                raise ImportError("Cannot read lazy without polars installed.")
        else:
            lines = content.split(self.__lines_end__)
            lines = list(filter(lambda x: x != "", lines))
            if not _no_interaction:
                iterator = iterate_with_bar(
                    lines[self.__ignore_header_lines__:],
                    desc=f"Reading file {self.filename}", unit="entry"
                )
            else:
                iterator = lines[self.__ignore_header_lines__:]
            for line in iterator:
                kwargs = dict()
                for field, value in zip(self.__fields__, line.split(self.__fields_end__)):
                    kwargs[field.name] = field.format(value)
                self.__entries__.append(DataFile.Entry(**kwargs))
        return


    def write_file(self, _no_interaction: bool = False) -> str:
        """
        Write the content as a text using format information on this object.

        Returns
        -------
        str
            Data File as plain text.
        """
        output_file = ""
        if self.__ignore_header_lines__ > 0:
            output_file += f"###{self.__lines_end__}" * (self.__ignore_header_lines__ - 1)
            header = [field.name for field in self.__fields__]
            output_file += f"{self.__fields_end__}".join(header) + self.__lines_end__
        if not _no_interaction:
            iterator = iterate_with_bar(self.__entries__, desc=f"Writing data {self.uri}", unit="line")
        else:
            iterator = self.__entries__
        for entry in iterator:
            line = list()
            for field in self.__fields__:
                try:
                    line.append(field.unformat(getattr(entry, field.name)))
                except AssertionError:  # In case the type got lost in pandas
                    # TODO: field.TYPE will not work for Typing package
                    line.append(field.unformat(field.TYPE(getattr(entry, field.name))))
                except Exception as e:
                    print(f"Error on {field.name} with value {getattr(entry, field.name)}", file=sys.stderr)
                    raise e
            output_file += f"{self.__fields_end__}".join(line) + self.__lines_end__
        return output_file

    def as_pandas(self, _no_interaction: bool = False) -> pd.DataFrame:
        """
        Convert information in this DataFile in a pandas.DataFrame.

        Returns
        -------
        DataFrame
            Information as a pandas.DataFrame.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("Install pandas to use this feature.")
        fields = list()
        for field in self.__fields__:
            fields.append(field.name)
        entries = list()
        if _no_interaction:
            for entry in self.__entries__:
                entries.append(entry.to_dict())
        else:
            for entry in iterate_with_bar(self.__entries__, desc="Converting to pandas", unit="entry"):
                entries.append(entry.to_dict())
        self.__data__ = pd.DataFrame(entries, columns=fields)
        return self.__data__

    def as_polars(self, _no_interaction: bool = False) -> pl.DataFrame:
        """
        Convert information in this DataFile in a polars DataFrame.

        Returns
        -------
        DataFrame:
            Information as a polars.DataFrame.
        """
        try:
            import polars as pl
        except ImportError:
            raise ImportError("Install polars to use this feature.")
        if self.is_lazy():
            self.__data__ = self.__data__.collect()
            self.__lazy__ = False
            self.close()
            return self.__data__
        else:
            fields = list()
            for field in self.__fields__:
                fields.append((field.name, type_to_pl(field.TYPE)))
            entries = list()
            if _no_interaction:
                for entry in self.__entries__:
                    entries.append(entry.to_dict())
            else:
                for entry in iterate_with_bar(self.__entries__, desc="Converting to polars", unit="entry"):
                    entries.append(entry.to_dict())
            self.__data__ = pl.DataFrame(entries, schema=fields)
            return self.__data__

    def set_core_field(self, field: Field) -> None:
        """
        Set the Core field in an Extension DataFile.

        Parameters
        ----------
        field : Field
            Primary Key from the Core DataFile.

        Returns
        -------
        None
        """
        if self.__type__ == DataFileType.CORE:
            raise AttributeError(f"Core DataField cannot change primary field.")
        self.__fields__[self.id] = field
        self.__fields__[self.id].__index__ = self.id
        self.__core_field__ = True
        return

    def set_primary_key(self, primary_key: str) -> None:
        """
        Set the primary key in an Extension DataFile to be referenced on the new SQL table.

        Parameters
        ----------
        primary_key : str
            Name of the Core Data File.

        Returns
        -------
        None
        """
        if self.__type__ == DataFileType.CORE:
            raise AttributeError(f"Core DataField cannot be set the primary key.")
        self.__primary_key__ = primary_key
        return

    def generate_sql_table(self) -> str:
        """
        Generate the CREATE TABLE statement for SQL database.

        Returns
        -------
        str
            CREATE TABLE statement.
        """
        if self.__type__ == DataFileType.EXTENSION and self.__primary_key__ is None:
            raise RuntimeError("`set_primary_key` must be called before `generate_sql_table` in Extension DataFile.")
        sql_columns = ""
        for field in self.__fields__:
            sql_columns += f"\"{field.name}\" {field.sql_type},\n"
        primary_key = self.__fields__[self.id].name
        if primary_key == "":
            raise RuntimeError("Primary key cannot be empty, in case of Extension, called `set_core_field` first.")
        foreign_key = ""
        if self.__type__ == DataFileType.EXTENSION:
            foreign_key = f""",
            FOREIGN KEY ("{primary_key}") REFERENCES \"{self.__primary_key__}\""""
        # TODO: Fix foreign key is not necessary primary key
        self.__sql__ = f"""CREATE TABLE "{self.name}" (
            {sql_columns}
            PRIMARY KEY ("{primary_key}"){foreign_key}
        );"""
        return self.__sql__

    def merge(self, data_file: DataFile) -> DataFile:
        assert self.uri == data_file.uri, "Cannot merge two different classes: `{}` and `{}`".format(
            self.uri, data_file.uri
        )
        merged = deepcopy(self)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            for field in data_file.__fields__:
                if field.uri not in merged.fields:
                    merged.add_field(field)
        try:
            data = merged.pandas
            merged.pandas = pd.concat([data, data_file.pandas], axis=0).reset_index(drop=True)
        except ImportError:
            for entry in data_file.__entries__:
                merged.__entries__.append(entry)
            for i, entry in enumerate(merged.__entries__):
                for field in merged.__fields__:
                    try:
                        getattr(entry, field.name)
                    except AttributeError:
                        setattr(merged.__entries__[i], field.name, field.default)
        return merged

    def close(self) -> None:
        if self.is_lazy():
            os.remove(self.__temp_file__)
            self.__temp_file__ = ""
            self.__lazy__ = False
        return

    def __str__(self) -> str:
        role = self.__type__.name.lower().capitalize()
        return (f"{role}:"
                f"\n\tclass: {self.uri}"
                f"\n\tfilename: {self.filename}"
                f"\n\tcontent: {self.__len__()} entries")
