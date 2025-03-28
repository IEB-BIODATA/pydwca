import datetime as dt
from datetime import datetime
from typing import TypeAlias, get_args, List, Any, Union, get_origin
from warnings import warn

from datetime_interval import Interval

POSSIBLE_DATETIME_FORMATS = [
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M%z",
    "%Y-%m-%dT%H%z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%dT%H",
    "%Y-%m-%d",
    "%Y-%m",
    "%Y",
]


def format_to_type(value: str, a_type: TypeAlias, address_value: bool = True) -> Any:
    """
    Convert the string value according to the type given.

    Parameters
    ----------
    value : str
        A value to be converted.
    a_type : TypeAlias
        The type to convert the value.
    address_value : bool, optional
        If the conversion gives ValueError, whether return None.

    Returns
    -------
    Any
        The value as a TypeAlias.

    Raises
    ------
    TypeError
        When the Type alias is not supported or value cannot be converted in that particular Type.
    """
    try:
        if a_type == Interval:
            raise TypeError
        return a_type(value)
    except ValueError as e:
        if address_value:
            return None
        else:
            raise e
    except TypeError as e:
        if a_type == List[str]:
            if value is None:
                return None
            return value.split(" | ")
        elif a_type.__name__ == "Tuple":
            return tuple([
                format_to_type(
                    this_value,
                    this_type
                ) for this_value, this_type in zip(
                    value.split("/"),
                    get_args(a_type)
                )
            ])
        elif a_type == Any:
            warn("<Any> type is not recommended as Type of field.")
            return value
        elif a_type == Interval:
            start_value, end_value = value.split("/")
            return Interval(start=format_datetime(start_value), end=format_datetime(end_value))
        elif a_type == dt.datetime:
            return format_datetime(value)
        elif getattr(a_type, "__origin__", None) is Union:
            return format_union(value, a_type)
        else:
            if str(a_type)[0] == "<":
                type_str = str(a_type)
            else:
                type_str = f"<{a_type}>"
            raise TypeError(f"Type {type_str} does not have automatic conversion.")


def format_union(value: str, types: TypeAlias) -> Any:
    """
    Convert the string value to any of the types given inside the union.

    Parameters
    ----------
    value : str
        A value to be converted.
    types : TypeAlias
        A Union Type with various option of types.

    Returns
    -------
    Any
        Value in one of the type listed inside the `types` parameter.

    Raises
    ------
    TypeError
        When the value cannot be converted in any of Types given.
    """
    previous_exception = None
    for a_type in get_args(types):
        try:
            return format_to_type(value, a_type, address_value=False)
        except (TypeError, ValueError) as e:
            e.__cause__ = previous_exception
            previous_exception = e
            continue
    type_str = [f"<{a_type}>" if str(a_type)[0] != "<" else str(a_type) for a_type in get_args(types)]
    exception = TypeError(f"{value} does not match any of {', '.join(type_str)}")
    exception.__cause__ = previous_exception
    raise exception


def format_datetime(value: str) -> dt.datetime | None:
    """
    Convert value in a datetime object.

    Parameters
    ----------
    value : str
        Value to be parsed in a datetime object.

    Returns
    -------
    datatime
        Datetime object from value.
    """
    previous_exception = None
    if value == "" or value is None:
        return
    for dt_format in POSSIBLE_DATETIME_FORMATS:
        try:
            return dt.datetime.strptime(value.strip(), dt_format)
        except ValueError as e:
            e.__cause__ = previous_exception
            previous_exception = e
            continue
    format_string = ", \n".join(POSSIBLE_DATETIME_FORMATS)
    exception = ValueError(f"{value} does not match any of:\n{format_string}")
    exception.__cause__ = previous_exception
    raise exception


