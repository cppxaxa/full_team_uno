
from typing import Optional
from pydantic import BaseModel

class CardModel(BaseModel):
    is_normal: Optional[bool] = True
    number: Optional[int] = -1
    color: Optional[str] = ""
    is_draw_2: Optional[bool] = False
    is_draw_4: Optional[bool] = False
    is_wild: Optional[bool] = False
    is_skip: Optional[bool] = False
    is_reverse: Optional[bool] = False
