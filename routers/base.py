from fastapi import APIRouter,Depends
from helper.config import get_settings,settings

base_router=APIRouter(prefix='/llms')
@base_router.get("/")

async def welcome(app_setting:settings=Depends(get_settings)):

    
    app_name=app_setting.app_name
    app_version=app_setting.app_version

    return {"app_name":app_name,
    "app_version":app_version}