"""
PAEI Calculator - Cálculo do estilo de gestão Adizes.

PAEI (Adizes) avalia 4 papéis gerenciais essenciais:
- P (Producer): Produção, execução, resultados de curto prazo
- A (Administrator): Administração, processos, organização
- E (Entrepreneur): Empreendedorismo, inovação, visão de longo prazo
- I (Integrator): Integração, cultura, pessoas, alinhamento
"""
from typing import List, Dict, Any
from decimal import Decimal
from collections import defaultdict

from app.models.response import Response


def calculate_paei(responses: List[Response], questions_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula scores PAEI a partir das respostas.

    Args:
        responses: Lista de respostas do usuário
        questions_data: Dados do questionário com pontuações

    Returns:
        Dicionário com scores PAEI e código
    """
    # Acumula pontuações brutas
    raw_scores = {
        "paei_p": 0.0,
        "paei_a": 0.0,
        "paei_e": 0.0,
        "paei_i": 0.0
    }

    # Contadores para normalização
    question_counts = defaultdict(int)

    # Mapeia respostas
    response_map = {str(r.question_id): r for r in responses}

    # Processa cada pergunta
    for question in questions_data.get("perguntas", []):
        question_id = question.get("id")
        pontuacao = question.get("pontuacao", {})

        # Filtra chaves paei_
        paei_keys = [k for k in pontuacao.keys() if k.startswith("paei_")]
        if not paei_keys:
            continue

        # Busca resposta
        response = response_map.get(question_id)
        if not response:
            continue

        answer_value = response.answer_value

        # Para perguntas Likert (1-5)
        if question.get("tipo") == "likert_5":
            if isinstance(answer_value, (int, float)):
                likert_value = float(answer_value)
            elif isinstance(answer_value, dict) and "value" in answer_value:
                likert_value = float(answer_value["value"])
            else:
                continue

            # Normaliza Likert para -1 a +1
            normalized_value = (likert_value - 3) / 2

            # Aplica pesos (incluindo negativos)
            for paei_key in raw_scores.keys():
                if paei_key in pontuacao:
                    weight = float(pontuacao[paei_key])
                    raw_scores[paei_key] += normalized_value * weight
                    question_counts[paei_key] += 1

        # Para perguntas de trade-off (q061, q062, q063)
        elif question.get("tipo") == "multiple_choice" and question_id in ["q061", "q062", "q063"]:
            if isinstance(answer_value, str):
                selected_value = answer_value
            elif isinstance(answer_value, dict) and "value" in answer_value:
                selected_value = answer_value["value"]
            else:
                continue

            # Adiciona 3 pontos para a escolha (trade-off forçado)
            paei_map = {
                "p": "paei_p",
                "a": "paei_a",
                "e": "paei_e",
                "i": "paei_i"
            }

            if selected_value in paei_map:
                paei_key = paei_map[selected_value]
                raw_scores[paei_key] += 3.0
                question_counts[paei_key] += 1

    # Normaliza scores para 0-100
    normalized_scores = {}
    for key in raw_scores.keys():
        if question_counts[key] > 0:
            avg_score = raw_scores[key] / question_counts[key]
            # Para PAEI, usamos escala mais ampla para capturar trade-offs
            normalized_scores[key] = max(0, min(100, (avg_score + 1.5) * 33.33))
        else:
            normalized_scores[key] = 50.0

    # Gera código PAEI
    paei_code = _generate_paei_code(
        p=normalized_scores["paei_p"],
        a=normalized_scores["paei_a"],
        e=normalized_scores["paei_e"],
        i=normalized_scores["paei_i"]
    )

    # Detecta problemas comuns
    issues = _detect_paei_issues(
        p=normalized_scores["paei_p"],
        a=normalized_scores["paei_a"],
        e=normalized_scores["paei_e"],
        i=normalized_scores["paei_i"],
        code=paei_code
    )

    return {
        "p": Decimal(str(round(normalized_scores["paei_p"], 2))),
        "a": Decimal(str(round(normalized_scores["paei_a"], 2))),
        "e": Decimal(str(round(normalized_scores["paei_e"], 2))),
        "i": Decimal(str(round(normalized_scores["paei_i"], 2))),
        "code": paei_code,
        "description": _get_paei_description(paei_code),
        "issues": issues
    }


def _generate_paei_code(p: float, a: float, e: float, i: float) -> str:
    """
    Gera código PAEI baseado nos scores.

    Letra MAIÚSCULA = score > 65 (forte)
    Letra minúscula = score 35-65 (presente)
    Traço (-) = score < 35 (fraco/ausente)

    Args:
        p, a, e, i: Scores de cada papel (0-100)

    Returns:
        Código PAEI (ex: "PAeI", "paEi", "P---")
    """
    def get_letter(score: float, letter: str) -> str:
        if score > 65:
            return letter.upper()
        elif score >= 35:
            return letter.lower()
        else:
            return "-"

    code = (
        get_letter(p, "P") +
        get_letter(a, "A") +
        get_letter(e, "E") +
        get_letter(i, "I")
    )

    return code


def _detect_paei_issues(p: float, a: float, e: float, i: float, code: str) -> List[Dict[str, Any]]:
    """
    Detecta problemas comuns de gestão baseados no perfil PAEI.

    Args:
        p, a, e, i: Scores normalizados
        code: Código PAEI gerado

    Returns:
        Lista de problemas detectados
    """
    issues = []

    # P muito alto + I muito baixo = Faz tudo sozinho
    if p > 75 and i < 30:
        issues.append({
            "type": "delegation_problem",
            "severity": "high",
            "description": "Alto P + Baixo I: Você tende a fazer tudo sozinho ao invés de delegar e desenvolver pessoas.",
            "impact": "Sobrecarga pessoal, gargalo de crescimento, equipe desmotivada.",
            "solution": "Pratique delegação progressiva. Invista tempo em treinamento mesmo que pareça 'ineficiente' no curto prazo."
        })

    # E muito alto + A muito baixo = Caos criativo
    if e > 75 and a < 30:
        issues.append({
            "type": "chaos_problem",
            "severity": "critical",
            "description": "Alto E + Baixo A: Muitas ideias, pouca execução estruturada. Mudanças constantes geram caos.",
            "impact": "Falta de processos, retrabalho, equipe perdida, dificuldade em escalar.",
            "solution": "Para cada 3 ideias, implemente apenas 1 até o fim. Contrate/desenvolva um Administrador forte para estruturar suas ideias."
        })

    # A muito alto + E muito baixo = Paralisia por análise
    if a > 75 and e < 30:
        issues.append({
            "type": "rigidity_problem",
            "severity": "medium",
            "description": "Alto A + Baixo E: Excesso de processos, falta de inovação. Empresa pode ficar estagnada.",
            "impact": "Dificuldade de adaptação, perda de oportunidades, burocracia excessiva.",
            "solution": "Reserve 20% do tempo para experimentação. Permita 'experimentos controlados' fora dos processos padrão."
        })

    # I muito alto + P muito baixo = Harmonia sem resultados
    if i > 75 and p < 30:
        issues.append({
            "type": "results_problem",
            "severity": "high",
            "description": "Alto I + Baixo P: Foco excessivo em harmonia, pouca cobrança por resultados.",
            "impact": "Equipe feliz mas improdutiva, metas não cumpridas, dificuldade financeira.",
            "solution": "Separe 'cuidar das pessoas' de 'cobrar resultados'. Você pode (e deve) fazer ambos. Use OKRs claros e transparentes."
        })

    # Todos baixos (---- ou similar)
    if all(score < 40 for score in [p, a, e, i]):
        issues.append({
            "type": "disengagement",
            "severity": "critical",
            "description": "Scores baixos em todos os papéis: Possível desengajamento ou falta de clareza sobre seu papel.",
            "impact": "Empresa sem direção clara, você pode estar perdido ou desmotivado.",
            "solution": "Reavalie se você realmente quer ser empreendedor. Se sim, identifique qual papel te energiza e comece por ele."
        })

    # Apenas um papel muito alto (monomaníaco)
    high_roles = sum(1 for score in [p, a, e, i] if score > 70)
    if high_roles == 1:
        issues.append({
            "type": "one_trick_pony",
            "severity": "medium",
            "description": "Apenas um papel dominante: Você pode estar negligenciando outros aspectos essenciais da gestão.",
            "impact": "Empresa desbalanceada, vulnerável a problemas nos papéis negligenciados.",
            "solution": "Desenvolva ao menos um papel secundário OU contrate/forme parceiros que complementem você."
        })

    # E alto + P alto + A baixo + I baixo = Workaholic maker
    if e > 65 and p > 65 and a < 40 and i < 40:
        issues.append({
            "type": "workaholic_entrepreneur",
            "severity": "high",
            "description": "Alto E+P, Baixo A+I: Empreendedor que faz tudo. Você gera ideias E executa tudo sozinho.",
            "impact": "Burnout garantido. Empresa depende 100% de você. Crescimento limitado.",
            "solution": "CRÍTICO: Contrate A (Organizador) e desenvolva I (Integrador). Você não pode ser todos os papéis."
        })

    return issues


def _get_paei_description(code: str) -> str:
    """
    Retorna descrição do perfil PAEI.

    Args:
        code: Código PAEI (ex: "PAeI")

    Returns:
        Descrição do perfil
    """
    descriptions = {
        "PAEI": "Super-líder (raro) - Forte em todos os papéis. Risco de sobrecarga.",
        "PAEi": "Líder Completo - Forte em execução, processos e inovação. Desenvolva Integração.",
        "PAeI": "Executor Integrador - Entrega resultados e cuida das pessoas. Inove mais.",
        "PaEI": "Visionário Integrador - Ideias e pessoas, mas precisa de mais disciplina.",
        "pAEI": "Líder de Pessoas - Forte em estrutura, inovação e cultura. Execute mais.",
        "PAe-": "Executor Organizador - Faz e organiza, mas sem visão de longo prazo.",
        "P-E-": "Empreendedor Fazedor - Ideias e execução, mas sem processos nem pessoas.",
        "P---": "Produtor Solitário (Lone Ranger) - Faz tudo sozinho. Não escala.",
        "-AE-": "Administrador Inovador - Estrutura mudanças, mas não executa nem integra.",
        "-A--": "Burocrata - Só processos. Empresa vira máquina sem alma.",
        "--E-": "Inventor - Só ideias, nenhuma execução. Empresa não sai do papel.",
        "---I": "Superficial - Só harmonia, sem substância. Empresa não funciona.",
        "paEi": "Empreendedor Equilibrado - Inovação com execução, processos e pessoas presentes.",
        "Paei": "Executor com Apoio - Produção forte, demais papéis presentes.",
        "pAei": "Organizador Equilibrado - Processos fortes, demais papéis presentes.",
        "----": "Sem Perfil Definido - Possível desengajamento ou transição."
    }

    return descriptions.get(code, f"Perfil {code} - Combinação única de papéis de gestão")
