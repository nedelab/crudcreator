from fastapi.testclient import TestClient
from test.app import app
from ..utils import check_dict_key_type, reinit_db

#TODO : lib not compatible with pydantic v2
from openapi_schema_pydantic.v3.v3_0_3 import OpenAPI
from openapi_schema_pydantic.v3.v3_0_3.responses import Responses

import pytest

def _get_schema():
    """
    Renvoie le json du schema openapi
    """
    with TestClient(app) as client:
        ret = client.get("/openapi.json")
        assert ret.status_code == 200
        return ret.json()
    

def check_validation_error_response(responses: Responses):
    assert "422" in responses
    assert responses["422"].description == "Validation Error"
    assert len(responses["422"].content.keys()) == 1
    assert "application/json" in responses["422"].content
    assert responses["422"].content["application/json"].media_type_schema.ref == "#/components/schemas/HTTPValidationError"


def check_part_of_successfull_response(responses: Responses):
    assert "200" in responses
    assert responses["200"].description == "Successful Response"
    assert len(responses["200"].content.keys()) == 1
    assert "application/json" in responses["200"].content


def check_not_found_response(responses: Responses):
    assert "404" in responses
    assert responses["404"].description == "Not Found"
    assert len(responses["404"].content.keys()) == 1
    assert "application/json" in responses["404"].content


def check_conflict_response(responses: Responses):
    assert "409" in responses
    assert responses["409"].description == "Conflict"
    assert len(responses["409"].content.keys()) == 1
    assert "application/json" in responses["409"].content


def check_read_response(openapi: OpenAPI, path: str, object_name: str, could_have_validation_error: bool = True):
    assert len(openapi.paths[path].get.responses.keys()) == 2 if could_have_validation_error else 1
    ###200
    assert "200" in openapi.paths[path].get.responses
    assert openapi.paths[path].get.responses["200"].description == "Successful Response"
    assert len(openapi.paths[path].get.responses["200"].content.keys()) == 1
    assert "application/json" in openapi.paths[path].get.responses["200"].content
    assert openapi.paths[path].get.responses["200"].content["application/json"].media_type_schema.items.ref == f"#/components/schemas/{object_name}"
    assert openapi.paths[path].get.responses["200"].content["application/json"].media_type_schema.type == "array"
    ###422
    if could_have_validation_error:
        check_validation_error_response(openapi.paths[path].get.responses)


def check_update_response(openapi: OpenAPI, path: str):
    assert len(openapi.paths[path].patch.responses.keys()) == 4
    ###200
    check_part_of_successfull_response(openapi.paths[path].patch.responses)
    assert openapi.paths[path].patch.responses["200"].content["application/json"].media_type_schema.title is None#ne renvoie rien
    ###422
    check_validation_error_response(openapi.paths[path].patch.responses)
    ##404
    check_not_found_response(openapi.paths[path].patch.responses)
    ##409
    check_conflict_response(openapi.paths[path].patch.responses)


def check_delete_response(openapi: OpenAPI, path: str):
    assert len(openapi.paths[path].delete.responses.keys()) == 3
    ###200
    check_part_of_successfull_response(openapi.paths[path].patch.responses)
    assert openapi.paths[path].delete.responses["200"].content["application/json"].media_type_schema.title is None#ne renvoie rien
    ###422
    check_validation_error_response(openapi.paths[path].delete.responses)
    ##404
    check_not_found_response(openapi.paths[path].patch.responses)


def check_create_response(openapi: OpenAPI, path: str):
    assert len(openapi.paths[path].post.responses.keys()) == 3
    ###200
    check_part_of_successfull_response(openapi.paths[path].patch.responses)
    assert openapi.paths[path].post.responses["200"].content["application/json"].media_type_schema.title is None#ne renvoie rien
    ###422
    check_validation_error_response(openapi.paths[path].post.responses)
    ##409
    check_conflict_response(openapi.paths[path].patch.responses)


def get_structure() -> OpenAPI:
    """
    Récupère le schema openapi, et vérifie qu'il répond aux spécifications openapi
    """
    schema = _get_schema()
    assert type(schema) == dict
    return OpenAPI.parse_obj(schema)


