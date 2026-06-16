from fastapi import APIRouter, status, Depends, HTTPException
from ..schema.schemas import  UsuarioResponse, UsuarioCriar, UsuarioEditar
from ..models.models import Usuario
from ..dependencies import verificar_token, SessionOpen
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.security import bcrypt_context
from sqlalchemy.exc import IntegrityError




router = APIRouter(prefix="/usuarios",tags=["usuarios"])


@router.get("/listar", response_model=UsuarioResponse)
async def perfil_usuario(usuario_logado: Usuario = Depends(verificar_token)):
    return usuario_logado


@router.get("/listar/{id}", response_model=UsuarioResponse, response_model_exclude_none=True)
async def listar_usuario(id: int, usuario_logado: Usuario = Depends(verificar_token), sessao: AsyncSession = Depends(SessionOpen)):
    try:
        if usuario_logado.id_usuario != id and not usuario_logado.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Erro, voce nao tem essa permissao"
            )
        if usuario_logado.id_usuario == id:
            if usuario_logado.admin:
                return usuario_logado
            
            return UsuarioResponse(nome=usuario_logado.nome, email=usuario_logado.email, telefone=usuario_logado.telefone)
        
        query = select(Usuario).where(Usuario.id_usuario == id)
        results = await sessao.execute(query)
        usuario = results.scalar_one_or_none()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario nao encontrado"
                )
        user = UsuarioResponse(id_usuario=usuario.id_usuario, nome=usuario.nome, email=usuario.email, telefone=usuario.telefone, ativo=usuario.ativo)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no sistema: {e}"
        )
    
@router.post("/criar-usuario")
async def criar_usuario(usuario_criar: UsuarioCriar, sessao: AsyncSession = Depends(SessionOpen)):
    try:
        senha_hash = bcrypt_context.hash(usuario_criar.senha)
        novo_usuario = Usuario(nome=usuario_criar.nome, email=usuario_criar.email,telefone=usuario_criar.telefone, senha_hash=senha_hash)

        sessao.add(novo_usuario)
        await sessao.commit()
        await sessao.refresh(novo_usuario)
        return {f"Usuario Cadastrado com sucesso: {novo_usuario.nome} {novo_usuario.email}"}
    except IntegrityError:
        await sessao.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esse email já existe !"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao cadastrar novo usuario"
        )
    


@router.put("/alterar")
async def alterar_usuario(usuario_alterar: UsuarioEditar, usuario_autenticado: Usuario = Depends(verificar_token), sessao: AsyncSession = Depends(SessionOpen)):
    try:

        dict_usuario = usuario_alterar.model_dump(exclude_none=True)

        if "senha_hash" in dict_usuario and dict_usuario["senha_hash"]:
            dict_usuario["senha_hash"] = bcrypt_context.hash(dict_usuario["senha_hash"])
        
        for chave, valor in dict_usuario.items():
            setattr(usuario_autenticado, chave, valor)

        await sessao.commit()
        await sessao.refresh(usuario_autenticado)

        return f"Usuario alterado com sucesso: {usuario_autenticado}"
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno, usuario nao alterado"
        )
    


@router.delete("/deletar/{id}")
async def deletar_usuario(id: int, usuario_autenticado: Usuario = Depends(verificar_token), sessao: AsyncSession = Depends(SessionOpen)):
    try:
        if id != usuario_autenticado.id_usuario and not usuario_autenticado.admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem autorizacao pra fazer isso"
            )
        if id == usuario_autenticado.id_usuario:
            usuario_deletar = usuario_autenticado
        else:
            query = select(Usuario).where(Usuario.id_usuario == id)
            results = await sessao.execute(query)
            usuario_banco = results.scalar_one_or_none()
            usuario_deletar = usuario_banco
                
        if not usuario_deletar.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario Inativo no sistema")
        usuario_deletar.ativo = False
        await sessao.commit()
        await sessao.refresh(usuario_autenticado)

        return {"msg": "Usuario deletado",
                "ID": usuario_deletar.id_usuario,
                "NOME": usuario_deletar.nome}
        
    except IntegrityError:
        await sessao.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao deletar Usuario"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro no servidor"
        )






















































# from fastapi import APIRouter, HTTPException, status, Depends
# from sqlalchemy.exc import IntegrityError
# from app.dependencies import SessionOpen,verificar_token
# from app.schema.schemas import UsuarioCriar, UsuarioResponse, UsuarioEditar, ListUsuarioResponse
# from app.models.models import Usuario
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from app.security import bcrypt_context

