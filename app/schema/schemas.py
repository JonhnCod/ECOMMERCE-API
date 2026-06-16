from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional


#Schema Base para Usuario 
class UsuarioBase(BaseModel):

    nome: str
    email: EmailStr
    telefone: Optional[str] = None


#Schema para criar um usuario, ele herda a propriedades do Base e acresenta mais a senha !
class UsuarioCriar(UsuarioBase):
    senha: str


#Schema para editar Usuario ele Herda as propriedades do Base porem ele altera os campos como opcional caso ele queria ediatar apenas um campo !
class UsuarioEditar(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha_hash: Optional[str] = None
    telefone: Optional[str] = None

# Schema de resposta Para um return de Usuario ao inves de retornar um Usuario com todos seus campos ele retorna apenas aqui que é importante como 'ID' e seu 'STATUS'
class UsuarioResponse(UsuarioBase):
    id_usuario: Optional[int] = None
    ativo: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

# Schema que entrega uma lista de todos os Usuarios 
class ListUsuarioResponse(BaseModel):
    usuarios: list[UsuarioResponse]

    model_config = ConfigDict(from_attributes=True)



class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str



class TokenResponse(BaseModel):
    access_token: str 
    refresh_token: str | None = None
    token_type: str = "Bearer"