@pytest.mark.asyncio
async def test_paths():
    """
    Vérifie qu'apparaissent les bonnes routes, et uniquement celles-là
    """
    await reinit_db()
    openapi = get_structure()
    assert list(openapi.paths.keys()) == [
        "/entity1", 
        "/entity1/bulk", 
        "/entity2", 
        "/entity3", 
        "/entity4", 
        "/entity6", 
        "/entity7", 
        "/entity7_bis",
        "/entity8", 
        "/entity9", 
        "/entity10", 
        "/entity11", 
        "/entity12",  
        "/entity13", 
        "/entity14",
        "/entity15",
        "/entity16",
        "/entity17",
        "/entity18",
        "/entity19",
        "/entity20",
        "/entity21",
        "/entity22",
        "/entity23",
        "/entity24",
        "/entity24/bulk",
        "/entity25",
        "/entity25/bulk",
        "/entity26",
    ]


@pytest.mark.asyncio
async def test_tags():
    """
    Vérifie que les routes sont associées aux bons tags
    """
    await reinit_db()
    openapi = get_structure()
    assert openapi.paths["/entity1"].get.tags == ["ENTITY1"]
    assert openapi.paths["/entity1"].post.tags == ["ENTITY1"]
    assert openapi.paths["/entity1"].patch.tags == ["ENTITY1"]
    assert openapi.paths["/entity1"].delete.tags == ["ENTITY1"]

    assert openapi.paths["/entity2"].get.tags == ["ENTITY2"]
    assert openapi.paths["/entity2"].post.tags == ["ENTITY2"]
    assert openapi.paths["/entity2"].patch.tags == ["ENTITY2"]
    assert openapi.paths["/entity2"].delete.tags == ["ENTITY2"]



@pytest.mark.asyncio
async def test_descriptions():
    """
    Vérifie que les routes ont les bonnes descriptions
    """
    await reinit_db()
    openapi = get_structure()
    assert openapi.paths["/entity1"].get.description == "Return a list of entity1.\n\nPossible filters :\n\n* field_text_primary_not_null_no_default (contain)\n\n* field_text_not_null_default (equal)\n\n* field_text_default (pattern)\n\n* field_bool_converted (equal)\n\n* field_bool_converted_bis (equal)"
    assert openapi.paths["/entity1"].post.description == "Create a entity1."
    assert openapi.paths["/entity1"].patch.description == "Update a entity1."
    assert openapi.paths["/entity1"].delete.description == "Delete a entity1."
    assert openapi.paths["/entity1"].put.description == "Create or update a entity1."

    assert openapi.paths["/entity2"].get.description == "Return a list of entity2."
    assert openapi.paths["/entity2"].post.description == "Create a entity2."
    assert openapi.paths["/entity2"].patch.description == "Update a entity2."
    assert openapi.paths["/entity2"].delete.description == "Delete a entity2."
    assert openapi.paths["/entity2"].put.description == "Create or update a entity2."


