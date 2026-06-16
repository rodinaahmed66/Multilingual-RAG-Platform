import uuid
from sqlalchemy import Index
from minirag_base import SQLAlchemyBase
from sqlalchemy.orm import relationship
from sqlalchemy import column,Integer,DateTime,func,String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSONB

class Asset(SQLAlchemyBase):
        
        __tablename__="assets"

        asset_id=column(Integer,primery_key=True,autoincrement=True)
        asset_uuid=column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False)
        
        asset_type=column(String,nullable=False)
        asset_name=column(String,nullable=False)
        asset_size=column(String,nullable=False)

        asset_config=column(JSONB,nullable=True)

        asset_project_id=column(Integer,ForeignKey("projects.project_id"),nullable=False)

        project = relationship("Project", back_populates="assets")

        __table_args__ = (
        Index('ix_asset_project_id', asset_project_id),
        Index('ix_asset_type', asset_type),
    )