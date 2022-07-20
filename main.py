# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/openapi.json
# http://127.0.0.1:8000/redoc


from fastapi import FastAPI

app = FastAPI()

# http://127.0.0.1:8000/
@app.get("/")
async def root():
    return {"message": "Hello World"}


# http://127.0.0.1:8000/items/3
# http://127.0.0.1:8000/items/foo --fails because we do an integer check
# http://127.0.0.1:8000/items/4.2 -- fails because we do and integer check
@app.get("/items/{item_id}")
async def read_item(item_id: int):  # integer check in the function definition
    return {"item_id": item_id}


### Order matters in path operations. If the next 2 routes where in the opposite order, calling 'me' would match the input parameter and not the the fixed end point
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


### Duplicate paths will never reach beyond the first
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


# This result will always fail because the above result matches first
@app.get("/users")
async def read_users():
    return ["Bean", "Elfo"]