@pytest.mark.asyncio
async def test_parameters_entity1():
    """
    Vérifie que les routes ont les bons paramètres/body
    """
    await reinit_db()
    openapi = get_structure()
    ##get
    assert len(openapi.paths["/entity1"].get.parameters) == 5
    assert openapi.paths["/entity1"].get.requestBody is None#pas de body dans un get
    assert openapi.paths["/entity1"].get.parameters[0].required == False#on filtre seulement si l'on souhaite
    assert openapi.paths["/entity1"].get.parameters[0].name == "field_text_primary_not_null_no_default"
    assert openapi.paths["/entity1"].get.parameters[0].param_schema.type == "string"
    assert openapi.paths["/entity1"].get.parameters[0].param_schema.default == None
    assert openapi.paths["/entity1"].get.parameters[0].param_in == "query"
    assert openapi.paths["/entity1"].get.parameters[1].required == False#on filtre seulement si l'on souhaite
    assert openapi.paths["/entity1"].get.parameters[1].name == "field_text_not_null_default"
    assert openapi.paths["/entity1"].get.parameters[1].param_schema.type == "string"
    assert openapi.paths["/entity1"].get.parameters[1].param_schema.default == None
    assert openapi.paths["/entity1"].get.parameters[1].param_in == "query"
    assert openapi.paths["/entity1"].get.parameters[2].required == False#on filtre seulement si l'on souhaite
    assert openapi.paths["/entity1"].get.parameters[2].name == "field_text_default"
    assert openapi.paths["/entity1"].get.parameters[2].param_schema.type == "string"
    assert openapi.paths["/entity1"].get.parameters[2].param_schema.default == None
    assert openapi.paths["/entity1"].get.parameters[2].param_in == "query"
    assert openapi.paths["/entity1"].get.parameters[3].required == False#on filtre seulement si l'on souhaite
    assert openapi.paths["/entity1"].get.parameters[3].name == "field_bool_converted"
    assert openapi.paths["/entity1"].get.parameters[3].param_schema.type == "boolean"
    assert openapi.paths["/entity1"].get.parameters[3].param_schema.default == None
    assert openapi.paths["/entity1"].get.parameters[3].param_in == "query"
    assert openapi.paths["/entity1"].get.parameters[4].required == False#on filtre seulement si l'on souhaite
    assert openapi.paths["/entity1"].get.parameters[4].name == "field_bool_converted_bis_equal"#force_long_name
    assert openapi.paths["/entity1"].get.parameters[4].param_schema.type == "boolean"
    assert openapi.paths["/entity1"].get.parameters[4].param_schema.default == None
    assert openapi.paths["/entity1"].get.parameters[4].param_in == "query"
    ##post
    assert openapi.paths["/entity1"].post.parameters is None#pas de paramètres dans l'url pour le post
    assert len(openapi.paths["/entity1"].post.requestBody.content.keys()) == 1
    assert "application/json" in openapi.paths["/entity1"].post.requestBody.content#le body est au format json
    assert openapi.paths["/entity1"].post.requestBody.content["application/json"].media_type_schema.ref == "#/components/schemas/creator_of_entity1"
    ##patch
    assert len(openapi.paths["/entity1"].patch.requestBody.content.keys()) == 1
    assert "application/json" in openapi.paths["/entity1"].patch.requestBody.content
    assert openapi.paths["/entity1"].patch.requestBody.content["application/json"].media_type_schema.ref == "#/components/schemas/updator_of_entity1"
    assert len(openapi.paths["/entity1"].patch.parameters) == 1#body est paramètre url pour le patch
    assert openapi.paths["/entity1"].patch.parameters[0].required == True
    assert openapi.paths["/entity1"].patch.parameters[0].name == "field_text_primary_not_null_no_default"
    assert openapi.paths["/entity1"].patch.parameters[0].param_schema.type == "string"
    assert openapi.paths["/entity1"].patch.parameters[0].param_in == "query"
    ##delete
    assert len(openapi.paths["/entity1"].delete.parameters) == 1
    assert openapi.paths["/entity1"].delete.requestBody is None#pas de body dans un delete
    assert openapi.paths["/entity1"].delete.parameters[0].required == True
    assert openapi.paths["/entity1"].delete.parameters[0].name == "field_text_primary_not_null_no_default"
    assert openapi.paths["/entity1"].delete.parameters[0].param_schema.type == "string"
    assert openapi.paths["/entity1"].delete.parameters[0].param_in == "query"


@pytest.mark.asyncio
async def test_parameters_entity2():
    """
    Vérifie que les routes attendent les bons paramètres/body
    """
    await reinit_db()
    openapi = get_structure()
    ##get
    assert openapi.paths["/entity2"].get.parameters is None
    ##post
    assert openapi.paths["/entity2"].post.parameters is None#pas de paramètres dans l'url pour le post
    assert len(openapi.paths["/entity2"].post.requestBody.content.keys()) == 1
    assert "application/json" in openapi.paths["/entity2"].post.requestBody.content#le body est au format json
    assert openapi.paths["/entity2"].post.requestBody.content["application/json"].media_type_schema.ref == "#/components/schemas/creator_of_entity2"
    ##patch
    assert len(openapi.paths["/entity2"].patch.requestBody.content.keys()) == 1
    assert "application/json" in openapi.paths["/entity2"].patch.requestBody.content
    assert openapi.paths["/entity2"].patch.requestBody.content["application/json"].media_type_schema.ref == "#/components/schemas/updator_of_entity2"
    assert len(openapi.paths["/entity2"].patch.parameters) == 1#body est paramètre url pour le patch
    assert openapi.paths["/entity2"].patch.parameters[0].required == False#la clé primaire peut être null
    assert openapi.paths["/entity2"].patch.parameters[0].name == "field_not_pk_becomes_pk"
    assert openapi.paths["/entity2"].patch.parameters[0].param_schema.type == "integer"
    assert openapi.paths["/entity2"].patch.parameters[0].param_in == "query"
    ##delete
    assert len(openapi.paths["/entity2"].delete.parameters) == 1
    assert openapi.paths["/entity2"].delete.requestBody is None#pas de body dans un delete
    assert openapi.paths["/entity2"].delete.parameters[0].required == False#la clé primaire peut être null
    assert openapi.paths["/entity2"].delete.parameters[0].name == "field_not_pk_becomes_pk"
    assert openapi.paths["/entity2"].delete.parameters[0].param_schema.type == "integer"
    assert openapi.paths["/entity2"].delete.parameters[0].param_in == "query"


