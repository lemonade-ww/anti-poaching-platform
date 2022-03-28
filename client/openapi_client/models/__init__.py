# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from openapi_client.model.conservation_status import ConservationStatus
from openapi_client.model.defendant import Defendant
from openapi_client.model.defendant_post import DefendantPost
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.judgment import Judgment
from openapi_client.model.judgment_post import JudgmentPost
from openapi_client.model.protection_class import ProtectionClass
from openapi_client.model.source import Source
from openapi_client.model.source_category import SourceCategory
from openapi_client.model.source_post import SourcePost
from openapi_client.model.species import Species
from openapi_client.model.species_bulk_patch_result import SpeciesBulkPatchResult
from openapi_client.model.species_short import SpeciesShort
from openapi_client.model.validation_error import ValidationError
