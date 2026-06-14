from pydantic import BaseModel
from typing import Optional

class PushRequest(BaseModel):
    do_reset:Optional[int]=0


class Search_Request(BaseModel):
    text:str
    limit:Optional[int]=4
