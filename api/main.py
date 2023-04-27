"""
API for reading Aerosol Alerts Service evaluation database
"""

from typing import Union

from fastapi import FastAPI

app = FastAPI(
    title="Aerosol Alerts Service API",
    version="0.1.0",
    contact={
        "name": "Augustin Mortier",
        "email": "augustinm@met.no"
    },
    description="Aerosol Alerts Service API for reading the Evaluation Database",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    root_path="/api/0.1.0" #comment this line when run locally
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}