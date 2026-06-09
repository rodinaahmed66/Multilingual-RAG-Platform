from .BaseController import BaseController
from models.db_schemes import Project,DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List

class NLPController(BaseController):

    def __init__(self,vectordb_client,
                 embedding_client,
                 generation_client  ):
        
        super().__init__()

        self.vectordb_client=vectordb_client
        self.embedding_client=embedding_client
        self.generation_client=generation_client

    
    def create_collection_name(self,project_id:str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self,project:Project):

        collection_name=self.create_collection_name(
            project_id=project.project_id
        )
        return self.vectordb_client.delete_collection(
            collection_name=collection_name
        )
    
    def get_vector_collection_info(self,project:Project):

        collection_name=self.create_collection_name(
            project_id=project.project_id
        )

        collection_info=self.vectordb_client.get_collection_info(
            collection_name=collection_name
        )

        return collection_info
    
    def index_into_vector_db(self,project:Project,
                             chunks:List[DataChunk],
                             chunks_ids:List[int],
                            do_reset:bool =False):
        
        #step 1 get collection name
        collection_name=self.create_collection_name(
            project_id=project.project_id
        )

        #step 2 mange items
        texts=[c.chunk_text for c in chunks]
        metadata=[c.chunk_metadata for c in chunks]
        vectors=[
            self.embedding_client.embed_text(
                text=text,
                document_type=DocumentTypeEnum.DOCUMENT.value)
                 for text in texts
                ]
        
        #step 3 create collection
        self.vectordb_client.create_collection(
            collection_name=collection_name,
                        embedding_size=self.embedding_client.embedding_size,
                        do_reset=do_reset)
        
        #step 4 insert inside db
        _=self.vectordb_client.insert_many(
            collection_name=collection_name,
                   texts=texts,
                   vectors=vectors,
                   metadata= metadata,
                   record_ids=chunks_ids
               )
        
        return True
        
        