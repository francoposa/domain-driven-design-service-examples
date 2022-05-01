import argparse
import sys

import uvicorn  # type: ignore
import yaml
from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter
from starlette.middleware.cors import CORSMiddleware

from api.application.entity_aggregate.entity_handler import EntityHandler
from api.application.health import health_handler
from api.domain.entity_aggregate.entity import Entity, EntityList
from api.domain.entity_aggregate.entity_repo import IEntityRepo
from api.domain.entity_aggregate.entity_service import EntityService
from api.infrastructure.entity_aggregate.entity_repo import StubEntityRepo

app = FastAPI()
API_PREFIX_V0 = "/api/v0"
API_V0_ENTITIES_PATH = API_PREFIX_V0 + "/entities"
API_V0_ENTITIES_ID_PATH = API_PREFIX_V0 + "/entities/{entity_id}"


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="config.local.yaml", help="Config file")
args = parser.parse_args()

# Load config.
with open(args.config, "r") as conf_file:
    config = yaml.safe_load(conf_file)

# inject database connection info from config here
# and use it to connect to some database client like:
# pg_client = databases.Database(DATABASE_URL)
# then inject it into your repo implementation like
# entity_repo: EntityRepo = PGEntityRepo(pg_client=pgclient)
entity_repo: IEntityRepo = StubEntityRepo()
entity_service = EntityService(repo=entity_repo)
entity_handler = EntityHandler(service=entity_service)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

get_service_health_route = APIRoute(
    path="/health",
    endpoint=health_handler.get_service_health,
    methods=["GET"],
    name="Get Service Health",
)
health_router = APIRouter(routes=[get_service_health_route])
app.include_router(health_router)

# FastAPI does not yet support introspection on class-based handlers.
# Using APIRoute/APIRouter instead of decorators allows our handlers to be
# members of a class, which allows us to inject the Service as a dependency.
# The cost is some extra boilerplate config like declaring the response model,
# instead of the magic/introspection provided by the decorators.
get_entity_route = APIRoute(
    path=API_V0_ENTITIES_ID_PATH,
    endpoint=entity_handler.get,
    methods=["GET"],
    response_model=Entity,
    name="Get Entity",
)
list_entities_route = APIRoute(
    path=API_V0_ENTITIES_PATH,
    endpoint=entity_handler.list,
    methods=["GET"],
    response_model=EntityList,
    name="List Entities",
)
entity_router = APIRouter(
    routes=[
        get_entity_route,
        list_entities_route,
    ]
)
app.include_router(entity_router)

# Apply these startup and shutdown signal handlers
# to whichever database client/engine you use

# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


def main():  # pylint: disable=missing-function-docstring
    uvicorn.run(
        "api.main:app",
        host=config["server"]["host"],
        port=config["server"]["port"],
    )


if __name__ == "__main__":
    sys.exit(main())
