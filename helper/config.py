from pydantic_settings import BaseSettings,SettingsConfigDict

class settings(BaseSettings):
    app_name: str
    app_version:str
    file_allowed_types:list
    file_max_size:int
    file_default_chunk_size:int
    MONGO_URL:str
    MONGODB_DATABASE:str
    #class config: 
        #env_file=".env"
    model_config = SettingsConfigDict(env_file=".env")
    
def get_settings():
    return settings()
