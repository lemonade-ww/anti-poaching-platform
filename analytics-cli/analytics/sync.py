import argparse
import json
from typing import TypeAlias, TypeVar

from analytics.lib.data_types import (
    DefendantData,
    PoachingData,
    SourceData,
    SourceInfo,
    SpeciesData,
)
from analytics.lib.functional import unpack, unpack_list
from analytics.sync_data import sync_poaching_data, sync_species

T = TypeVar("T")
ParseResult: TypeAlias = tuple[list[T], list[tuple[str, object]]]


def species_from_json(path: str) -> ParseResult[SpeciesData]:
    """Parse species from a json file into a list of SpeciesData

    Args:
        path (str): The path to the file to be parsed

    Raises:
        ValueError: If the structure of the json file is unsupported

    Returns:
        tuple[list[SpeciesData], list[tuple[str, str]]]: A tuple containing the parsed list of SpeciesData and a list of skipped entries
    """
    with open(path, "r") as f:
        data = json.load(f)
        if not isinstance(data, dict) or len(data) == 0:
            raise ValueError("Unsupported JSON file for species")
        skipped: list[tuple[str, object]] = []
        result: list[SpeciesData] = []
        for (species_name, value) in data.items():
            if not isinstance(value, str):
                # Skip entries with non-str values
                skipped.append((species_name, value))
                continue

            # Each entry is stored as "species_name": "class order family genus"
            # So we split the value by space
            taxon_info: list[str] = value.split()
            # Reverse taxon_info so it will structure like ["genus", "family", "order", "class"]
            taxon_info.reverse()

            if len(taxon_info) < 4:
                # Skip entries that do not have enough information
                skipped.append((species_name, value))
                continue

            result.append(SpeciesData(species_name, *taxon_info))
    return result, skipped


def analyzed_data_from_json(path: str) -> ParseResult[PoachingData]:
    """Parse species from a json file into a list of PoachingData

    Args:
        path (str): The path to the file to be parsed

    Raises:
        ValueError: If the structure of the json file is unsupported

    Returns:
        tuple[list[PoachingData], list[tuple[str, str]]]: A tuple containing the parsed list of PoachingData and a list of skipped entries
    """
    with open(path, "r") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Unsupported JSON file for sources")
        skipped: list[tuple[str, object]] = []
        result: list[PoachingData] = []
        for value in data:
            if (
                not isinstance(value, dict)
                or value.get("title") is None
                or value.get("data_id") is None
            ):
                # Skip entries with non-str values
                skipped.append(value)
                continue

            poaching_data = unpack(
                PoachingData,
                value,
                sentence=lambda: "\n".join(value["sentence"]),
                defendant_info=lambda: unpack_list(
                    DefendantData, value["defendant_info"]
                ),
                sources_info=lambda: unpack_list(
                    lambda **kwargs: unpack(
                        SourceData,
                        kwargs,
                        input=lambda: unpack_list(SourceInfo, kwargs["input"]),
                        output=lambda: unpack_list(SourceInfo, kwargs["output"]),
                    ),
                    value["sources_info"],
                ),
            )
            print(poaching_data)

            result.append(poaching_data)
    return result, skipped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", choices=["species", "analyzed"], help="The type of action for sync"
    )
    parser.add_argument(
        "sources", nargs="+", help="Files containing data to be synchronized"
    )
    args = parser.parse_args()

    sources: list[str] = args.sources
    match args.action:
        case "species":
            print("Reading sources..")
            for idx, source in enumerate(sources):
                try:
                    species_data, skipped = species_from_json(source)
                except json.JSONDecodeError:
                    print(
                        f"[{idx + 1}/{len(sources)}] {source}: Invalid JSON file. Skipping..."
                    )
                    continue

                result = sync_species(species_data)
                affected = len(result["species"])
                print(
                    f"[{idx + 1}/{len(sources)}] {source}: {affected}/{len(species_data)} species updated. {len(skipped)} entries skipped."
                )
            print("Done.")
        case "analyzed":
            print("Reading analyzed data..")
            for idx, source in enumerate(sources):
                try:
                    analyzed_data, skipped = analyzed_data_from_json(source)
                except json.JSONDecodeError:
                    print(
                        f"[{idx + 1}/{len(sources)}] {source}: Invalid JSON file. Skipping..."
                    )
                    continue

                result = sync_poaching_data(analyzed_data)
                affected = 1
                print(
                    f"[{idx + 1}/{len(sources)}] {source}: {affected}/{len(analyzed_data)} judgments updated. {len(skipped)} entries skipped."
                )
            print("Done.")


if __name__ == "__main__":
    main()
