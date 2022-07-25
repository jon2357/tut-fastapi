from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse

app = FastAPI()


# @app.post("/files/")
# async def create_file(file: bytes = File(description="A file read as bytes")):
#     return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(
#     file: UploadFile = File(description="A file read as UploadFile"),
# ):
#     return {"filename": file.filename}


@app.post("/files/")
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {
        "filenames": [file.filename for file in files],
        "description": [file.description for file in files],
    }


@app.post("/formfiles/")
async def create_form_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


@app.get("/")
async def main():
    content = """
<body>

<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>

<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>

</body>
    """
    return HTMLResponse(content=content)
