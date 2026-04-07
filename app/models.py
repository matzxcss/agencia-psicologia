"""
Clarear Psicologia — ORM Models (SQLAlchemy 2.0)
Tabelas: Agendamento, Depoimento
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base declarativa para todos os models."""
    pass


class Agendamento(Base):
    """Lead capturado pelo formulário de agendamento."""

    __tablename__ = "agendamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    mensagem: Mapped[str] = mapped_column(Text, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Agendamento(id={self.id}, nome='{self.nome}', email='{self.email}')>"


class Depoimento(Base):
    """Depoimentos exibidos na landing page."""

    __tablename__ = "depoimentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(80), nullable=False)
    idade: Mapped[int | None] = mapped_column(Integer, nullable=True)
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Depoimento(id={self.id}, nome='{self.nome}', ativo={self.ativo})>"
