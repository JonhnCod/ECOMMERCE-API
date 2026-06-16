from sqlalchemy import select
from app.models.models import Usuario
from fastapi import HTTPException, status
from app.security import bcrypt_context
from datetime import timedelta, timezone, datetime
from jose import jwt, JWTError
from app.security import ALGORITHM, SECRET_KEY



async def autenticar_usuario(senha, email, sessao):
    try:
        query_usuario = select(Usuario).where(Usuario.email == email)
        results_usuario = await sessao.execute(query_usuario)
        usuario = results_usuario.scalars().first()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario nao encontrado ou email ou senha incorreto "
            )

        if not bcrypt_context.verify(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="senha invalida"
            )
        return usuario
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro: {str(e)}"
        )
    

async def gerar_token(id_usuario, duracao_token=timedelta(hours=1)):

    try:
        tempo_expiracao = datetime.now(timezone.utc) + duracao_token
        timestamp_inteiro = int(tempo_expiracao.timestamp())

        payload = {
            "sub": str(id_usuario),
            "exp": timestamp_inteiro
            }
        
        token_encoding = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token_encoding
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao gerar token"
        )
    
    