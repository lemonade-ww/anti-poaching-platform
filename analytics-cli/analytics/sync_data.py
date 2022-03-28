import openapi_client
from openapi_client.api import default_api
from openapi_client.model.species import Species
from openapi_client.model.species_bulk_patch_result import SpeciesBulkPatchResult

from analytics.lib.data_types import SpeciesData

client = openapi_client.ApiClient()
instance = default_api.DefaultApi(client)


def sync_species(species_data: list[SpeciesData]) -> SpeciesBulkPatchResult:
    data = [Species(**species.__dict__) for species in species_data]

    result: SpeciesBulkPatchResult = (
        instance.bulk_patch_species_analytics_species_patch(data)
    )

    return result
