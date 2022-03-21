from typing import Any

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

from api.crud.species import query_species
from api.db.models import (
    ModelT,
    TaxonClass,
    TaxonFamily,
    TaxonGenus,
    TaxonOrder,
    TaxonSpecies,
)
from api.db.utils import bulk_upsert
from api.dependencies import get_db
from api.lib import get_unique_attributes, has_query_params, map_attribute
from api.lib.schemas import Species, SpeciesBulkPatchResult, SpeciesFilter

router = APIRouter(prefix="/species")


@router.get("", response_model=list[Species])
def get_species(
    species_filter: SpeciesFilter = Depends(has_query_params(SpeciesFilter)),
    db: Session = Depends(get_db),
):
    """Get a list of species with the given filters

    Args:
        species_filter (SpeciesFilter, optional): [description]. Defaults to Depends(SpeciesFilter).
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        list[Species]: [description]
    """

    # Retrieve records of species from the database
    species = query_species(db, species_filter)

    return species


@router.patch("", response_model=SpeciesBulkPatchResult)
def bulk_patch_species(species: list[Species], db: Session = Depends(get_db)):
    """Insert or update species in bulk, creating missing taxons for each rank during operation

    Args:
        species (List[Species]): The species to be added/updated
    """
    # Find the minimal set for each rank of taxons of all species to be inserted
    # and then upsert in the top-to-down order (class -> order -> family -> genus -> species)
    tables: list[ModelT] = [
        TaxonClass,
        TaxonOrder,
        TaxonFamily,
        TaxonGenus,
        TaxonSpecies,
    ]
    taxon_unique_dict = get_unique_attributes(
        species, ["class_", "order", "family", "genus", "species"]
    )

    has_previous_taxon = False
    # Keep track of the name-id mappings of the parent taxons we just upserted
    previous_taxon: str = ""
    # Keep track of the name-to-id mapping for foreign keys
    taxon_name_id_dict: dict[str, Any] = {}
    upserted_objects = SpeciesBulkPatchResult()

    for table, taxon, (taxon_names, taxon_ref) in zip(
        tables, taxon_unique_dict.keys(), taxon_unique_dict.values()
    ):
        # We have a different naming format for the "class_" taxon
        previous_taxon_id_key = f"{previous_taxon.replace('_', '')}_id"

        # On conflicts, we update the foreign key reference
        # (plus protection_class and conservation_status for species
        # or name for the top-level taxon)
        update_keys = ["name"]
        if has_previous_taxon:
            update_keys = [previous_taxon_id_key]
            if taxon == "species":
                update_keys += ["protection_class", "conservation_status"]

        # Preare the values to be inserted
        values = []
        for name in taxon_names:
            # Top-level taxon only requires the name
            taxon_value = {"name": name}
            if has_previous_taxon:
                # lower-level taxons # retrieve the name of its parent taxon
                # from the referenced Species object, and query with the name
                # in taxon_name_id_dict to find the parent id
                taxon_value[previous_taxon_id_key] = taxon_name_id_dict[
                    getattr(taxon_ref[name], previous_taxon)
                ]
                if taxon == "species":
                    taxon_value["protection_class"] = getattr(
                        taxon_ref[name], "protection_class"
                    )
                    taxon_value["conservation_status"] = getattr(
                        taxon_ref[name], "conservation_status"
                    )
            values.append(taxon_value)

        # Perform a bulk upsert operation on the current taxon table
        # while returning the upserted id and name
        upsert_results = bulk_upsert(
            db,
            table,
            table.id,
            table.name,
            values=values,
            update_keys=update_keys,
            index_elements=[table.name],
        ).all()
        previous_taxon = taxon
        has_previous_taxon = True
        taxon_name_id_dict = map_attribute(upsert_results, "name", "id")
        setattr(upserted_objects, taxon, [name for name in taxon_name_id_dict.keys()])

    db.commit()
    return upserted_objects