@pytest.mark.asyncio
async def test_response_entity1():
    """
    Vérifie le schema des réponses des routes
    """
    await reinit_db()
    openapi = get_structure()
    check_read_response(openapi, "/entity1", "entity1", could_have_validation_error=True)
    check_create_response(openapi, "/entity1")
    check_update_response(openapi, "/entity1")
    check_delete_response(openapi, "/entity1")


@pytest.mark.asyncio
async def test_response_entity2():
    """
    Vérifie le schema des réponses des routes
    """
    await reinit_db()
    openapi = get_structure()
    
    check_read_response(openapi, "/entity2", "entity2", could_have_validation_error=False)#could_have_validation_error=False car aucun filtre possible
    check_create_response(openapi, "/entity2")
    check_update_response(openapi, "/entity2")
    check_delete_response(openapi, "/entity2")


@pytest.mark.asyncio
async def test_components():
    """
    Que le nombre de composants est correct
    """
    await reinit_db()
    openapi = get_structure()
    assert len(openapi.components.schemas.keys()) == 125


@pytest.mark.asyncio
async def test_component_error_model():
    await reinit_db()
    openapi = get_structure()
    assert "ErrorModel" in openapi.components.schemas
    assert openapi.components.schemas["ErrorModel"].type == "object"
    assert len(openapi.components.schemas["ErrorModel"].properties.keys()) == 1
    assert "detail" in openapi.components.schemas["ErrorModel"].properties
    assert openapi.components.schemas["ErrorModel"].properties["detail"].type == "string"


@pytest.mark.asyncio
async def test_component_http_validation_error():
    await reinit_db()
    openapi = get_structure()
    assert "HTTPValidationError" in openapi.components.schemas
    assert openapi.components.schemas["HTTPValidationError"].type == "object"
    assert len(openapi.components.schemas["HTTPValidationError"].properties.keys()) == 1
    assert "detail" in openapi.components.schemas["HTTPValidationError"].properties
    assert openapi.components.schemas["HTTPValidationError"].properties["detail"].type == "array"
    assert openapi.components.schemas["HTTPValidationError"].properties["detail"].items.ref == "#/components/schemas/ValidationError"


@pytest.mark.asyncio
async def test_component_validation_error():
    await reinit_db()
    openapi = get_structure()
    assert "ValidationError" in openapi.components.schemas
    assert openapi.components.schemas["ValidationError"].type == "object"
    assert openapi.components.schemas["ValidationError"].required == ["loc", "msg", "type"]
    assert len(openapi.components.schemas["ValidationError"].properties.keys()) == 3
    assert "loc" in openapi.components.schemas["ValidationError"].properties
    assert openapi.components.schemas["ValidationError"].properties["loc"].type == "array"
    assert len(openapi.components.schemas["ValidationError"].properties["loc"].items.anyOf) == 2
    assert openapi.components.schemas["ValidationError"].properties["loc"].items.anyOf[0].type == "string"
    assert openapi.components.schemas["ValidationError"].properties["loc"].items.anyOf[1].type == "integer"
    assert "msg" in openapi.components.schemas["ValidationError"].properties
    assert openapi.components.schemas["ValidationError"].properties["msg"].type == "string"
    assert "type" in openapi.components.schemas["ValidationError"].properties
    assert openapi.components.schemas["ValidationError"].properties["type"].type == "string"
    

