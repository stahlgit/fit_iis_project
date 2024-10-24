from fastapi import HTTPException


def not_found(model: str):
    raise HTTPException(status_code=404, detail=f"{model} not found")
