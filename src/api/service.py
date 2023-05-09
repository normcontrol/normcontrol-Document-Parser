import uvicorn
from fastapi import FastAPI
from bestconfig import Config
from .router import parser_router

__config = Config('settings.ini').to_dict()

app = FastAPI(
    title= "Parser Service"
)
app.config = __config
app.include_router(parser_router)
