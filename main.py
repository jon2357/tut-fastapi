# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/openapi.json
# http://127.0.0.1:8000/redoc

from enum import Enum
from fastapi import FastAPI, Query, Path, Body, status
from datetime import datetime, time, timedelta
from uuid import UUID


###########################################################
#### GET API setup Examples
###########################################################
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

###########################################################
#### POST API End Point Examples
###########################################################
from pydantic import BaseModel, Field, HttpUrl


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float

    # = Field(
    #     gt=0, description="The price must be greater than zero", example=35.4
    # )
    tax: float | None = Field(default=None, example=3.2)
    tags: list[str] = set()
    images: list[Image] | None = None

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Foo",
    #             "description": "A very nice item",
    #             "price": 40.3,
    #             "tax": 2.8,
    #         }
    #     }


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class User(BaseModel):
    username: str
    full_name: str | None = None


app = FastAPI()

###########################################################
#### POST API End Point Examples
###########################################################
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results


###########################################################
#### GET API End Point Examples
###########################################################

# http://127.0.0.1:8000/
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/")
async def read_items(
    q: list[str]
    | None = Query(
        default=["foo", "bar"],
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        deprecated=True,
        include_in_schema=False,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "bar"}]}
    if q:
        results.update({"q": q})

    return results


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: str | None = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# http://127.0.0.1:8000/items/?skip=0&limit=10
@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# http://127.0.0.1:8000/items/3
# http://127.0.0.1:8000/items/foo --fails because we do an integer check
# http://127.0.0.1:8000/items/4.2 -- fails because we do and integer check
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):  # integer check in the function definition
#     return {"item_id": item_id}

# http://127.0.0.1:8000/items/3?q=%22something%20else%20in%20the%20query%20string%22
# http://127.0.0.1:8000/items/3
# http://127.0.0.1:8000/items/3?q=howdy&short=true
# http://127.0.0.1:8000/items/3?q=howdy
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )

#     return item

# http://127.0.0.1:8000/items/3?needy=34
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


### Duplicate paths will never reach beyond the first
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


# This result will always fail because the above result matches first
@app.get("/users")
async def read_users():
    return ["Bean", "Elfo"]


### Order matters in path operations. If the next 2 routes where in the opposite order, calling 'me' would match the input parameter and not the the fixed end point
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# path parameter containing a complete path URL
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


#####
## https://fastapi.tiangolo.com/tutorial/query-params/
####


@app.post(
    "/itemsDesc/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
