from sqlalchemy.engine.row import Row
from sqlalchemy.orm.session import Session

from api.db.models import TaxonClass, TaxonFamily, TaxonGenus, TaxonOrder, TaxonSpecies
from api.db.utils import optional_filters
from api.lib.schemas import Species


def query_species(
    db: Session,
    *,
    species: str | None,
    genus: str | None,
    family: str | None,
    order: str | None,
    class_: str | None,
) -> list[Species]:
    """Query the species based on taxon names

    Args:
        db (Session): The database session
        species (str | None): The name of the species
        genus (str | None): The name of the genus
        family (str | None): The name of the family
        order (str | None): The name of the order
        class_ (str | None): The name of the class_

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

    result: list[Row] = optional_filters(
        query,
        (TaxonSpecies.name, "~", species),
        (TaxonGenus.name, "~", genus),
        (TaxonFamily.name, "~", family),
        (TaxonOrder.name, "~", order),
        (TaxonClass.name, "~", class_),
        (TaxonGenus.id, "=", TaxonSpecies.genus_id),
        (TaxonFamily.id, "=", TaxonGenus.family_id),
        (TaxonOrder.id, "=", TaxonFamily.order_id),
        (TaxonClass.id, "=", TaxonOrder.class_id),
    ).all()

    return [Species(**row._mapping) for row in result]
