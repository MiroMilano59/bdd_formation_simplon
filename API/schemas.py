from pydantic import BaseModel

class Item(BaseModel):
    formaCode : int
    # Insert other parameters

    class Config:
        orm_mode = True