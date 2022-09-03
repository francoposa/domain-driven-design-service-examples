import argparse
import asyncio
import os
import sys
from decimal import Decimal

import databases
import uvicorn  # type: ignore
import yaml
from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter
from starlette.middleware.cors import CORSMiddleware

from api.application.entity_aggregate.entity_handler import EntityHandler
from api.application.entity_aggregate.entity_router import entity_router
from api.application.health import health_handler
from api.domain.entity_aggregate.entity import (
    BarValueObject,
    ChildEntity,
    Entity,
    EntityList,
)
from api.domain.entity_aggregate.entity_repo import IEntityRepo
from api.domain.entity_aggregate.entity_service import EntityService
from api.infrastructure.entity_aggregate.entity_repo import PGEntityRepo

app = FastAPI()


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
pg_host = os.getenv("POSTGRES_HOST", default="localhost")
pg_port = os.getenv("POSTGRES_PORT", default=5432)
pg_user = os.getenv("POSTGRES_USER", default="postgres")
pg_password = os.getenv("POSTGRES_PASSWORD", default="")
pg_database = os.getenv("POSTGRES_DB", "entity_service")
pg_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
pg_client = databases.Database(pg_url)

entity_repo: IEntityRepo = PGEntityRepo(pg_client)
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


app.include_router(entity_router(entity_handler))


@app.on_event("startup")
async def startup():
    await pg_client.connect()


@app.on_event("shutdown")
async def shutdown():
    await pg_client.disconnect()


def main():  # pylint: disable=missing-function-docstring
    uvicorn.run(
        "api.main:app",
        host=config["server"]["host"],
        port=config["server"]["port"],
    )


if __name__ == "__main__":
    sys.exit(main())
