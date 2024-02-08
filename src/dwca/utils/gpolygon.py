from __future__ import annotations

from typing import List, Tuple, Any, Iterator


class GRing:
    """
    A set of ordered pairs of floating-point numbers.

    Parameters
    ----------
    points : Tuple[float, float]
        Points to generate a ring, minimum 3 points with latitude and longitude.
    """
    def __init__(self, *points: Tuple[float, float]) -> None:
        self.__points__ = list()
        assert len(points) >= 3, "At least 3 points to generate a ring"
        for point in points:
            self.__points__.append(point)
        return

    def __iter__(self) -> Iterator[Tuple[float, float]]:
        for point in self.__points__:
            yield point

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, GRing):
            return sorted(self.__points__) == sorted(other.__points__)
        if isinstance(other, list):
            return sorted(self.__points__) == sorted(other)
        return False


class GPolygon:
    """
    This construct creates a spatial ring with a hollow center.

    Parameters
    ----------
    outer : GRing
        The outer containment loop of a datasetGPolygon.
    exclusion : List[GRing], optional
        Exclusion G-Ring, the closed non-intersecting boundary of a void area (or hole in an interior area).
    """
    def __init__(
            self,
            outer: GRing,
            exclusion: List[GRing] = None
    ) -> None:
        self.__outer__ = outer
        self.__exclusion__ = list()
        if exclusion is not None:
            self.__exclusion__.extend(exclusion)
        return

    @property
    def outer(self) -> GRing:
        """GRing: The outer containment loop of a datasetGPolygon."""
        return self.__outer__

    @property
    def exclusion(self) -> List[GRing]:
        """List[GRing]: Exclusion G-Ring."""
        return self.__exclusion__
