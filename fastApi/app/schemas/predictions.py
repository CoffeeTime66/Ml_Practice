from typing import Any
from pydantic import BaseModel


class InputData(BaseModel):
    model: int
    age_group: Any
    RIAGENDR: Any
    PAQ605: Any
    BMXBMI: Any
    LBXGLU: Any
    DIQ010: Any
    LBXGLT: Any
    LBXIN: Any
    token: str