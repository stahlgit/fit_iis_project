import importlib
import os

from fastapi import FastAPI

app = FastAPI(
    title="FIT ISS PROJECT API",
    version="0.1",
)


@app.get("/")
def read_root():
    return {"Hello": "World!"}


directory = "app/api/v1/routers"
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and f.endswith(".py"):
        module_name = filename[:-3]  # remove .py from filename
        module = importlib.import_module(
            directory.replace("/", ".") + "." + module_name, package=None
        )
        app.include_router(module.router)
