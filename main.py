from fastapi import FastAPI

import yaml

from db import models
from db.db import engine
from api.api import api_router
from middleware.auth import AuthenticationMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blyze", docs_url='/')
app.openapi_schema = yaml.load(open('swagger.yaml').read())
app.include_router(api_router)
app.add_middleware(AuthenticationMiddleware)
