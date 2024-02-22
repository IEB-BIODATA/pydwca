from dwca.utils import CamelCaseEnum


class EstablishmentMeans(CamelCaseEnum):
    """
    Terms intended to be used as a controlled value for Darwin Core terms with local name establishmentMeans.

    For details and rationale, see Groom et al. 2019. Improving Darwin Core for research
    and management of alien species. https://doi.org/10.3897/biss.3.38084

    Attributes
    ----------
    NATIVE : int
        A taxon occurring within its natural range.
    NATIVE_REINTRODUCED : int
        A taxon re-established by direct introduction into its natural range, but from where it had become extinct.
    INTRODUCED : int
        Establishment of a taxon by human agency into an area that is not part of its natural range.
    INTRODUCED_ASSISTED_COLONISATION : int
        Establishment of a taxon specifically with the intention of creating a self-sustaining wild population.
    VAGRANT : int
        The temporary occurrence of a taxon far outside its natural or migratory range.
    UNCERTAIN : int
        The origin of the occurrence of the taxon in an area is obscure.
    """
    NATIVE = 1
    NATIVE_REINTRODUCED = 2
    INTRODUCED = 3
    INTRODUCED_ASSISTED_COLONISATION = 4
    VAGRANT = 5
    UNCERTAIN = 6

    def get_iri(self) -> str:
        """
        Generate the Term IRI (Internationalized Resource Identifier) of the Establishment Means.

        Returns
        -------
        str
            Term IRI.
        """
        return f"http://rs.tdwg.org/dwcem/values/e{self.value:03}"
