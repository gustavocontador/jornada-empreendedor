"""
Exemplo de uso dos calculadores de scoring.

Este arquivo demonstra como usar o ScoringEngine e os calculadores individuais.
"""
import yaml
from typing import Any
from uuid import uuid4
from datetime import datetime

# Mock de Response para exemplo
class MockResponse:
    def __init__(self, question_id: str, answer_value: Any):
        self.id = uuid4()
        self.question_id = question_id
        self.answer_value = answer_value
        self.answered_at = datetime.utcnow()


def create_sample_responses() -> list:
    """
    Cria respostas de exemplo para um empreendedor típico perfil Laranja/PAEI-E.

    Este perfil representa um empreendedor ambicioso, inovador,
    mas com dificuldades em organização e delegação.
    """
    responses = [
        # Seção Comportamento - Perfil D/I alto (assertivo e sociável)
        MockResponse("q006", 5),  # Agir rapidamente
        MockResponse("q007", 4),  # Assumir controle
        MockResponse("q008", 5),  # Frustra com burocracia
        MockResponse("q009", 4),  # Competir e ganhar
        MockResponse("q010", 4),  # Não tem medo de confrontos
        MockResponse("q011", 5),  # Bom em influenciar
        MockResponse("q012", 4),  # Networking
        MockResponse("q013", 5),  # Ambientes dinâmicos

        # Seção Comportamento - Perfil S/C baixo (pouca estabilidade/conformidade)
        MockResponse("q015", 2),  # Valoriza estabilidade (baixo)
        MockResponse("q019", 3),  # Precisão e detalhes (neutro)
        MockResponse("q020", 3),  # Analisar antes de decidir (neutro)
        MockResponse("q021", 2),  # Incomodado com desorganização (baixo)

        # Spiral Dynamics - Laranja alto (conquista, eficiência)
        MockResponse("q029", 5),  # Sucesso material
        MockResponse("q030", 5),  # Formas mais eficientes
        MockResponse("q031", 5),  # Progresso > Estabilidade

        # Spiral - Vermelho moderado (ação, poder)
        MockResponse("q023", 4),  # Respeito por resultados
        MockResponse("q024", 4),  # Ajo imediatamente
        MockResponse("q025", 3),  # Mundo como selva (neutro)

        # Spiral - Verde baixo (pouca colaboração igualitária)
        MockResponse("q032", 2),  # Ouvir todas vozes
        MockResponse("q033", 2),  # Trabalhar em equipe
        MockResponse("q034", 2),  # Bem-estar > lucro

        # PAEI - E alto (empreendedor)
        MockResponse("q051", 5),  # Penso em novos produtos
        MockResponse("q052", 5),  # Adapto estratégia rápido
        MockResponse("q053", 5),  # Tédio me assusta
        MockResponse("q054", 5),  # Vejo oportunidades
        MockResponse("q055", 4),  # Experimentar > aperfeiçoar

        # PAEI - P moderado (produtor)
        MockResponse("q041", 4),  # Satisfação em resultados
        MockResponse("q042", 4),  # Reuniões atrasam execução
        MockResponse("q043", 3),  # Fazer eu mesmo (neutro)

        # PAEI - A baixo (baixa administração)
        MockResponse("q046", 2),  # Processos para escalar
        MockResponse("q047", 2),  # Criar SOPs
        MockResponse("q048", 3),  # Analisar dados históricos
        MockResponse("q049", 2),  # Crescer devagar

        # PAEI - I baixo (baixa integração)
        MockResponse("q056", 2),  # Alinhar valores
        MockResponse("q057", 2),  # Clima > eficiência
        MockResponse("q058", 2),  # Decisões difíceis me drenam
        MockResponse("q060", 2),  # Engajamento > resultados

        # PAEI - Trade-offs (escolhas forçadas)
        MockResponse("q061", "e"),  # Priorizo: inovar
        MockResponse("q062", "e"),  # Contratação: inovador
        MockResponse("q063", "e"),  # Crise: pivotar

        # Eneagrama - Tipo 3 (realizador)
        MockResponse("q070", 5),  # Valor em resultados
        MockResponse("q071", 4),  # Medo de falhar

        # Eneagrama - Tipo 7 moderado (entusiasta)
        MockResponse("q077", 4),  # Novas experiências
        MockResponse("q078", 3),  # Evita sentimentos dolorosos

        # Eneagrama - Tipo 8 baixo
        MockResponse("q079", 3),  # Controle e vulnerabilidade

        # Valores - Ranking
        MockResponse("q086", ["crescimento", "inovacao", "resultado"]),

        # Arquetipos - Ranking
        MockResponse("q087", ["executor", "criativo", "vendedor"]),

        # Contexto financeiro
        MockResponse("q083", 3),  # Dificuldade precificar (neutro)
        MockResponse("q084", 4),  # Gastos impulsivos (alto)
        MockResponse("q085", 2),  # Evita números (baixo)
    ]

    return responses


