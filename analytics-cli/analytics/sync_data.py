from itertools import chain

import openapi_client
from openapi_client.api import default_api
from openapi_client.model.defendant import Defendant
from openapi_client.model.defendant_post import DefendantPost
from openapi_client.model.judgment import Judgment
from openapi_client.model.judgment_post import JudgmentPost
from openapi_client.model.source import Source
from openapi_client.model.source_category import SourceCategory
from openapi_client.model.source_post import SourcePost
from openapi_client.model.species import Species
from openapi_client.model.species_bulk_patch_result import SpeciesBulkPatchResult

from analytics.lib.data_types import PoachingData, SpeciesData
from analytics.lib.functional import apply_non_none

client = openapi_client.ApiClient()
instance = default_api.DefaultApi(client)


def sync_species(species_data: list[SpeciesData]) -> SpeciesBulkPatchResult:
    data = [Species(**species.__dict__) for species in species_data]

    result: SpeciesBulkPatchResult = (
        instance.bulk_patch_species_analytics_species_patch(data)
    )

    return result


def sync_poaching_data(poaching_data: list[PoachingData]):
    for item in poaching_data:
        judgment_data = JudgmentPost(
            title=item.title,
            location=item.location,
            sentence=item.sentence,
            case_number=item.number,
            # species_info.keys() is a list of names of the species
            species_info=list(item.species_info.keys()),
        )
        defendant_data = [
            apply_non_none(
                DefendantPost,
                name=defendant.name,
                gender=defendant.gender,
                education_level=defendant.education_level,
            )
            for defendant in item.defendant_info
        ]
        source_data = [
            (
                defendant_source.name,
                [
                    apply_non_none(
                        SourcePost,
                        category=SourceCategory(source.type),
                        occasion=source.occasion,
                        seller=source.seller,
                        buyer=source.buyer,
                        method=source.method,
                        destination=source.destination,
                        usage=source.usage,
                    )
                    for source in chain(defendant_source.input, defendant_source.output)
                ],
            )
            for defendant_source in item.sources_info
        ]
        print(judgment_data)
        print(defendant_data)
        print(source_data)

        # We rely on the returned judgment id to sync the defendants and sources
        judgment_result: Judgment = instance.post_judgment_analytics_judgment_post(
            judgment_data, _check_return_type=False
        )
        print(judgment_result)

        # TODO: Use a bulk insertion API endpoint
        defendant_results: list[Defendant] = []
        for defendant in defendant_data:
            defendant_result: Defendant = (
                instance.post_defendant_analytics_judgment_defendant_judgment_id_post(
                    judgment_result.id, defendant, _check_return_type=False
                )
            )
            print(defendant_result)
            defendant_results.append(defendant_result)

        name_to_id_map = {
            defendant_result.name: defendant_result.id
            for defendant_result in defendant_results
        }

        for (name, sources) in source_data:
            for source in sources:
                if name in name_to_id_map:
                    source.set_attribute("defendant_id", name_to_id_map[name])
                source_result: Source = (
                    instance.post_source_analytics_judgment_source_judgment_id_post(
                        judgment_result.id, source, _check_return_type=False
                    )
                )
                print(source_result)

    return {}