@pytest.mark.asyncio
async def test_component_creator_of_entity1():
    await reinit_db()
    openapi = get_structure()
    assert "creator_of_entity1" in openapi.components.schemas
    assert openapi.components.schemas["creator_of_entity1"].type == "object"
    assert openapi.components.schemas["creator_of_entity1"].required == ["field_text_primary_not_null_no_default"]#car c'est le seul qui ne peut être null et qui n'a pas de valeur par défaut
    assert len(openapi.components.schemas["creator_of_entity1"].properties.keys()) == 9
    
    assert "field_to_join" in openapi.components.schemas["creator_of_entity1"].properties
    assert openapi.components.schemas["creator_of_entity1"].properties["field_to_join"].type == "integer"
    assert openapi.components.schemas["creator_of_entity1"].properties["field_to_join"].default is None

    assert "field_int" in openapi.components.schemas["creator_of_entity1"].properties
    assert openapi.components.schemas["creator_of_entity1"].properties["field_int"].type == "integer"
    assert openapi.components.schemas["creator_of_entity1"].properties["field_int"].default is None
    
    assert "field_text_primary_not_null_no_default" in openapi.components.schemas["creator_of_entity1"].properties
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_primary_not_null_no_default"].type == "string"
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_primary_not_null_no_default"].default is None
    
    assert "field_text_not_null_default" in openapi.components.schemas["creator_of_entity1"].properties
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_not_null_default"].type == "string"
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_not_null_default"].default == "default_value_not_null"
    
    assert "field_text_default" in openapi.components.schemas["creator_of_entity1"].properties
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_default"].type == "string"
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_default"].default == "default_value"
    
    assert "field_text_no_default" in openapi.components.schemas["creator_of_entity1"].properties
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_no_default"].type == "string"
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_no_default"].default is None
    
    assert "field_text_overwritten_default" in openapi.components.schemas["creator_of_entity1"].properties
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_overwritten_default"].type == "string"
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_overwritten_default"].default == "overwritten_default"
    
    assert "field_bool_converted" in openapi.components.schemas["creator_of_entity1"].properties
    assert openapi.components.schemas["creator_of_entity1"].properties["field_bool_converted"].type == "boolean"#test que boolean bien que str dans la base
    assert openapi.components.schemas["creator_of_entity1"].properties["field_bool_converted"].default == True
    
    assert "field_text_creatable_not_updatable" in openapi.components.schemas["creator_of_entity1"].properties
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_creatable_not_updatable"].type == "string"
    assert openapi.components.schemas["creator_of_entity1"].properties["field_text_creatable_not_updatable"].default == None
    
    
@pytest.mark.asyncio
async def test_component_update_or_create_entity1():
    await reinit_db()
    openapi = get_structure()
    assert "update_or_create_of_submodel_value_update_or_create_entity1" in openapi.components.schemas
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].type == "object"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].required == ["field_text_primary_not_null_no_default"]#car c'est le seul qui ne peut être null et qui n'a pas de valeur par défaut
    assert len(openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties.keys()) == 10
    
    assert "field_to_join" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_to_join"].type == "integer"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_to_join"].default is None

    assert "field_int" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_int"].type == "integer"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_int"].default is None
    
    assert "field_text_primary_not_null_no_default" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_primary_not_null_no_default"].type == "string"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_primary_not_null_no_default"].default is None
    
    assert "field_text_not_null_default" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_not_null_default"].type == "string"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_not_null_default"].default == "default_value_not_null"
    
    assert "field_text_default" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_default"].type == "string"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_default"].default == "default_value"
    
    assert "field_text_no_default" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_no_default"].type == "string"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_no_default"].default is None
    
    assert "field_text_overwritten_default" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_overwritten_default"].type == "string"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_overwritten_default"].default == "overwritten_default"
    
    assert "field_bool_converted" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_bool_converted"].type == "boolean"#test que boolean bien que str dans la base
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_bool_converted"].default == True
    
    assert "field_text_creatable_not_updatable" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_creatable_not_updatable"].type == "string"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_creatable_not_updatable"].default == None

    assert "field_text_updatable_not_creatable" in openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_updatable_not_creatable"].type == "string"
    assert openapi.components.schemas["update_or_create_of_submodel_value_update_or_create_entity1"].properties["field_text_updatable_not_creatable"].default == None