# router = APIRouter(prefix="/usuarios",tags=["usuarios"])


# #--------------------------------  LISTAR USUARIOS  -------------------------------------------------#

# @router.get("/listar", response_model=ListUsuarioResponse)
# async def listar_usuarios(usuario_autenticado: Usuario = Depends(verificar_token), sessao: AsyncSession = Depends(SessionOpen)):
#     try:

#         if not usuario_autenticado.admin:
#             raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, 
#         detail="Voce Nao tem permissao."
#         )

#         query = select(Usuario)
#         resultado = await sessao.execute(query)
#         usuarios = resultado.scalars().all()

#         if not usuarios:
#             raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, 
#         detail="Nenhum usuário encontrado."
#         )
#         return {"usuarios": usuarios}

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro ao listar usuários: {str(e)}"
#         )
    
#     #--------------------------------  LISTAR USUARIO POR ID  -------------------------------------------------#

# @router.get("/listar/{id}", response_model=UsuarioResponse)
# async def exibir_perfil(id: int, sessao: AsyncSession = Depends(SessionOpen), usuario_autenticado: Usuario = Depends(verificar_token)):
#     try:
#         print(type(usuario_autenticado.id_usuario))
        

#         if usuario_autenticado.id_usuario != id and not usuario_autenticado.admin:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Voce nao tem permissao para fazer isso"
#             )
        
#         if usuario_autenticado.id_usuario == id:
#             return usuario_autenticado
        
#         query = select(Usuario).where(Usuario.id_usuario == id)
#         resultado = await sessao.execute(query)
#         usuario = resultado.scalar_one_or_none()

#         if not usuario:
#             raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, 
#         detail=f"Usuario nao encontrado com ID: {id}"
#         )
#         return usuario

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro ao buscar usuário: {str(e)}"
#         )

#--------------------------------  CRIAR USUARIO  -------------------------------------------------#
# @router.post("/criar", response_model=UsuarioResponse)
# async def criar_usuario(usuario: UsuarioCriar, sessao: AsyncSession = Depends(SessionOpen)):
#     try:
#         novo_usuario = Usuario(
#             nome = usuario.nome,
#             email = usuario.email,
#             senha_hash = bcrypt_context.hash(usuario.senha),
#             telefone = usuario.telefone

#         )
#         sessao.add(novo_usuario)
#         await sessao.commit()
#         await sessao.refresh(novo_usuario)

#         return novo_usuario

#     except IntegrityError:
#         await sessao.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email já Cadastrado"
#         )
        
#     except Exception as e:
#         await sessao.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro ao criar usuario: {str(e)}"
#         )


# #--------------------------------  EDITAR USUARIO  -------------------------------------------------#


# @router.put("/editar/{id}", response_model=UsuarioResponse)
# async def editar_usuario(id: int, usuario_in: UsuarioEditar, sessao: AsyncSession = Depends(SessionOpen),usuario_autenticado: Usuario  = Depends(verificar_token)):
#     try:
#         if usuario_autenticado.admin:
        
#             query = select(Usuario).where(Usuario.id_usuario == id)
#             resultado = await sessao.execute(query)
#             usuario_banco = resultado.scalar_one_or_none()

            
#             if not usuario_banco:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail=f"Usuário com ID {id} não encontrado."
#                 )
#         else:
#             if usuario_autenticado.id_usuario != id:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="Você não tem permissão para editar outros usuários."
#                 )

#         dados_atualizados = usuario_in.model_dump(exclude_unset=True)
            
#         for chave, valor in dados_atualizados.items():
#                 setattr(usuario_autenticado, chave, valor)

#         await sessao.commit()
#         await sessao.refresh(usuario_autenticado)

#         return usuario_autenticado

#     except HTTPException:
#         raise
#     except Exception as e:
#         await sessao.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro ao editar usuário: {str(e)}"
#         )
    


# @router.delete("/deletar/{id}", response_model=UsuarioResponse)
# async def deletar_usuario(
#     id: int, 
#     sessao: AsyncSession = Depends(SessionOpen)
# ):
#     try:

#         query = select(Usuario).where(Usuario.id_usuario == id , Usuario.ativo == True)
#         resultado = await sessao.execute(query)
#         usuario_banco = resultado.scalar_one_or_none()

#         if not usuario_banco:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Usuário com ID {id} não encontrado ou Desativado."
#             )
        
#         usuario_banco.ativo = False
#         await sessao.commit()
#         await sessao.refresh(usuario_banco)

#         return usuario_banco
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         await sessao.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erro ao deletar usuário: {str(e)}"
#         )
