from typing import Iterable, TypeVar

T = TypeVar('T')


def iterate_with_bar(iterator: Iterable[T], **kwargs) -> T:
    try:
        from tqdm import tqdm
        return tqdm(iterator, **kwargs)
    except ImportError:
        return iterator
