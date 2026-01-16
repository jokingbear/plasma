from plasma.data_model import BaseModel


class SubForm(BaseModel):
    field1:int
    field2:str


class Form(BaseModel):
    field1:int
    field2:str
    field3:list[int]
    field4:str|int
    field5:SubForm
