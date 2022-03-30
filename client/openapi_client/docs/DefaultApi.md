# openapi_client.DefaultApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bulk_patch_species_analytics_species_patch**](DefaultApi.md#bulk_patch_species_analytics_species_patch) | **PATCH** /analytics/species | Bulk Patch Species
[**get_defendant_analytics_judgment_defendant_get**](DefaultApi.md#get_defendant_analytics_judgment_defendant_get) | **GET** /analytics/judgment/defendant | Get Defendant
[**get_judgment_analytics_judgment_judgment_id_get**](DefaultApi.md#get_judgment_analytics_judgment_judgment_id_get) | **GET** /analytics/judgment/{judgment_id} | Get Judgment
[**get_sources_analytics_judgment_source_get**](DefaultApi.md#get_sources_analytics_judgment_source_get) | **GET** /analytics/judgment/source | Get Sources
[**get_species_analytics_species_get**](DefaultApi.md#get_species_analytics_species_get) | **GET** /analytics/species | Get Species
[**post_defendant_analytics_judgment_defendant_judgment_id_post**](DefaultApi.md#post_defendant_analytics_judgment_defendant_judgment_id_post) | **POST** /analytics/judgment/defendant/{judgment_id} | Post Defendant
[**post_judgment_analytics_judgment_post**](DefaultApi.md#post_judgment_analytics_judgment_post) | **POST** /analytics/judgment | Post Judgment
[**post_source_analytics_judgment_source_judgment_id_post**](DefaultApi.md#post_source_analytics_judgment_source_judgment_id_post) | **POST** /analytics/judgment/source/{judgment_id} | Post Source
[**read_root_get**](DefaultApi.md#read_root_get) | **GET** / | Read Root
[**search_judgments_analytics_judgment_get**](DefaultApi.md#search_judgments_analytics_judgment_get) | **GET** /analytics/judgment | Search Judgments


# **bulk_patch_species_analytics_species_patch**
> SpeciesBulkPatchResult bulk_patch_species_analytics_species_patch(species)

Bulk Patch Species

Insert or update species in bulk, creating missing taxons for each rank during operation  Args:     species (List[Species]): The species to be added/updated

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.species import Species
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.species_bulk_patch_result import SpeciesBulkPatchResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    species = [
        Species(
            species="species_example",
            genus="genus_example",
            family="family_example",
            order="order_example",
            _class="_class_example",
            protection_class=ProtectionClass("I"),
            conservation_status=ConservationStatus("EX"),
        ),
    ] # [Species] | 

    # example passing only required values which don't have defaults set
    try:
        # Bulk Patch Species
        api_response = api_instance.bulk_patch_species_analytics_species_patch(species)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->bulk_patch_species_analytics_species_patch: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **species** | [**[Species]**](Species.md)|  |

### Return type

[**SpeciesBulkPatchResult**](SpeciesBulkPatchResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_defendant_analytics_judgment_defendant_get**
> [Defendant] get_defendant_analytics_judgment_defendant_get()

Get Defendant

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.defendant import Defendant
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    judgment_id = 1 # int |  (optional)
    name = [
        "name_example",
    ] # [str] |  (optional)
    gender = [
        "gender_example",
    ] # [str] |  (optional)
    birth_before = dateutil_parser('1970-01-01').date() # date |  (optional)
    birth_after = dateutil_parser('1970-01-01').date() # date |  (optional)
    education_level = [
        "educationLevel_example",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Defendant
        api_response = api_instance.get_defendant_analytics_judgment_defendant_get(judgment_id=judgment_id, name=name, gender=gender, birth_before=birth_before, birth_after=birth_after, education_level=education_level)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_defendant_analytics_judgment_defendant_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **judgment_id** | **int**|  | [optional]
 **name** | **[str]**|  | [optional]
 **gender** | **[str]**|  | [optional]
 **birth_before** | **date**|  | [optional]
 **birth_after** | **date**|  | [optional]
 **education_level** | **[str]**|  | [optional]

### Return type

[**[Defendant]**](Defendant.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_judgment_analytics_judgment_judgment_id_get**
> Judgment get_judgment_analytics_judgment_judgment_id_get(judgment_id)

Get Judgment

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.judgment import Judgment
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    judgment_id = 1 # int | 

    # example passing only required values which don't have defaults set
    try:
        # Get Judgment
        api_response = api_instance.get_judgment_analytics_judgment_judgment_id_get(judgment_id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_judgment_analytics_judgment_judgment_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **judgment_id** | **int**|  |

### Return type

[**Judgment**](Judgment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sources_analytics_judgment_source_get**
> [Source] get_sources_analytics_judgment_source_get()

Get Sources

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.source import Source
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.source_category import SourceCategory
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    judgment_id = 1 # int |  (optional)
    defendant_id = 1 # int |  (optional)
    category = [
        SourceCategory("收购"),
    ] # [SourceCategory] |  (optional)
    occasion = [
        "occasion_example",
    ] # [str] |  (optional)
    seller = [
        "seller_example",
    ] # [str] |  (optional)
    buyer = [
        "buyer_example",
    ] # [str] |  (optional)
    method = [
        "method_example",
    ] # [str] |  (optional)
    destination = [
        "destination_example",
    ] # [str] |  (optional)
    usage = [
        "usage_example",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Sources
        api_response = api_instance.get_sources_analytics_judgment_source_get(judgment_id=judgment_id, defendant_id=defendant_id, category=category, occasion=occasion, seller=seller, buyer=buyer, method=method, destination=destination, usage=usage)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_sources_analytics_judgment_source_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **judgment_id** | **int**|  | [optional]
 **defendant_id** | **int**|  | [optional]
 **category** | [**[SourceCategory]**](SourceCategory.md)|  | [optional]
 **occasion** | **[str]**|  | [optional]
 **seller** | **[str]**|  | [optional]
 **buyer** | **[str]**|  | [optional]
 **method** | **[str]**|  | [optional]
 **destination** | **[str]**|  | [optional]
 **usage** | **[str]**|  | [optional]

### Return type

[**[Source]**](Source.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_species_analytics_species_get**
> [Species] get_species_analytics_species_get()

Get Species

Get a list of species with the given filters  Args:     species_filter (SpeciesFilter, optional): [description]. Defaults to Depends(SpeciesFilter).     db (Session, optional): [description]. Defaults to Depends(get_db).  Returns:     list[Species]: [description]

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.species import Species
from openapi_client.model.protection_class import ProtectionClass
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.conservation_status import ConservationStatus
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    species = [
        "species_example",
    ] # [str] |  (optional)
    genus = [
        "genus_example",
    ] # [str] |  (optional)
    family = [
        "family_example",
    ] # [str] |  (optional)
    order = [
        "order_example",
    ] # [str] |  (optional)
    _class = [
        "class_example",
    ] # [str] |  (optional)
    protection_class = [
        ProtectionClass("I"),
    ] # [ProtectionClass] |  (optional)
    conservation_status = [
        ConservationStatus("EX"),
    ] # [ConservationStatus] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Species
        api_response = api_instance.get_species_analytics_species_get(species=species, genus=genus, family=family, order=order, _class=_class, protection_class=protection_class, conservation_status=conservation_status)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->get_species_analytics_species_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **species** | **[str]**|  | [optional]
 **genus** | **[str]**|  | [optional]
 **family** | **[str]**|  | [optional]
 **order** | **[str]**|  | [optional]
 **_class** | **[str]**|  | [optional]
 **protection_class** | [**[ProtectionClass]**](ProtectionClass.md)|  | [optional]
 **conservation_status** | [**[ConservationStatus]**](ConservationStatus.md)|  | [optional]

### Return type

[**[Species]**](Species.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_defendant_analytics_judgment_defendant_judgment_id_post**
> Defendant post_defendant_analytics_judgment_defendant_judgment_id_post(judgment_id, defendant_post)

Post Defendant

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.defendant import Defendant
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.defendant_post import DefendantPost
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    judgment_id = 1 # int | 
    defendant_post = DefendantPost(
        name="name_example",
        gender="gender_example",
        birth=dateutil_parser('1970-01-01').date(),
        education_level="education_level_example",
    ) # DefendantPost | 

    # example passing only required values which don't have defaults set
    try:
        # Post Defendant
        api_response = api_instance.post_defendant_analytics_judgment_defendant_judgment_id_post(judgment_id, defendant_post)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->post_defendant_analytics_judgment_defendant_judgment_id_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **judgment_id** | **int**|  |
 **defendant_post** | [**DefendantPost**](DefendantPost.md)|  |

### Return type

[**Defendant**](Defendant.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_judgment_analytics_judgment_post**
> Judgment post_judgment_analytics_judgment_post(judgment_post)

Post Judgment

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.judgment_post import JudgmentPost
from openapi_client.model.judgment import Judgment
from openapi_client.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    judgment_post = JudgmentPost(
        title="title_example",
        case_number="case_number_example",
        location="location_example",
        release_date=dateutil_parser('1970-01-01').date(),
        content="content_example",
        sentence="sentence_example",
        species_names=[],
    ) # JudgmentPost | 

    # example passing only required values which don't have defaults set
    try:
        # Post Judgment
        api_response = api_instance.post_judgment_analytics_judgment_post(judgment_post)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->post_judgment_analytics_judgment_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **judgment_post** | [**JudgmentPost**](JudgmentPost.md)|  |

### Return type

[**Judgment**](Judgment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_source_analytics_judgment_source_judgment_id_post**
> Source post_source_analytics_judgment_source_judgment_id_post(judgment_id, source_post)

Post Source

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.source import Source
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.source_post import SourcePost
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    judgment_id = 1 # int | 
    source_post = SourcePost(
        category=SourceCategory("收购"),
        defendant_id=1,
        occasion="occasion_example",
        seller="seller_example",
        buyer="buyer_example",
        method="method_example",
        destination="destination_example",
        usage="usage_example",
    ) # SourcePost | 

    # example passing only required values which don't have defaults set
    try:
        # Post Source
        api_response = api_instance.post_source_analytics_judgment_source_judgment_id_post(judgment_id, source_post)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->post_source_analytics_judgment_source_judgment_id_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **judgment_id** | **int**|  |
 **source_post** | [**SourcePost**](SourcePost.md)|  |

### Return type

[**Source**](Source.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_root_get**
> bool, date, datetime, dict, float, int, list, str, none_type read_root_get()

Read Root

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Read Root
        api_response = api_instance.read_root_get()
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->read_root_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_judgments_analytics_judgment_get**
> [Judgment] search_judgments_analytics_judgment_get()

Search Judgments

### Example


```python
import time
import openapi_client
from openapi_client.api import default_api
from openapi_client.model.judgment import Judgment
from openapi_client.model.protection_class import ProtectionClass
from openapi_client.model.http_validation_error import HTTPValidationError
from openapi_client.model.conservation_status import ConservationStatus
from openapi_client.model.source_category import SourceCategory
from pprint import pprint
# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    judgment_id = 1 # int |  (optional)
    title = "title_example" # str |  (optional)
    location = "location_example" # str |  (optional)
    date_before = dateutil_parser('1970-01-01T00:00:00.00Z') # datetime |  (optional)
    date_after = dateutil_parser('1970-01-01T00:00:00.00Z') # datetime |  (optional)
    name = [
        "name_example",
    ] # [str] |  (optional)
    gender = [
        "gender_example",
    ] # [str] |  (optional)
    birth_before = dateutil_parser('1970-01-01').date() # date |  (optional)
    birth_after = dateutil_parser('1970-01-01').date() # date |  (optional)
    education_level = [
        "educationLevel_example",
    ] # [str] |  (optional)
    species = [
        "species_example",
    ] # [str] |  (optional)
    genus = [
        "genus_example",
    ] # [str] |  (optional)
    family = [
        "family_example",
    ] # [str] |  (optional)
    order = [
        "order_example",
    ] # [str] |  (optional)
    _class = [
        "class_example",
    ] # [str] |  (optional)
    protection_class = [
        ProtectionClass("I"),
    ] # [ProtectionClass] |  (optional)
    conservation_status = [
        ConservationStatus("EX"),
    ] # [ConservationStatus] |  (optional)
    defendant_id = 1 # int |  (optional)
    category = [
        SourceCategory("收购"),
    ] # [SourceCategory] |  (optional)
    occasion = [
        "occasion_example",
    ] # [str] |  (optional)
    seller = [
        "seller_example",
    ] # [str] |  (optional)
    buyer = [
        "buyer_example",
    ] # [str] |  (optional)
    method = [
        "method_example",
    ] # [str] |  (optional)
    destination = [
        "destination_example",
    ] # [str] |  (optional)
    usage = [
        "usage_example",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Search Judgments
        api_response = api_instance.search_judgments_analytics_judgment_get(judgment_id=judgment_id, title=title, location=location, date_before=date_before, date_after=date_after, name=name, gender=gender, birth_before=birth_before, birth_after=birth_after, education_level=education_level, species=species, genus=genus, family=family, order=order, _class=_class, protection_class=protection_class, conservation_status=conservation_status, defendant_id=defendant_id, category=category, occasion=occasion, seller=seller, buyer=buyer, method=method, destination=destination, usage=usage)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling DefaultApi->search_judgments_analytics_judgment_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **judgment_id** | **int**|  | [optional]
 **title** | **str**|  | [optional]
 **location** | **str**|  | [optional]
 **date_before** | **datetime**|  | [optional]
 **date_after** | **datetime**|  | [optional]
 **name** | **[str]**|  | [optional]
 **gender** | **[str]**|  | [optional]
 **birth_before** | **date**|  | [optional]
 **birth_after** | **date**|  | [optional]
 **education_level** | **[str]**|  | [optional]
 **species** | **[str]**|  | [optional]
 **genus** | **[str]**|  | [optional]
 **family** | **[str]**|  | [optional]
 **order** | **[str]**|  | [optional]
 **_class** | **[str]**|  | [optional]
 **protection_class** | [**[ProtectionClass]**](ProtectionClass.md)|  | [optional]
 **conservation_status** | [**[ConservationStatus]**](ConservationStatus.md)|  | [optional]
 **defendant_id** | **int**|  | [optional]
 **category** | [**[SourceCategory]**](SourceCategory.md)|  | [optional]
 **occasion** | **[str]**|  | [optional]
 **seller** | **[str]**|  | [optional]
 **buyer** | **[str]**|  | [optional]
 **method** | **[str]**|  | [optional]
 **destination** | **[str]**|  | [optional]
 **usage** | **[str]**|  | [optional]

### Return type

[**[Judgment]**](Judgment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

