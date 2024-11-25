import os
from urllib.parse import quote_plus

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.api.v1.schemas import InvalidFileName

STORE_FILE_PATH = "media/"
IMAGE_FILE_PATH = STORE_FILE_PATH + "images/"

if os.path.exists(STORE_FILE_PATH) is False:
    os.makedirs(STORE_FILE_PATH)
if os.path.exists(IMAGE_FILE_PATH) is False:
    os.makedirs(IMAGE_FILE_PATH)


def store_image(image: UploadFile) -> str:
    if image.filename is None:
        raise InvalidFileName
    if image.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        raise InvalidFileName
    with open(IMAGE_FILE_PATH + quote_plus(image.filename), "wb") as f:
        f.write(image.file.read())
    return image.filename


def read_image(filename: str):
    if os.path.exists(IMAGE_FILE_PATH + quote_plus(filename)) is False:
        raise InvalidFileName
    return FileResponse(
        IMAGE_FILE_PATH + quote_plus(filename),
        media_type="image/" + filename.split(".")[-1],
    )
