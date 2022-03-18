from sqlalchemy.engine.row import Row
from sqlalchemy.orm.session import Session

from api.db.models import TaxonClass, TaxonFamily, TaxonGenus, TaxonOrder, TaxonSpecies
from api.db.utils import QueryFilter, apply_filters, optional_filters
from api.lib.schemas import Species, SpeciesFilter


def from_species_filter(species_filter: SpeciesFilter) -> list[QueryFilter]:
    """Convert a filter object to a QueryFilter

    Args:
        species_filter (SpeciesFilter): The filter object to be converted

    Returns:
        list[QueryFilter]: A list of query filters
    """
    return optional_filters(
        (TaxonSpecies.name, "in", species_filter.species),
        (TaxonGenus.name, "in", species_filter.genus),
        (TaxonFamily.name, "in", species_filter.family),
        (TaxonOrder.name, "in", species_filter.order),
        (TaxonClass.name, "in", species_filter.class_),
        (TaxonSpecies.protection_class, "in", species_filter.protection_class),
        (TaxonSpecies.conservation_status, "in", species_filter.conservation_status),
    )


def query_species(db: Session, species_filter: SpeciesFilter) -> list[Species]:
    """Query the species based on taxon names

    Args:
        db (Session): The database session
        species_filter (SpeciesFilter): The filter to apply

    Returns:
        list[Species]: a list of species satisfying all the filtering constraints (None filters are ignored)
    """
    query = db.query(
        TaxonSpecies.name.label("species"),
        TaxonGenus.name.label("genus"),
        TaxonFamily.name.label("family"),
        TaxonOrder.name.label("order"),
        TaxonClass.name.label("class_"),
        TaxonSpecies.protection_class,
        TaxonSpecies.conservation_status,
    )

    query = apply_filters(
        query,
        optional_filters(
            (TaxonGenus.id, "=", TaxonSpecies.genus_id),
            (TaxonFamily.id, "=", TaxonGenus.family_id),
            (TaxonOrder.id, "=", TaxonFamily.order_id),
            (TaxonClass.id, "=", TaxonOrder.class_id),
        ),
    )

    result: list[Row] = apply_filters(
        query,
        from_species_filter(species_filter),
    ).all()

    return [Species(**row._mapping) for row in result]
