from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBEnums
from Controllers.BaseController import BaseController

class VectorDBProviderFactory:

    def __init__(self,config:dict):
        self.config=config
        self.base_contrller=BaseController()


    def create(self,provider:str):
        if provider==VectorDBEnums.QDRANT.value:
            db_path=self.base_contrller.get_database_path(db_name=self.config.Vector_DB_PATH)
            return QdrantDBProvider(
               db_path=db_path,
               distance_method=self.config.Vector_DB_METHOD
            )
        return None


