from typing import Iterable, TypeVar

T = TypeVar('T')


def iterate_with_bar(iterator: Iterable[T], **kwargs) -> T:
    try:
        from tqdm import tqdm
        return tqdm(iterator, **kwargs)
    except ImportError:
        return iterator


class OptionalTqdm:
    def __init__(self, **kwargs) -> None:
        try:
            from tqdm import tqdm
            self.__tqdm__ = tqdm(**kwargs)
        except ImportError:
            self.__tqdm__ = None
        return

    def set_descriptor(self, **kwargs) -> None:
        if self.__tqdm__ is not None:
            self.__tqdm__.set_description(**kwargs)
        return

    def update(self, **kwargs) -> None:
        if self.__tqdm__ is not None:
            self.__tqdm__.update(**kwargs)
        return

    def close(self) -> None:
        if self.__tqdm__ is not None:
            self.__tqdm__.close()
        return

    def set_postfix(self, **kwargs) -> None:
        if self.__tqdm__ is not None:
            self.__tqdm__.set_postfix(**kwargs)
        return

    def reset(self, **kwargs) -> None:
        if self.__tqdm__ is not None:
            self.__tqdm__.reset(**kwargs)
        return
