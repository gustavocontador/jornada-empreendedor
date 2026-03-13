"""
DISC Calculator - Cálculo do perfil DISC.

DISC é um modelo de comportamento que avalia 4 dimensões:
- D (Dominância): Assertividade, controle, resultados
- I (Influência): Sociabilidade, persuasão, otimismo
- S (Estabilidade): Paciência, lealdade, consistência
- C (Conformidade): Precisão, qualidade, análise
"""
from typing import List, Dict, Any
from decimal import Decimal
from collections import defaultdict

from app.models.response import Response


def calculate_disc(responses: List[Response], questions_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula scores DISC a partir das respostas.

    Args:
        responses: Lista de respostas do usuário
        questions_data: Dados do questionário com pontuações

    Returns:
        Dicionário com scores DISC normalizados e perfil
    """
    # Acumula pontuações brutas
    raw_scores = {
        "disc_d": 0.0,
        "disc_i": 0.0,
        "disc_s": 0.0,
        "disc_c": 0.0
    }

    # Contadores de perguntas que pontuam cada dimensão (para normalização)
    question_counts = defaultdict(int)

    # Mapeia respostas por question_id para lookup rápido
    response_map = {str(r.question_id): r for r in responses}

    # Processa cada pergunta do questionário
    for question in questions_data.get("perguntas", []):
        question_id = question.get("id")
        pontuacao = question.get("pontuacao", {})

        # Pula perguntas sem pontuação DISC
        disc_keys = [k for k in pontuacao.keys() if k.startswith("disc_")]
        if not disc_keys:
            continue

        # Busca resposta do usuário
        response = response_map.get(question_id)
        if not response:
            continue

        # Extrai valor da resposta
        answer_value = response.answer_value

        # Para perguntas Likert (1-5)
        if question.get("tipo") == "likert_5":
            if isinstance(answer_value, (int, float)):
                likert_value = float(answer_value)
            elif isinstance(answer_value, dict) and "value" in answer_value:
                likert_value = float(answer_value["value"])
            else:
                continue

            # Normaliza Likert para -1 a +1 (3 é neutro)
            # 1 = -1.0, 2 = -0.5, 3 = 0.0, 4 = 0.5, 5 = 1.0
            normalized_value = (likert_value - 3) / 2

            # Aplica pesos de cada dimensão DISC
            for disc_key in ["disc_d", "disc_i", "disc_s", "disc_c"]:
                if disc_key in pontuacao:
                    weight = float(pontuacao[disc_key])
                    raw_scores[disc_key] += normalized_value * weight
                    question_counts[disc_key] += 1

    # Normaliza scores para 0-100
    normalized_scores = {}
    for key in ["disc_d", "disc_i", "disc_s", "disc_c"]:
        if question_counts[key] > 0:
            # Calcula média ponderada
            avg_score = raw_scores[key] / question_counts[key]
            # Converte de [-1, 1] para [0, 100]
            normalized_scores[key] = max(0, min(100, (avg_score + 1) * 50))
        else:
            normalized_scores[key] = 50.0  # Neutro se não houver perguntas

    # Gera perfil DISC (letras maiúsculas para scores > 60)
    profile = _generate_disc_profile(
        d=normalized_scores["disc_d"],
        i=normalized_scores["disc_i"],
        s=normalized_scores["disc_s"],
        c=normalized_scores["disc_c"]
    )

    return {
        "d": Decimal(str(round(normalized_scores["disc_d"], 2))),
        "i": Decimal(str(round(normalized_scores["disc_i"], 2))),
        "s": Decimal(str(round(normalized_scores["disc_s"], 2))),
        "c": Decimal(str(round(normalized_scores["disc_c"], 2))),
        "profile": profile,
        "description": _get_profile_description(profile)
    }


def _generate_disc_profile(d: float, i: float, s: float, c: float) -> str:
    """
    Gera código do perfil DISC baseado nos scores.

    Letras maiúsculas = score > 60 (traço dominante)
    Letras minúsculas = score 40-60 (traço presente)
    Sem letra = score < 40 (traço fraco)

    Args:
        d, i, s, c: Scores de cada dimensão (0-100)

    Returns:
        Código do perfil (ex: "DI", "SC", "disc", "D")
    """
    profile = ""

    dimensions = [
        ("D", d),
        ("I", i),
        ("S", s),
        ("C", c)
    ]

    # Ordena por score (maior primeiro)
    dimensions.sort(key=lambda x: x[1], reverse=True)

    for letter, score in dimensions:
        if score > 60:
            profile += letter  # Maiúscula
        elif score >= 40:
            profile += letter.lower()  # Minúscula
        # Scores < 40 não aparecem

    return profile if profile else "Equilibrado"


def _get_profile_description(profile: str) -> str:
    """
    Retorna descrição do perfil DISC.

    Args:
        profile: Código do perfil (ex: "DI", "SC")

    Returns:
        Descrição do perfil
    """
    descriptions = {
        "D": "Dominante puro - Assertivo, direto, orientado a resultados",
        "I": "Influente puro - Sociável, persuasivo, otimista",
        "S": "Estável puro - Paciente, leal, consistente",
        "C": "Consciente puro - Analítico, preciso, sistemático",
        "DI": "Inspirador/Criativo - Assertivo e sociável, líder carismático",
        "Di": "Realizador - Assertivo com toque de influência",
        "DS": "Resiliente - Assertivo mas com paciência (raro)",
        "DC": "Desafiador - Assertivo e analítico, busca excelência",
        "ID": "Persuasor - Influente e assertivo, vendedor nato",
        "IS": "Conselheiro - Influente e paciente, bom com pessoas",
        "IC": "Estimulador - Influente mas com análise (raro)",
        "SD": "Executor Estável - Paciente mas consegue ser assertivo quando necessário",
        "SI": "Agente de Suporte - Paciente e sociável, excelente em atendimento",
        "SC": "Planejador - Paciente e analítico, segue processos",
        "CD": "Perfeccionista Assertivo - Analítico que entrega resultados",
        "CI": "Analista Comunicador - Analítico que consegue persuadir (raro)",
        "CS": "Objetivo/Metodico - Analítico e paciente, especialista técnico",
        "Equilibrado": "Perfil balanceado - Adaptável a diferentes contextos"
    }

    return descriptions.get(profile, f"Perfil {profile} - Combinação única de traços")
