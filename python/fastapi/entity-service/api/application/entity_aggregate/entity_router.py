from fastapi.routing import APIRoute, APIRouter

from api.application.entity_aggregate.entity_handler import EntityHandler
from api.domain.entity_aggregate.entity import Entity, EntityList

API_PREFIX_V0 = "/api/v0"
API_V0_ENTITIES_PATH = API_PREFIX_V0 + "/entities"
API_V0_ENTITIES_ID_PATH = API_PREFIX_V0 + "/entities/{entity_id}"


def entity_router(handler: EntityHandler) -> APIRouter:
    # FastAPI does not yet support introspection on class-based handlers.
    # Using APIRoute/APIRouter instead of decorators allows our handlers to be
    # members of a class, which allows us to inject the Service as a dependency.
    # The cost is some extra boilerplate config like declaring the response model,
    # instead of the magic/introspection provided by the decorators.
    get_entity_route = APIRoute(
        path=API_V0_ENTITIES_ID_PATH,
        endpoint=handler.get,
        methods=["GET"],
        response_model=Entity,
        name="Get Entity",
    )
    list_entities_route = APIRoute(
        path=API_V0_ENTITIES_PATH,
        endpoint=handler.list,
        methods=["GET"],
        response_model=EntityList,
        name="List Entities",
    )
    create_entity_route = APIRoute(
        path=API_V0_ENTITIES_PATH,
        endpoint=handler.create,
        methods=["PUT"],
        response_model=Entity,
        name="Create Entity",
    )
    return APIRouter(
        routes=[get_entity_route, list_entities_route, create_entity_route]
    )
