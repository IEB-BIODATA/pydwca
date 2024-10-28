from typing import Iterable, TypeVar

T = TypeVar('T')


def is_notebook() -> bool:
    """
    Check if it is running in a terminal or in a notebook (or interactive Python).

    Returns
    -------
    bool
        True if it is running in an IPython, False otherwise.
    """
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except ImportError:
        return False


def get_optional_iterator(**kwargs) -> T:
    """
    Get optional bar progress with or without iterator.

    Parameters
    ----------
    See tqdm documentation.

    Returns
    -------
    tqdm
        Instance of tqdm in case library is installed.

    See Also
    --------
    tqdm : https://tqdm.github.io/docs/tqdm/#tqdm-objects
    """
    iterator = kwargs.pop("iterator", None)
    if is_notebook():
        try:
            from tqdm.notebook import tqdm
            if iterator is None:
                return tqdm(**kwargs)
            else:
                return tqdm(iterator, **kwargs)
        except ImportError:
            return iterator
    else:
        try:
            from tqdm import tqdm
            if iterator is None:
                return tqdm(**kwargs)
            else:
                return tqdm(iterator, **kwargs)
        except ImportError:
            return iterator


def iterate_with_bar(iterator: Iterable[T], **kwargs) -> T:
    """
    Get a tqdm instance iterator or just the iterator.

    Parameters
    ----------
    iterator : Iterable
        Python object to be iterated.

    Other Parameters
    ----------------
    See tqdm documentation.

    Returns
    -------
    tqdm
        Instance of tqdm in case library is installed.

    See Also
    --------
    tqdm : https://tqdm.github.io/docs/tqdm/#tqdm-objects
    """
    return get_optional_iterator(iterator = iterator, **kwargs)


class OptionalTqdm:
    """
    Optional TQDM progress bar. Support all method in case tqdm is not installed.
    """
    def __init__(self, **kwargs) -> None:
        self.__tqdm__ = get_optional_iterator(**kwargs)
        return

    def set_descriptor(self, **kwargs) -> None:
        """
        Set descriptor for tqdm progress bar.

        Other Parameters
        ----------------
        See tqdm documentation.

        See Also
        --------
        tqdm : https://tqdm.github.io/docs/tqdm/#set_description
        """
        if self.__tqdm__ is not None:
            self.__tqdm__.set_description(**kwargs)
        return

    def update(self, **kwargs) -> None:
        """
        Update tqdm progress bar.

        Other Parameters
        ----------------
        See tqdm documentation.

        See Also
        --------
        tqdm : https://tqdm.github.io/docs/tqdm/#update
        """
        if self.__tqdm__ is not None:
            self.__tqdm__.update(**kwargs)
        return

    def close(self) -> None:
        """
        Close tqdm progress bar.

        Other Parameters
        ----------------
        See tqdm documentation.

        See Also
        --------
        tqdm : https://tqdm.github.io/docs/tqdm/#close
        """
        if self.__tqdm__ is not None:
            self.__tqdm__.close()
        return

    def set_postfix(self, **kwargs) -> None:
        """
        Set postfix for tqdm progress bar.

        Other Parameters
        ----------------
        See tqdm documentation.

        See Also
        --------
        tqdm : https://tqdm.github.io/docs/tqdm/#set_postfix
        """
        if self.__tqdm__ is not None:
            self.__tqdm__.set_postfix(**kwargs)
        return

    def reset(self, **kwargs) -> None:
        """
        Reset tqdm progress bar.

        Other Parameters
        ----------------
        See tqdm documentation.

        See Also
        --------
        tqdm : https://tqdm.github.io/docs/tqdm/#reset
        """
        if self.__tqdm__ is not None:
            self.__tqdm__.reset(**kwargs)
        return