def load_questions_data() -> dict[str, Any]:
    """
    Carrega dados do questionário.

    Em produção, isso viria do arquivo YAML.
    """
    # Simplificado para exemplo - em produção carrega do YAML
    return {
        "perguntas": [
            {
                "id": "q006",
                "tipo": "likert_5",
                "pontuacao": {
                    "disc_d": 1.0,
                    "paei_p": 0.6,
                    "paei_e": 0.3,
                    "enneagram_8": 0.4,
                    "spiral_red": 0.5,
                    "spiral_orange": 0.3
                }
            },
            # ... todas as outras perguntas
            # (em produção vem do arquivo completo)
        ]
    }


def example_full_calculation():
    """
    Exemplo de cálculo completo usando ScoringEngine.
    """
    from app.services.calculators import ScoringEngine

    print("=" * 80)
    print("EXEMPLO: Cálculo Completo de Assessment")
    print("=" * 80)

    # Cria respostas de exemplo
    responses = create_sample_responses()
    print(f"\n✓ {len(responses)} respostas carregadas")

    # Carrega questionário (em produção vem do YAML)
    questions_data = load_questions_data()
    print("✓ Questionário carregado")

    # Calcula todos os scores
    print("\n🔄 Calculando scores...")
    scores = ScoringEngine.calculate_all_scores(responses, questions_data)

    # Exibe resultados
    print("\n" + "=" * 80)
    print("RESULTADOS")
    print("=" * 80)

    # DISC
    disc = scores["disc"]
    print(f"\n📊 DISC Profile: {disc['profile']}")
    print(f"   D (Dominância):    {disc['d']:.1f}")
    print(f"   I (Influência):    {disc['i']:.1f}")
    print(f"   S (Estabilidade):  {disc['s']:.1f}")
    print(f"   C (Conformidade):  {disc['c']:.1f}")

    # Spiral Dynamics
    spiral = scores["spiral"]
    print(f"\n🌀 Spiral Dynamics: {spiral['primary'].upper()}")
    print(f"   Primário:   {spiral['primary']}")
    print(f"   Secundário: {spiral['secondary']}")
    print(f"   Terciário:  {spiral['tertiary']}")

    # PAEI
    paei = scores["paei"]
    print(f"\n⚙️  PAEI Code: {paei['code']}")
    print(f"   P (Producer):      {paei['p']:.1f}")
    print(f"   A (Administrator): {paei['a']:.1f}")
    print(f"   E (Entrepreneur):  {paei['e']:.1f}")
    print(f"   I (Integrator):    {paei['i']:.1f}")

    # Eneagrama
    enneagram = scores["enneagram"]
    print(f"\n🎭 Eneagrama: Tipo {enneagram['type']}")
    if enneagram.get("wing"):
        print(f"   Wing: {enneagram['wing']}")
    if enneagram.get("subtype"):
        print(f"   Subtype: {enneagram['subtype']}")

    # Valores
    valores = scores["valores"]
    print(f"\n💎 Valores Empresariais:")
    print(f"   1º {valores['primary']}")
    print(f"   2º {valores['secondary']}")
    print(f"   3º {valores['tertiary']}")

    # Arquetipos
    arquetipos = scores["arquetipos"]
    print(f"\n👥 Arquétipos de Contratação:")
    print(f"   1º {arquetipos['primary']}")
    print(f"   2º {arquetipos['secondary']}")
    print(f"   3º {arquetipos['tertiary']}")

    # Interpretações
    print("\n" + "=" * 80)
    print("INTERPRETAÇÕES")
    print("=" * 80)

    interpretations = scores["interpretations"]

    # Forças
    print("\n✅ FORÇAS:")
    for strength in interpretations.get("forcas", [])[:3]:
        print(f"\n   • {strength['area']}")
        print(f"     {strength['description']}")

    # Desafios
    print("\n⚠️  DESAFIOS:")
    for challenge in interpretations.get("desafios", [])[:3]:
        print(f"\n   • {challenge['area']}")
        print(f"     {challenge['description']}")
        print(f"     Solução: {challenge['solution']}")

    # Recomendações
    print("\n" + "=" * 80)
    print("RECOMENDAÇÕES")
    print("=" * 80)

    recommendations = scores["recommendations"]

    for area, recs in recommendations.items():
        if recs:
            print(f"\n📋 {area.replace('_', ' ').title()}:")
            for rec in recs[:2]:  # Primeiras 2
                print(f"\n   • {rec.get('area', rec.get('issue', 'N/A'))}")
                print(f"     {rec.get('action', rec.get('description', 'N/A'))}")


