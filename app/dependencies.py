from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Usuario
from app.security import outh2_schema
from fastapi import HTTPException, status, Depends
from app.database import async_session
from app.security import ALGORITHM, SECRET_KEY
from jose import JWTError
import jwt



async def SessionOpen():
    async with async_session() as  sessao:
        yield sessao



async def verificar_token(token: str = Depends(outh2_schema), sessao: AsyncSession = Depends(SessionOpen)):
    try:
        info_user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(info_user.get("sub"))
    except JWTError:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Acesso negado ou token expirado {e}"
        )
    query_usuario = select(Usuario).where(Usuario.id_usuario == usuario_id)
    results_usuario = await sessao.execute(query_usuario)
    usuario = results_usuario.scalars().first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado"
        )
    
    return usuario



