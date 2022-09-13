from pydantic import BaseModel, EmailStr

class NewUser(BaseModel):
    username : str
    fullname : str
    password : str
    email : EmailStr

class LoginUser(BaseModel):
    username : str
    password : str