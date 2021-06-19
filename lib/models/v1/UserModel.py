
from pydantic import BaseModel

from typing import Optional

class UserModel(BaseModel):
    username: Optional[str] = ""
    passcode: Optional[str] = ""

    def is_valid(self):
        error = []
        if len(self.username) == 0:
            error.append("Username cannot be blank")
        if len(self.passcode) == 0:
            error.append("Password cannot be blank")
        
        if len(error) == 0:
            return True, error
        return False, error
    