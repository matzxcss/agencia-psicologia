"""
Clarear Psicologia — Seed de dados iniciais.
Popula depoimentos fictícios no primeiro boot.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Depoimento

DEPOIMENTOS_INICIAIS = [
    {
        "nome": "Mariana S.",
        "idade": 24,
        "texto": (
            "Eu achava que ansiedade era só 'ser assim'. "
            "Depois de algumas sessões, entendi meus padrões e hoje "
            "consigo respirar antes de reagir."
        ),
    },
    {
        "nome": "Lucas R.",
        "idade": 28,
        "texto": (
            "Estava travado em tudo: carreira, relacionamento, decisões. "
            "O Método Clarear me ajudou a separar o que era medo "
            "do que era realidade."
        ),
    },
    {
        "nome": "Camila T.",
        "idade": 22,
        "texto": (
            "Nunca tinha ido a um psicólogo. Achava que era 'coisa de gente com problema'. "
            "A primeira conversa mudou completamente essa ideia."
        ),
    },
]


async def seed_depoimentos(db: AsyncSession) -> None:
    """Insere depoimentos iniciais caso a tabela esteja vazia."""
    result = await db.execute(select(Depoimento).limit(1))
    if result.scalar_one_or_none() is not None:
        return  # já tem dados, pula

    for dados in DEPOIMENTOS_INICIAIS:
        db.add(Depoimento(**dados))

    await db.commit()
