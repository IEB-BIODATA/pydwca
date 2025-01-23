def read_string(content: str | bytes, encoding: str = "utf-8") -> str:
    """
    Read a string or a byte into string.

    Parameters
    ----------
    content : str | bytes
        Content as a string or byte.
    encoding : str, optional
        Encoding of the content.

    Returns
    -------
    str
        Content as string.
    """
    try:
        return content.decode(encoding=encoding)
    except AttributeError:
        return content
