import argparse
import json

from analytics.lib.data_types import SpeciesData
from analytics.sync_data import sync_species


def species_from_json(path: str) -> tuple[list[SpeciesData], list[tuple[str, object]]]:
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", choices=["species"], help="The type of action for sync"
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


if __name__ == "__main__":
    main()
