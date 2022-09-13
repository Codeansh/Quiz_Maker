from pydantic import BaseModel

class Solvers(BaseModel):
    pass
class Create_Quiz(BaseModel):
    title: str
    description : str
    duration :int
    solvers:dict
    questions : dict

class Update_quiz(BaseModel):

    description: str
    duration: int
    solvers: dict
    questions : dict

class Res_quiz(BaseModel):
    title : str
    description : str
    duration : int