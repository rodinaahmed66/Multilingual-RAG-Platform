import uuid
from .minirag_base import SQLAlchemyBase
from sqlalchemy import column,Integer,DateTime,func
from sqlalchemy.dialects.postgresql import UUID

class Project(SQLAlchemyBase):

    __tablename__="projects"
    project_id=column(Integer,primery_key=True,autoincrement=True)
    project_uuid=column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False)


    creat_at=column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    update_at=column(DateTime(timezone=True),onupdate=func.now(),nullable=False)
    