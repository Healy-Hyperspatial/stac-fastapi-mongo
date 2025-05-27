"""FastAPI application."""

import logging
import os

from stac_fastapi.api.app import StacApi
from stac_fastapi.api.models import create_get_request_model, create_post_request_model
from stac_fastapi.core.core import (
    CoreClient,
    EsAsyncBaseFiltersClient,
    TransactionsClient,
)
from stac_fastapi.core.extensions import QueryExtension
from stac_fastapi.core.route_dependencies import get_route_dependencies
from stac_fastapi.core.session import Session
from stac_fastapi.extensions.core import (
    FieldsExtension,
    FilterExtension,
    SortExtension,
    TokenPaginationExtension,
    TransactionExtension,
)

# from stac_fastapi.extensions.third_party import BulkTransactionExtension
from stac_fastapi.mongo.config import AsyncMongoDBSettings
from stac_fastapi.mongo.database_logic import (
    DatabaseLogic,
    create_collection_index,
    create_item_index,
)

logger = logging.getLogger(__name__)

settings = AsyncMongoDBSettings()
session = Session.create_from_settings(settings)

database_logic = DatabaseLogic()

filter_extension = FilterExtension(client=EsAsyncBaseFiltersClient(database=database_logic))
filter_extension.conformance_classes.append(
    "http://www.opengis.net/spec/cql2/1.0/conf/advanced-comparison-operators"
)

extensions = [
    TransactionExtension(
        client=TransactionsClient(
            database=database_logic, session=session, settings=settings
        ),
        settings=settings,
    ),
    # BulkTransactionExtension(
    #     client=BulkTransactionsClient(
    #         database=database_logic,
    #         session=session,
    #         settings=settings,
    #     )
    # ),
    FieldsExtension(),
    QueryExtension(),
    SortExtension(),
    TokenPaginationExtension(),
    filter_extension,
]

post_request_model = create_post_request_model(extensions)

api = StacApi(
    settings=settings,
    extensions=extensions,
    client=CoreClient(
        database=database_logic,
        session=session,
        post_request_model=post_request_model,
        landing_page_id=os.getenv("STAC_FASTAPI_LANDING_PAGE_ID", "stac-fastapi"),
    ),
    search_get_request_model=create_get_request_model(extensions),
    search_post_request_model=post_request_model,
    route_dependencies=get_route_dependencies(),
)
app = api.app


@app.on_event("startup")
async def _startup_event() -> None:
    if (
        os.getenv("MONGO_CREATE_INDEXES", "true") == "true"
    ):  # Boolean env variables in docker compose are actually strings
        await create_collection_index()
        await create_item_index()


def run() -> None:
    """Run app from command line using uvicorn if available."""
    try:
        import uvicorn

        logger.info("host: %s", settings.app_host)
        logger.info("port: %s", settings.app_port)
        uvicorn.run(
            "stac_fastapi.mongo.app:app",
            host=settings.app_host,
            port=settings.app_port,
            log_level="info",
            reload=settings.reload,
        )
    except ImportError:
        raise RuntimeError("Uvicorn must be installed in order to use command")


if __name__ == "__main__":
    run()


def create_handler(app):
    """Create a handler to use with AWS Lambda if mangum available."""
    try:
        from mangum import Mangum

        return Mangum(app)
    except ImportError:
        return None


handler = create_handler(app)
