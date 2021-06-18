
from pydantic import BaseModel

from typing import Optional

class UserModel(BaseModel):
    username: Optional[str] = ""
    passcode: Optional[str] = ""