@pytest.mark.asyncio
async def test_component_entity1():
    await reinit_db()
    openapi = get_structure()
    assert "entity1" in openapi.components.schemas
    assert openapi.components.schemas["entity1"].type == "object"
    assert openapi.components.schemas["entity1"].required == [
        "field_text_primary_not_null_no_default",
        "field_text_not_null_default"
    ]#ce sont les deux champs qui ne peuvent être nulls
    assert len(openapi.components.schemas["entity1"].properties.keys()) == 14
    
    assert "field_to_join" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_to_join"].type == "integer"
    assert openapi.components.schemas["entity1"].properties["field_to_join"].default is None
    
    assert "field_test" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_test"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_test"].default is None

    assert "field_int" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_int"].type == "integer"
    assert openapi.components.schemas["entity1"].properties["field_int"].default is None
    
    assert "field_text_primary_not_null_no_default" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_text_primary_not_null_no_default"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_text_primary_not_null_no_default"].default is None#pas de defaut dans un get
    
    assert "field_text_not_null_default" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_text_not_null_default"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_text_not_null_default"].default is None#pas de defaut dans un get
    
    assert "field_text_default" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_text_default"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_text_default"].default is None#pas de defaut dans un get
    
    assert "field_text_no_default" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_text_no_default"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_text_no_default"].default is None
    
    assert "field_text_overwritten_default" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_text_overwritten_default"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_text_overwritten_default"].default is None#pas de defaut dans un get
    
    assert "field_text_not_writable" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_text_not_writable"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_text_not_writable"].default is None#pas de defaut dans un get
    
    assert "field_text_not_writable_no_default" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_text_not_writable_no_default"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_text_not_writable_no_default"].default is None
    
    assert "field_bool_converted" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_bool_converted"].type == "boolean"#test que boolean bien que str dans la base
    assert openapi.components.schemas["entity1"].properties["field_bool_converted"].default is None#pas de defaut dans un get
    
    assert "field_bool_converted_bis" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_bool_converted_bis"].type == "boolean"#test que boolean bien que str dans la base
    assert openapi.components.schemas["entity1"].properties["field_bool_converted_bis"].default is None
    
    assert "field_text_creatable_not_updatable" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_text_creatable_not_updatable"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_text_creatable_not_updatable"].default == None

    assert "field_text_updatable_not_creatable" in openapi.components.schemas["entity1"].properties
    assert openapi.components.schemas["entity1"].properties["field_text_updatable_not_creatable"].type == "string"
    assert openapi.components.schemas["entity1"].properties["field_text_updatable_not_creatable"].default == None


@pytest.mark.asyncio
async def test_component_updator_of_entity1():
    await reinit_db()
    openapi = get_structure()
    assert "updator_of_entity1" in openapi.components.schemas
    assert openapi.components.schemas["updator_of_entity1"].type == "object"
    assert openapi.components.schemas["updator_of_entity1"].required == None
    assert len(openapi.components.schemas["updator_of_entity1"].properties.keys()) == 9

    assert "field_text_primary_not_null_no_default" in openapi.components.schemas["updator_of_entity1"].properties
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_primary_not_null_no_default"].type == "string"
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_primary_not_null_no_default"].default is None
    
    assert "field_to_join" in openapi.components.schemas["updator_of_entity1"].properties
    assert openapi.components.schemas["updator_of_entity1"].properties["field_to_join"].type == "integer"
    assert openapi.components.schemas["updator_of_entity1"].properties["field_to_join"].default is None

    assert "field_int" in openapi.components.schemas["updator_of_entity1"].properties
    assert openapi.components.schemas["updator_of_entity1"].properties["field_int"].type == "integer"
    assert openapi.components.schemas["updator_of_entity1"].properties["field_int"].default is None
    
    assert "field_text_not_null_default" in openapi.components.schemas["updator_of_entity1"].properties
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_not_null_default"].type == "string"
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_not_null_default"].default is None##pas de défaut pour les updates
    
    assert "field_text_default" in openapi.components.schemas["updator_of_entity1"].properties
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_default"].type == "string"
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_default"].default is None##pas de défaut pour les updates
    
    assert "field_text_no_default" in openapi.components.schemas["updator_of_entity1"].properties
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_no_default"].type == "string"
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_no_default"].default is None#TODO : faire la différence entre default à null et pas de default
    
    assert "field_text_overwritten_default" in openapi.components.schemas["updator_of_entity1"].properties
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_overwritten_default"].type == "string"
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_overwritten_default"].default is None##pas de défaut pour les updates
    
    assert "field_bool_converted" in openapi.components.schemas["updator_of_entity1"].properties
    assert openapi.components.schemas["updator_of_entity1"].properties["field_bool_converted"].type == "boolean"#test que boolean bien que str dans la base
    assert openapi.components.schemas["updator_of_entity1"].properties["field_bool_converted"].default is None##pas de défaut pour les updates
    
    assert "field_text_updatable_not_creatable" in openapi.components.schemas["updator_of_entity1"].properties
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_updatable_not_creatable"].type == "string"
    assert openapi.components.schemas["updator_of_entity1"].properties["field_text_updatable_not_creatable"].default is None##pas de défaut pour les updates
    


