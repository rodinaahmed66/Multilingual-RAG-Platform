import uuid
from sqlalchemy import Index
from pydantic import BaseModel
from .minirag_base import SQLAlchemyBase
from sqlalchemy.orm import relationship
from sqlalchemy import column,Integer,DateTime,func,String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSONB


class DataChunk(SQLAlchemyBase):
        
        __tablename__="chunks"

        chunk_id=column(Integer,primery_key=True,autoincrement=True)
        chunk_uuid=column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False)

        chunk_text=column(String,nullable=False)
        chunk_metadata=column(JSONB,nullable=True)
        chunk_order=column(Integer,nullable=False)

        chunk_project_id=column(Integer,ForeignKey("projects.project_id"),nullable=False)
        chunk_asset_id=column(Integer,ForeignKey("assets.asset_id"),nullable=False)

        project = relationship("Project", back_populates="chunks") 
        asset = relationship("Asset", back_populates="chunks")


        __table_args__ = (
        Index('ix_chunk_project_id', chunk_project_id),
        Index('ix_chunk_type', chunk_asset_id),
    )
        

class RetrievedDocument(BaseModel):
        text:str
        score:float