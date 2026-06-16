from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date, text, Boolean, Numeric, CheckConstraint, Integer
from typing import Optional
from datetime import date
from decimal import Decimal

class Base(DeclarativeBase):
    pass

class Usuario(Base):

    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(String(254), nullable=False)
    telefone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    data_criacao: Mapped[Optional[date]] = mapped_column(Date, server_default=text("current_date"))
    ativo: Mapped[Optional[bool]] = mapped_column(Boolean, server_default= text("true"))
    admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"Usuario(id={self.id_usuario}, nome={self.nome}, email={self.email})"
    


class Produto(Base):
    
    __tablename__ = "produtos"

    id_produto: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(254), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=True)
    preco: Mapped[Decimal] = mapped_column(Numeric(10,2), CheckConstraint("preco >= 0", name="check_preco_positivo"), nullable=False)
    estoque: Mapped[int] = mapped_column(Integer, CheckConstraint("estoque >= 0", name="check_estoque_positivo"), nullable=False)
    categoria: Mapped[str] = mapped_column(String(150), nullable=False)
    ativo: Mapped[Optional[bool]] = mapped_column(server_default= text("true"))
    data_criacao: Mapped[Optional[date]] = mapped_column(server_default=text("current_date"))

    def __repr__(self) -> str:
        return f"Produto(id={self.id_produto}, nome={self.nome}, descricao={self.deescricao}, preco={self.preco}, quantidade_estoque={self.estoque})"