@pytest.mark.asyncio
async def test_filter_parameters_entity6():
    """
    Vérifie que les routes ont les bons paramètres/body
    """
    await reinit_db()
    openapi = get_structure()
    ##get
    assert len(openapi.paths["/entity16"].get.parameters) == 2
    assert openapi.paths["/entity16"].get.requestBody is None#pas de body dans un get
    assert openapi.paths["/entity16"].get.parameters[0].required == True#obligatoire
    assert openapi.paths["/entity16"].get.parameters[0].name == "field_id"
    assert openapi.paths["/entity16"].get.parameters[0].param_schema.type == "integer"
    assert openapi.paths["/entity16"].get.parameters[0].param_schema.default == None
    assert openapi.paths["/entity16"].get.parameters[0].param_in == "query"
    assert openapi.paths["/entity16"].get.parameters[1].required == False#a une valeur par défaut, donc considéré comme pas obligatoire
    assert openapi.paths["/entity16"].get.parameters[1].name == "field_test"
    assert openapi.paths["/entity16"].get.parameters[1].param_schema.type == "string"
    assert openapi.paths["/entity16"].get.parameters[1].param_schema.default == "test"
    assert openapi.paths["/entity16"].get.parameters[1].param_in == "query"



@pytest.mark.asyncio
async def test_parameters_entity18():
    """
    Vérifie que les routes ont les bons paramètres/body
    """
    await reinit_db()
    openapi = get_structure()
    ##get
    assert len(openapi.paths["/entity18"].get.parameters) == 2
    assert openapi.paths["/entity18"].get.requestBody is None#pas de body dans un get
    assert openapi.paths["/entity18"].get.parameters[0].required == False#on filtre seulement si l'on souhaite
    assert openapi.paths["/entity18"].get.parameters[0].name == "field_to_join"
    assert openapi.paths["/entity18"].get.parameters[0].param_schema.type == "integer"
    assert openapi.paths["/entity18"].get.parameters[0].param_schema.default == None
    assert openapi.paths["/entity18"].get.parameters[0].param_in == "query"
    assert openapi.paths["/entity18"].get.parameters[1].required == False#on filtre seulement si l'on souhaite
    assert openapi.paths["/entity18"].get.parameters[1].name == "field_bool_converted_bis"
    assert openapi.paths["/entity18"].get.parameters[1].param_schema.type == "boolean"
    assert openapi.paths["/entity18"].get.parameters[1].param_schema.default == None
    assert openapi.paths["/entity18"].get.parameters[1].param_in == "query"
    ##post
    assert openapi.paths["/entity18"].post.parameters is None#pas de paramètres dans l'url pour le post
    assert len(openapi.paths["/entity18"].post.requestBody.content.keys()) == 1
    assert "application/json" in openapi.paths["/entity18"].post.requestBody.content#le body est au format json
    assert openapi.paths["/entity18"].post.requestBody.content["application/json"].media_type_schema.ref == "#/components/schemas/creator_of_entity18"
    ##patch
    assert len(openapi.paths["/entity18"].patch.requestBody.content.keys()) == 1
    assert "application/json" in openapi.paths["/entity18"].patch.requestBody.content
    assert openapi.paths["/entity18"].patch.requestBody.content["application/json"].media_type_schema.ref == "#/components/schemas/updator_of_entity18"
    assert len(openapi.paths["/entity18"].patch.parameters) == 1#body est paramètre url pour le patch
    assert openapi.paths["/entity18"].patch.parameters[0].required == True
    assert openapi.paths["/entity18"].patch.parameters[0].name == "field_to_join"
    assert openapi.paths["/entity18"].patch.parameters[0].param_schema.type == "integer"
    assert openapi.paths["/entity18"].patch.parameters[0].param_in == "query"
    ##delete
    assert len(openapi.paths["/entity18"].delete.parameters) == 1
    assert openapi.paths["/entity18"].delete.requestBody is None#pas de body dans un delete
    assert openapi.paths["/entity18"].delete.parameters[0].required == True
    assert openapi.paths["/entity18"].delete.parameters[0].name == "field_to_join"
    assert openapi.paths["/entity18"].delete.parameters[0].param_schema.type == "integer"
    assert openapi.paths["/entity18"].delete.parameters[0].param_in == "query"