def example_individual_calculators():
    """
    Exemplo de uso de calculadores individuais.
    """
    from app.services.calculators import (
        calculate_disc,
        calculate_spiral,
        calculate_paei,
        calculate_enneagram,
        calculate_valores,
        calculate_arquetipos
    )

    print("\n" + "=" * 80)
    print("EXEMPLO: Calculadores Individuais")
    print("=" * 80)

    responses = create_sample_responses()
    questions_data = load_questions_data()

    # DISC apenas
    print("\n🔄 Calculando apenas DISC...")
    disc = calculate_disc(responses, questions_data)
    print(f"Perfil: {disc['profile']}")
    print(f"Descrição: {disc['description']}")

    # Spiral apenas
    print("\n🔄 Calculando apenas Spiral Dynamics...")
    spiral = calculate_spiral(responses, questions_data)
    print(f"Nível primário: {spiral['primary']}")
    if spiral.get("warnings"):
        print(f"Avisos: {len(spiral['warnings'])} conflito(s) detectado(s)")

    # PAEI apenas
    print("\n🔄 Calculando apenas PAEI...")
    paei = calculate_paei(responses, questions_data)
    print(f"Código: {paei['code']}")
    if paei.get("issues"):
        print(f"Problemas: {len(paei['issues'])} problema(s) detectado(s)")


def example_save_to_database():
    """
    Exemplo de como salvar resultados no banco de dados.
    """
    from app.services.calculators import ScoringEngine
    from app.models.result import Result
    from decimal import Decimal

    print("\n" + "=" * 80)
    print("EXEMPLO: Salvar no Banco de Dados")
    print("=" * 80)

    # Calcula scores
    responses = create_sample_responses()
    questions_data = load_questions_data()
    scores = ScoringEngine.calculate_all_scores(responses, questions_data)

    # Cria objeto Result
    result = Result(
        assessment_id=uuid4(),
        user_id=uuid4(),
        # DISC
        disc_d=Decimal(str(scores["disc"]["d"])),
        disc_i=Decimal(str(scores["disc"]["i"])),
        disc_s=Decimal(str(scores["disc"]["s"])),
        disc_c=Decimal(str(scores["disc"]["c"])),
        disc_profile=scores["disc"]["profile"],
        # Spiral Dynamics
        spiral_red=Decimal(str(scores["spiral"]["red"])),
        spiral_blue=Decimal(str(scores["spiral"]["blue"])),
        spiral_orange=Decimal(str(scores["spiral"]["orange"])),
        spiral_green=Decimal(str(scores["spiral"]["green"])),
        spiral_yellow=Decimal(str(scores["spiral"]["yellow"])),
        spiral_turquoise=Decimal(str(scores["spiral"]["turquoise"])),
        spiral_purple=Decimal(str(scores["spiral"]["purple"])),
        spiral_beige=Decimal(str(scores["spiral"]["beige"])),
        spiral_primary=scores["spiral"]["primary"],
        spiral_secondary=scores["spiral"]["secondary"],
        spiral_tertiary=scores["spiral"]["tertiary"],
        # PAEI
        paei_p=Decimal(str(scores["paei"]["p"])),
        paei_a=Decimal(str(scores["paei"]["a"])),
        paei_e=Decimal(str(scores["paei"]["e"])),
        paei_i=Decimal(str(scores["paei"]["i"])),
        paei_code=scores["paei"]["code"],
        # Eneagrama
        enneagram_type=scores["enneagram"]["type"],
        enneagram_wing=scores["enneagram"].get("wing"),
        enneagram_subtype=scores["enneagram"].get("subtype"),
        # Valores
        valores_primary=scores["valores"]["primary"],
        valores_secondary=scores["valores"]["secondary"],
        valores_tertiary=scores["valores"]["tertiary"],
        # Dados JSON
        arquetipos=scores["arquetipos"],
        interpretations=scores["interpretations"],
        recommendations=scores["recommendations"]
    )

    print("\n✓ Objeto Result criado")
    print(f"   DISC: {result.disc_profile}")
    print(f"   Spiral: {result.spiral_primary}")
    print(f"   PAEI: {result.paei_code}")
    print(f"   Eneagrama: Tipo {result.enneagram_type}")
    print(f"\n   (Pronto para db.add(result) e db.commit())")


if __name__ == "__main__":
    # Executa exemplos
    example_full_calculation()
    # example_individual_calculators()
    # example_save_to_database()
