"""
Scoring Engine - Orquestrador principal de cálculo de scores.

Este módulo coordena o cálculo de todos os frameworks psicométricos
a partir das respostas do usuário ao questionário.
"""
from typing import List, Dict, Any
from decimal import Decimal

from app.models.response import Response
from app.services.calculators.disc_calculator import calculate_disc
from app.services.calculators.spiral_calculator import calculate_spiral
from app.services.calculators.paei_calculator import calculate_paei
from app.services.calculators.enneagram_calculator import calculate_enneagram
from app.services.calculators.valores_calculator import calculate_valores
from app.services.calculators.arquetipos_calculator import calculate_arquetipos
from app.services.calculators.interpretations_generator import generate_interpretations


class ScoringEngine:
    """
    Engine principal para cálculo de todos os scores psicométricos.

    Coordena a execução de todos os calculadores individuais e gera
    interpretações baseadas nos resultados combinados.
    """

    @staticmethod
    def calculate_all_scores(responses: List[Response], questions_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula todos os scores a partir das respostas do usuário.

        Args:
            responses: Lista de respostas do usuário
            questions_data: Dados do questionário (perguntas e pontuações)

        Returns:
            Dicionário completo com todos os scores e interpretações
        """
        # Calcula cada framework individualmente
        disc_scores = calculate_disc(responses, questions_data)
        spiral_scores = calculate_spiral(responses, questions_data)
        paei_scores = calculate_paei(responses, questions_data)
        enneagram_scores = calculate_enneagram(responses, questions_data)
        valores_scores = calculate_valores(responses, questions_data)
        arquetipos_scores = calculate_arquetipos(responses, questions_data)

        # Gera interpretações profundas baseadas nos scores combinados
        interpretations = generate_interpretations(
            disc=disc_scores,
            spiral=spiral_scores,
            paei=paei_scores,
            enneagram=enneagram_scores,
            valores=valores_scores,
            arquetipos=arquetipos_scores,
            responses=responses,
            questions_data=questions_data
        )

        # Gera recomendações personalizadas
        recommendations = ScoringEngine._generate_recommendations(
            disc=disc_scores,
            spiral=spiral_scores,
            paei=paei_scores,
            enneagram=enneagram_scores,
            valores=valores_scores,
            arquetipos=arquetipos_scores,
            interpretations=interpretations
        )

        return {
            "disc": disc_scores,
            "spiral": spiral_scores,
            "paei": paei_scores,
            "enneagram": enneagram_scores,
            "valores": valores_scores,
            "arquetipos": arquetipos_scores,
            "interpretations": interpretations,
            "recommendations": recommendations
        }

    @staticmethod
    def _generate_recommendations(
        disc: Dict[str, Any],
        spiral: Dict[str, Any],
        paei: Dict[str, Any],
        enneagram: Dict[str, Any],
        valores: Dict[str, Any],
        arquetipos: Dict[str, Any],
        interpretations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Gera recomendações personalizadas baseadas em todos os scores.

        Args:
            disc: Scores DISC
            spiral: Scores Spiral Dynamics
            paei: Scores PAEI
            enneagram: Scores Eneagrama
            valores: Scores Valores
            arquetipos: Scores Arquétipos
            interpretations: Interpretações geradas

        Returns:
            Dicionário com recomendações personalizadas
        """
        recommendations = {
            "gestao_pessoas": [],
            "gestao_financeira": [],
            "processos_organizacao": [],
            "estrategia_crescimento": [],
            "desenvolvimento_pessoal": [],
            "contratacoes": []
        }

        # Recomendações baseadas em PAEI
        paei_code = paei.get("code", "")

        # Alto P + Baixo I = Problema com delegação
        if paei.get("p", 0) > 70 and paei.get("i", 0) < 40:
            recommendations["gestao_pessoas"].append({
                "area": "Delegação",
                "priority": "high",
                "issue": "Você tende a fazer tudo sozinho ao invés de delegar.",
                "action": "Crie um processo de delegação gradual: comece com tarefas pequenas e aumente progressivamente. Use o framework 'Observar-Explicar-Fazer-Revisar'."
            })

        # Alto E + Baixo A = Caos organizacional
        if paei.get("e", 0) > 70 and paei.get("a", 0) < 40:
            recommendations["processos_organizacao"].append({
                "area": "Estruturação",
                "priority": "critical",
                "issue": "Seu perfil empreendedor gera mudanças constantes sem processos estruturados.",
                "action": "Contrate ou desenvolva um 'Organizador Metódico' (arquétipo). Dedique 20% do seu tempo semanal para documentação de processos."
            })

        # Baixo A em geral = Problemas financeiros potenciais
        if paei.get("a", 0) < 40:
            recommendations["gestao_financeira"].append({
                "area": "Controle Financeiro",
                "priority": "high",
                "issue": "Falta de organização administrativa pode gerar problemas de caixa.",
                "action": "Implemente dashboards financeiros semanais. Use ferramentas como Conta Azul ou Omie. Considere contratar um CFO parcial."
            })

        # Recomendações baseadas em Spiral Dynamics
        primary_spiral = spiral.get("primary", "")
        secondary_spiral = spiral.get("secondary", "")

        # Combinação problemática: Roxo + Laranja
        if "purple" in [primary_spiral, secondary_spiral] and "orange" in [primary_spiral, secondary_spiral]:
            recommendations["desenvolvimento_pessoal"].append({
                "area": "Tensão Interna",
                "priority": "medium",
                "issue": "Tensão entre lealdade tribal (Roxo) e ambição individual (Laranja).",
                "action": "Reconheça que ambos são válidos em contextos diferentes. Use Roxo para cultura interna e Laranja para mercado externo."
            })

        # Alto Vermelho + Baixo Verde = Problemas com equipe
        if spiral.get("red", 0) > 60 and spiral.get("green", 0) < 30:
            recommendations["gestao_pessoas"].append({
                "area": "Estilo de Liderança",
                "priority": "high",
                "issue": "Seu estilo assertivo/dominante pode gerar atrito com equipes.",
                "action": "Pratique escuta ativa. Pergunte opiniões antes de decidir. Use o framework 'Perguntar-Ouvir-Decidir' ao invés de 'Decidir-Comunicar'."
            })

        # Alto Verde + Baixo Azul = Falta de estrutura
        if spiral.get("green", 0) > 60 and spiral.get("blue", 0) < 30:
            recommendations["processos_organizacao"].append({
                "area": "Disciplina e Processos",
                "priority": "medium",
                "issue": "Excesso de flexibilidade pode gerar falta de previsibilidade.",
                "action": "Estabeleça 3-5 regras inegociáveis para a empresa. Crie rituais semanais fixos (ex: reunião de resultados toda sexta às 9h)."
            })

        # Recomendações baseadas em Eneagrama
        ennea_type = enneagram.get("type", 0)

        if ennea_type == 8:
            recommendations["desenvolvimento_pessoal"].append({
                "area": "Vulnerabilidade",
                "priority": "medium",
                "issue": "Tipo 8 tende a esconder vulnerabilidade e afastar pessoas.",
                "action": "Pratique compartilhar incertezas com 1-2 pessoas de confiança. Vulnerabilidade não é fraqueza, é construção de confiança."
            })

        elif ennea_type == 9:
            recommendations["desenvolvimento_pessoal"].append({
                "area": "Assertividade",
                "priority": "high",
                "issue": "Tipo 9 evita conflitos e tem dificuldade em saber o que realmente quer.",
                "action": "Use a técnica 'Check-in diário': toda manhã, pergunte-se 'O que EU quero hoje?' e anote. Pratique dizer 'não' 1x por dia."
            })

        elif ennea_type == 3:
            recommendations["desenvolvimento_pessoal"].append({
                "area": "Autenticidade",
                "priority": "medium",
                "issue": "Tipo 3 pode se perder em busca de validação externa e status.",
                "action": "Defina 3 valores pessoais inegociáveis. Antes de decisões importantes, pergunte: 'Isso está alinhado com meus valores ou apenas com minha imagem?'"
            })

        # Recomendações baseadas em DISC
        disc_profile = disc.get("profile", "")

        if "D" in disc_profile and "S" not in disc_profile:
            recommendations["gestao_pessoas"].append({
                "area": "Paciência com Processos",
                "priority": "medium",
                "issue": "Seu perfil D (dominante) pode atropelar pessoas mais lentas/cuidadosas.",
                "action": "Ao delegar, respeite o tempo de processamento de perfis C e S. Dê prazo +20% do que você faria."
            })

        # Recomendações de contratação baseadas em gaps
        current_arquetipos = [
            arquetipos.get("primary"),
            arquetipos.get("secondary"),
            arquetipos.get("tertiary")
        ]

        # Se busca Executores mas tem perfil E alto
        if "executor" in current_arquetipos and paei.get("e", 0) > 70:
            recommendations["contratacoes"].append({
                "area": "Complementaridade",
                "priority": "high",
                "issue": "Você busca Executores mas seu perfil é Empreendedor (ideias).",
                "action": "CRÍTICO: Contrate executores ANTES de novas ideias. Regra: para cada ideia nova, 1 executor precisa estar disponível."
            })

        # Se busca Organizadores mas não valoriza disciplina
        if "organizador" in current_arquetipos and valores.get("primary") != "disciplina":
            recommendations["contratacoes"].append({
                "area": "Valores Organizacionais",
                "priority": "medium",
                "issue": "Você busca organizadores mas não prioriza disciplina nos valores.",
                "action": "Para reter Organizadores, você precisa respeitar processos que eles criam. Não atropele estruturas que pediu para construírem."
            })

        return recommendations