@pytest.mark.asyncio
async def test_component_creator_of_entity18():
    await reinit_db()
    openapi = get_structure()
    assert "creator_of_entity18" in openapi.components.schemas
    assert openapi.components.schemas["creator_of_entity18"].type == "object"
    assert openapi.components.schemas["creator_of_entity18"].required == ['field_to_join']
    assert len(openapi.components.schemas["creator_of_entity18"].properties.keys()) == 2
    assert "field_bool_converted_bis" in openapi.components.schemas["creator_of_entity18"].properties
    assert openapi.components.schemas["creator_of_entity18"].properties["field_bool_converted_bis"].type == "boolean"#test que boolean bien que str dans la base
    assert openapi.components.schemas["creator_of_entity18"].properties["field_bool_converted_bis"].default is None
    assert "field_to_join" in openapi.components.schemas["creator_of_entity18"].properties
    assert openapi.components.schemas["creator_of_entity18"].properties["field_to_join"].type == "integer"
    assert openapi.components.schemas["creator_of_entity18"].properties["field_to_join"].default is None


@pytest.mark.asyncio
async def test_component_updator_of_entity18():
    await reinit_db()
    openapi = get_structure()
    assert "updator_of_entity18" in openapi.components.schemas
    assert openapi.components.schemas["updator_of_entity18"].type == "object"
    assert openapi.components.schemas["updator_of_entity18"].required is None
    assert len(openapi.components.schemas["updator_of_entity18"].properties.keys()) == 2
    assert "field_bool_converted_bis" in openapi.components.schemas["updator_of_entity18"].properties
    assert openapi.components.schemas["updator_of_entity18"].properties["field_bool_converted_bis"].type == "boolean"#test que boolean bien que str dans la base
    assert openapi.components.schemas["updator_of_entity18"].properties["field_bool_converted_bis"].default is None
    assert "field_to_join" in openapi.components.schemas["updator_of_entity18"].properties
    assert openapi.components.schemas["updator_of_entity18"].properties["field_to_join"].type == "integer"
    assert openapi.components.schemas["updator_of_entity18"].properties["field_to_join"].default is None
     
@pytest.mark.asyncio
async def test_component_creator_of_entity21():
    await reinit_db()
    openapi = get_structure()
    assert "creator_of_entity21" in openapi.components.schemas
    assert openapi.components.schemas["creator_of_entity21"].type == "object"
    assert openapi.components.schemas["creator_of_entity21"].required is None#default
    assert len(openapi.components.schemas["creator_of_entity21"].properties.keys()) == 2
    assert "field_1" in openapi.components.schemas["creator_of_entity21"].properties
    assert openapi.components.schemas["creator_of_entity21"].properties["field_1"].type == "integer"
    assert openapi.components.schemas["creator_of_entity21"].properties["field_1"].default is None#même s'il y a un default factory ? (TODO)
    assert "field_2" in openapi.components.schemas["creator_of_entity21"].properties
    assert openapi.components.schemas["creator_of_entity21"].properties["field_2"].type == "integer"
    assert openapi.components.schemas["creator_of_entity21"].properties["field_2"].default == 10#AddDefault