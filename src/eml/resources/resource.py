from abc import ABC

from eml.types import EMLObject, Scope


class Resource(EMLObject, ABC):
    """
    Abstract class representing any resources on an EML document

    Parameters
    ----------
    _id : str, optional
        Unique identifier
    scope : Scope, default DOCUMENT
        The scope of the identifier.
    system : str, optional
        The data management system within which an identifier is in scope and therefore unique.
    referencing : bool, optional, default=False
        Whether the resource is referencing another or is being defined
    references_system : str, optional
        System attribute of reference
    """

    def __init__(self, _id: str, scope: Scope = Scope.DOCUMENT, system: str = None, referencing: bool = False,
                 references_system: str = None) -> None:
        super().__init__(_id, scope, system, referencing, references_system)
        return
