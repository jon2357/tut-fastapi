from fastapi import Cookie, FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    ads_id: str | None = Cookie(default=None),
    user_agent: str | None = Header(default=None),
):
    return {"ads_id": ads_id, "User-Agent": user_agent}
