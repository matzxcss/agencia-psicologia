"""
Clarear Psicologia — Rotas da API.
POST /api/agendar      → cria lead (agendamento)
GET  /api/depoimentos  → lista depoimentos ativos
GET  /health           → healthcheck
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Agendamento, Depoimento
from app.schemas import AgendamentoCreate, AgendamentoResponse, DepoimentoResponse

router = APIRouter()


# ── Agendamento ─────────────────────────────────────────────────


@router.post(
    "/api/agendar",
    response_model=AgendamentoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar agendamento (lead)",
    tags=["Agendamento"],
)
async def criar_agendamento(
    dados: AgendamentoCreate,
    db: AsyncSession = Depends(get_db),
) -> Agendamento:
    """
    Recebe dados do formulário, valida via Pydantic e persiste no banco.
    Retorna a confirmação com id e timestamp.
    """
    agendamento = Agendamento(
        nome=dados.nome,
        email=dados.email,
        telefone=dados.telefone,
        mensagem=dados.mensagem,
    )
    db.add(agendamento)
    await db.commit()
    await db.refresh(agendamento)
    return agendamento


# ── Depoimentos ────────────────────────────────────────────────


@router.get(
    "/api/depoimentos",
    response_model=list[DepoimentoResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar depoimentos ativos",
    tags=["Depoimentos"],
)
async def listar_depoimentos(
    db: AsyncSession = Depends(get_db),
) -> list[Depoimento]:
    """Retorna todos os depoimentos com ativo=True."""
    result = await db.execute(
        select(Depoimento).where(Depoimento.ativo.is_(True))
    )
    return list(result.scalars().all())


# ── Sistema ────────────────────────────────────────────────────


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Healthcheck",
    tags=["Sistema"],
)
async def health():
    """Retorna status da API."""
    return {"status": "ok", "app": "Clarear Psicologia"}
