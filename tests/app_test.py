import pytest
from pidgin.app import *
from pidgin.errors import NoCoreMetadataException

def test_translate_dict_to_bibtex():
    input = {"object_id": "object_id_test", "key2": "value2", "key3": "value3"}
    output = translate_dict_to_bibtex(input)
    expected = '@misc {object_id_test, object_id = "object_id_test", key2 = "value2", key3 = "value3"}'
    assert output == expected

def test_flatten_dict():
    input = {"data": {"data_type_test": [{"core_metadata_collections": [{"creator": "creator_test", "description": "description_test"}], "file_name_test": "file_name", "object_id": "object_id_test"}]}}
    output = flatten_dict(input)
    expected = {"creator": "creator_test", "description": "description_test", "file_name_test": "file_name", "object_id": "object_id_test"}
    assert output == expected

def test_flatten_dict_raises_exception():
    """
    An exception should be raised if the core_metadata_collections field does not contain any data.
    """
    input = {'data': {'data_type_test': [{'core_metadata_collections': [], "file_name_test": "file_name", "object_id": "object_id_test"}]}}
    with pytest.raises(NoCoreMetadataException):
        flatten_dict(input)

def test_flatten_dict_raises_exception_with_details():
    """
    An exception should be raised if a requested field was not found for this file. The details of the error should be in the exception message.
    """
    input = {"data": "null", "errors": ["error_details_test"]}
    with pytest.raises(NoCoreMetadataException) as e:
        flatten_dict(input)
    assert 'error_details_test' in e.value.args[0]