def unformat_type(value: Any, a_type: TypeAlias) -> str:
    """
    Convert a value to a string according to the type given.

    Parameters
    ----------
    value : Any
        A value in a_type format.
    a_type : TypeAlias
        The type of the value given.

    Returns
    -------
    str
        Encoded value
    """
    try:
        import pandas as pd
        if pd.isna(value):
            return ""
    except ImportError:
        pass
    except ValueError:
        pass
    if value is None:
        return ""
    if a_type == List[str]:
        assert isinstance(value, list), f"Value must be a list of string"
        return " | ".join([str(v) for v in value])
    elif a_type.__name__ == "Tuple":
        encoded_str = [unformat_type(v, this_type) for v, this_type in zip(value, get_args(a_type))]
        return "/".join(encoded_str)
    else:
        assert isinstance(value, a_type), f"Value must be an instance of {a_type}"
        if a_type == Interval or (Interval in get_args(a_type) and isinstance(value, Interval)):
            return f"{unformat_datetime(value.start)}/{unformat_datetime(value.end)}"
        elif a_type == dt.datetime or (dt.datetime in get_args(a_type) and isinstance(value, dt.datetime)):
            return unformat_datetime(value)
        else:
            return str(value)


def unformat_datetime(value: dt.datetime) -> str:
    """
    Convert a datetime value in an encoded string.

    Parameters
    ----------
    value : datetime
        Value to be encoded as a string.

    Returns
    -------
    str
        Encoded Datetime object.
    """
    if value.tzinfo is None:
        z = ""
    elif value.tzinfo == dt.timezone.utc:
        z = "Z"
    else:
        z = "%z"
    if value.second == 0:
        if value.minute == 0:
            if value.hour == 0:
                if value.day == 1:
                    if value.month == 1:
                        return value.strftime(f"%Y")
                    else:
                        return value.strftime(f"%Y-%m")
                else:
                    return value.strftime(f"%Y-%m-%d")
            else:
                return value.strftime(f"%Y-%m-%dT%H{z}")
        else:
            return value.strftime(f"%Y-%m-%dT%H:%M{z}")
    else:
        return value.strftime(f"%Y-%m-%dT%H:%M:%S{z}")


def type_to_pl(a_type: TypeAlias, lazy: bool = False) -> TypeAlias:
    """
    Equivalent to a_type in the polars dtype.

    Parameters
    ----------
    a_type : TypeAlias
        Any available type.
    lazy : bool
        When used to inference the types in lazy mode.

    Returns
    -------
    TypeAlias
        polars dtype.
    """
    try:
        import polars as pl
    except ImportError:
        raise ImportError("polars not installed.")
    if a_type == str:
        return pl.String
    elif get_origin(a_type) == list:
        if lazy:
            return pl.String
        inner_type = get_args(a_type)
        if len(inner_type) == 1:
            return pl.List(type_to_pl(get_args(a_type)[0]))
        else:
            return pl.List(pl.Object)
    elif a_type == bool:
        return pl.Boolean
    elif a_type == int:
        return pl.Int64
    elif a_type == float:
        return pl.Float64
    elif a_type == dt.datetime:
        return pl.Datetime
    else:
        if lazy:
            return pl.String
        return pl.Object

def type_to_sql(a_type: TypeAlias) -> str:
    """
    Equivalent to a_type in the polars dtype.

    Parameters
    ----------
    a_type : TypeAlias
        Any available type.

    Returns
    -------
    TypeAlias
        polars dtype.
    """
    if a_type == int:
        return "INTEGER"
    elif a_type == float:
        return "REAL"
    elif a_type == str:
        return "VARCHAR"
    elif a_type == bool:
        return "BOOLEAN"
    elif a_type == bytes:
        return "BLOB"
    elif a_type == dt.datetime:
        return "DATETIME"
    else:
        return "VARCHAR"


def format_to_sql(value: Any, a_type: TypeAlias) -> Any:
    """
    Format a value to the SQL equivalent.

    Parameters
    ----------
    value : Any
        Value to be formatted.
    a_type : TypeAlias
        The type of the value.

    Returns
    -------
    Any
        Value formatted.
    """
    given_type = type_to_sql(a_type)
    if value is None:
        return None
    if given_type == "INTEGER":
        return int(value)
    elif given_type =="REAL":
        return float(value)
    elif given_type == "BOOLEAN":
        return bool(value)
    elif given_type == "BLOB":
        if isinstance(value, bytes):
            return value
        elif isinstance(value, str):
            return bytes(value, encoding="ascii")
        else:
            return bytes(value)
    elif given_type == "DATETIME":
        if isinstance(value, str):
            return format_datetime(value)
        elif isinstance(value, dt.datetime):
            return value
        else:
            raise ValueError(f"{type(value)} is not supported to datetime.")
    elif given_type == "VARCHAR":
        return str(value)
    else:
        return str(value)
