"""
Clarear Psicologia — Pydantic Schemas (V2)
Validação de entrada e saída para a API.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ── Agendamento (Lead) ─────────────────────────────────────────


class AgendamentoCreate(BaseModel):
    """Schema de entrada: formulário de agendamento."""

    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Ana Clara"],
        description="Nome completo do paciente",
    )
    email: EmailStr = Field(
        ...,
        examples=["ana@email.com"],
        description="E-mail de contato",
    )
    telefone: str | None = Field(
        default=None,
        max_length=20,
        examples=["(11) 99999-0000"],
        description="Telefone (opcional)",
    )
    mensagem: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        examples=["Gostaria de agendar uma primeira conversa."],
        description="Mensagem para a psicóloga",
    )


class AgendamentoResponse(BaseModel):
    """Schema de saída: confirmação do agendamento."""

    id: int
    nome: str
    email: str
    criado_em: datetime

    model_config = {"from_attributes": True}


# ── Depoimento ─────────────────────────────────────────────────


class DepoimentoResponse(BaseModel):
    """Schema de saída: depoimento para a landing page."""

    id: int
    nome: str
    idade: int | None
    texto: str

    model_config = {"from_attributes": True}


# ── Quiz ────────────────────────────────────────────────────────


class QuizSubmit(BaseModel):
    """Schema de entrada: respostas do quiz interativo."""

    respostas: list[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Lista com 3 respostas (índice 0-3 cada)",
    )


class QuizResult(BaseModel):
    """Schema de saída: resultado do quiz."""

    perfil: str = Field(..., description="Nome do perfil emocional")
    descricao: str = Field(..., description="Descrição curta do resultado")
    recomendacao: str = Field(..., description="Sugestão de próximo passo")
