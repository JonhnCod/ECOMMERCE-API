from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from app.schema.schemas import UsuarioLogin, TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import SessionOpen
from app.routers.functions import gerar_token, autenticar_usuario
from ..dependencies import verificar_token
from datetime import timedelta
from app.models.models import Usuario
from fastapi.security import OAuth2PasswordRequestForm



auth_router = APIRouter(prefix="/auth",tags=["auth"])


@auth_router.post("/login", response_model=TokenResponse)
async def login(usuarioLogin: UsuarioLogin, sessao: AsyncSession = Depends(SessionOpen)):

    try:
        usuario = await autenticar_usuario(usuarioLogin.senha, usuarioLogin.email, sessao)

        token_access = await gerar_token(usuario.id_usuario)

        token_refresh = await gerar_token(usuario.id_usuario, duracao_token=timedelta(days=7))

        return TokenResponse(access_token=token_access, refresh_token=token_refresh)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro do servidor: {str(e)}"
        )
    

@auth_router.post("/login-form", response_model=TokenResponse, response_model_exclude_none=True)
async def login_form(dados_form: OAuth2PasswordRequestForm = Depends(), sessao: AsyncSession = Depends(SessionOpen)):

    try:
        usuario = await autenticar_usuario(email=dados_form.username, senha=dados_form.password, sessao=sessao)

        token_access = await gerar_token(usuario.id_usuario)

        return TokenResponse(access_token=token_access)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro do servidor: {str(e)}"
        )

@auth_router.get("/refresh")
async def refresh_token(usuario: Usuario = Depends(verificar_token)):

    token_access = await gerar_token(usuario.id_usuario)
    
    return {
        "access_token": token_access,
        "token_type": "Bearer"
        }
