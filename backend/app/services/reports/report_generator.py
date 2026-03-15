"""
Report Generator - Motor principal de geração de relatórios PDF.

Orquestra a geração de relatórios simplificados (2-3 páginas) e completos (15-20 páginas)
usando os frameworks DISC, Spiral Dynamics, PAEI, Eneagrama e Valores.
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from sqlalchemy.orm import Session

from app.models.result import Result
from app.models.user import User
from app.services.reports.chart_generator import (
    generate_disc_chart,
    generate_spiral_chart,
    generate_paei_chart,
    generate_enneagram_diagram,
    generate_valores_chart
)
from app.services.reports.pdf_renderer import render_pdf_from_html
from app.services.reports.content_generator import (
    generate_disc_content,
    generate_spiral_content,
    generate_paei_content,
    generate_enneagram_content,
    generate_valores_content,
    generate_integrated_content,
    generate_action_plan
)


# Diretórios
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = Path(os.getenv("REPORTS_OUTPUT_DIR", "/tmp/reports"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class ReportGenerator:
    """Gerador de relatórios PDF personalizados."""

    def __init__(self, db: Session):
        self.db = db

    def generate_simplified_report(self, result_id: str, user_id: str) -> str:
        """
        Gera relatório simplificado (2-3 páginas) e retorna path do PDF.

        Args:
            result_id: ID do resultado
            user_id: ID do usuário

        Returns:
            Path completo do arquivo PDF gerado
        """
        # Buscar dados
        result = self.db.query(Result).filter(Result.id == result_id).first()
        if not result:
            raise ValueError(f"Result {result_id} não encontrado")

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} não encontrado")

        # Extrair scores do JSON
        scores = result.scores
        disc_scores = scores.get("disc", {})
        spiral_scores = scores.get("spiral", {})
        paei_scores = scores.get("paei", {})
        enneagram_scores = scores.get("enneagram", {})
        valores_scores = scores.get("valores", {})

        # Gerar gráficos
        charts = self._generate_charts(scores)

        # Preparar dados para o template
        template_data = {
            "user_name": user.name,
            "assessment_date": result.calculated_at.strftime("%d/%m/%Y"),

            # CSS
            "css_content": self._load_css(),

            # DISC
            "disc_profile": disc_scores.get("profile", ""),
            "disc_description": self._get_disc_short_description(disc_scores.get("profile", "")),
            "disc_profile_title": self._get_disc_profile_title(disc_scores.get("profile", "")),
            "disc_profile_summary": self._get_disc_profile_summary(disc_scores.get("profile", "")),
            "disc_traits": self._format_list_items(self._get_disc_traits(disc_scores)),
            "disc_chart": charts["disc"],

            # Espiral
            "spiral_profile": self._format_spiral_colors(spiral_scores),
            "spiral_description": self._get_spiral_short_description(spiral_scores),
            "spiral_colors": self._format_spiral_colors_text(spiral_scores),
            "spiral_primary": spiral_scores.get("primary", "orange").capitalize(),
            "spiral_secondary": spiral_scores.get("secondary", "blue").capitalize(),
            "spiral_primary_pct": self._get_percentage(spiral_scores, spiral_scores.get("primary", "orange")),
            "spiral_secondary_pct": self._get_percentage(spiral_scores, spiral_scores.get("secondary", "blue")),
            "spiral_combination_summary": self._get_spiral_combination_summary(spiral_scores),
            "spiral_meaning": self._format_list_items(self._get_spiral_meaning(spiral_scores)),
            "spiral_chart": charts["spiral"],

            # PAEI
            "paei_code": paei_scores.get("code", ""),
            "paei_profile_name": self._get_paei_profile_name(paei_scores.get("code", "")),
            "paei_interpretation": self._get_paei_interpretation(paei_scores.get("code", "")),
            "paei_p_score": round(paei_scores.get("P", 0), 1),
            "paei_a_score": round(paei_scores.get("A", 0), 1),
            "paei_e_score": round(paei_scores.get("E", 0), 1),
            "paei_i_score": round(paei_scores.get("I", 0), 1),
            "paei_p_desc": self._get_paei_role_desc("P", paei_scores.get("P", 0)),
            "paei_a_desc": self._get_paei_role_desc("A", paei_scores.get("A", 0)),
            "paei_e_desc": self._get_paei_role_desc("E", paei_scores.get("E", 0)),
            "paei_i_desc": self._get_paei_role_desc("I", paei_scores.get("I", 0)),
            "paei_chart": charts["paei"],

            # Eneagrama
            "enneagram_type": enneagram_scores.get("type", 3),
            "enneagram_name": self._get_enneagram_name(enneagram_scores.get("type", 3)),
            "enneagram_shadow": self._get_enneagram_shadow(enneagram_scores.get("type", 3)),
            "enneagram_motivations": self._format_list_items(
                self._get_enneagram_motivations(enneagram_scores.get("type", 3))
            ),
            "enneagram_chart": charts["enneagram"],

            # Valores
            "top_values": self._format_ordered_list(
                self._get_top_values(valores_scores, 3)
            ),
        }

        # Carregar template
        template_path = TEMPLATES_DIR / "simplified_template.html"
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Substituir placeholders
        html_content = self._render_template(template_content, template_data)

        # Gerar PDF
        output_filename = f"relatorio_simplificado_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = OUTPUT_DIR / output_filename

        render_pdf_from_html(html_content, str(output_path))

        return str(output_path)

    def generate_complete_report(self, result_id: str, user_id: str) -> str:
        """
        Gera relatório completo (15-20 páginas) e retorna path do PDF.

        Args:
            result_id: ID do resultado
            user_id: ID do usuário

        Returns:
            Path completo do arquivo PDF gerado
        """
        # Buscar dados
        result = self.db.query(Result).filter(Result.id == result_id).first()
        if not result:
            raise ValueError(f"Result {result_id} não encontrado")

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} não encontrado")

        # Extrair scores
        scores = result.scores
        disc_scores = scores.get("disc", {})
        spiral_scores = scores.get("spiral", {})
        paei_scores = scores.get("paei", {})
        enneagram_scores = scores.get("enneagram", {})
        valores_scores = scores.get("valores", {})
        arquetipos_scores = scores.get("arquetipos", {})

        # Gerar gráficos
        charts = self._generate_charts(scores)

        # Gerar conteúdo detalhado de cada seção
        disc_content = generate_disc_content(disc_scores)
        spiral_content = generate_spiral_content(spiral_scores)
        paei_content = generate_paei_content(paei_scores)
        enneagram_content = generate_enneagram_content(enneagram_scores)
        valores_content = generate_valores_content(valores_scores, arquetipos_scores)
        integrated_content = generate_integrated_content(disc_scores, spiral_scores, paei_scores, enneagram_scores)
        action_plan = generate_action_plan(disc_scores, spiral_scores, paei_scores, enneagram_scores)

        # Preparar dados para o template
        template_data = {
            "user_name": user.name,
            "assessment_date": result.calculated_at.strftime("%d/%m/%Y às %H:%M"),
            "css_content": self._load_css(),

            # Gráficos
            "disc_chart": charts["disc"],
            "spiral_chart": charts["spiral"],
            "paei_chart": charts["paei"],
            "enneagram_chart": charts["enneagram"],
            "valores_chart": charts["valores"],

            # Conteúdo DISC detalhado
            **disc_content,

            # Conteúdo Espiral detalhado
            **spiral_content,

            # Conteúdo PAEI detalhado
            **paei_content,

            # Conteúdo Eneagrama detalhado
            **enneagram_content,

            # Conteúdo Valores
            **valores_content,

            # Síntese integrada
            **integrated_content,

            # Plano de ação
            **action_plan,
        }

        # Carregar template
        template_path = TEMPLATES_DIR / "complete_template.html"
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Substituir placeholders
        html_content = self._render_template(template_content, template_data)

        # Gerar PDF
        output_filename = f"relatorio_completo_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = OUTPUT_DIR / output_filename

        render_pdf_from_html(html_content, str(output_path))

        return str(output_path)

    def _generate_charts(self, scores: dict[str, Any]) -> dict[str, str]:
        """
        Gera todos os gráficos em base64 para embedding no HTML.

        Args:
            scores: Dicionário com todos os scores

        Returns:
            Dicionário com gráficos em base64
        """
        charts = {}

        # DISC
        disc_scores = scores.get("disc", {})
        if disc_scores:
            charts["disc"] = generate_disc_chart({
                "D": disc_scores.get("D", 0),
                "I": disc_scores.get("I", 0),
                "S": disc_scores.get("S", 0),
                "C": disc_scores.get("C", 0)
            })

        # Espiral
        spiral_scores = scores.get("spiral", {})
        if spiral_scores:
            charts["spiral"] = generate_spiral_chart({
                "beige": spiral_scores.get("beige", 0),
                "purple": spiral_scores.get("purple", 0),
                "red": spiral_scores.get("red", 0),
                "blue": spiral_scores.get("blue", 0),
                "orange": spiral_scores.get("orange", 0),
                "green": spiral_scores.get("green", 0),
                "yellow": spiral_scores.get("yellow", 0),
                "turquoise": spiral_scores.get("turquoise", 0)
            })

        # PAEI
        paei_scores = scores.get("paei", {})
        if paei_scores:
            charts["paei"] = generate_paei_chart({
                "P": paei_scores.get("P", 0),
                "A": paei_scores.get("A", 0),
                "E": paei_scores.get("E", 0),
                "I": paei_scores.get("I", 0)
            })

        # Eneagrama
        enneagram_scores = scores.get("enneagram", {})
        if enneagram_scores:
            charts["enneagram"] = generate_enneagram_diagram(
                enneagram_scores.get("type", 3),
                enneagram_scores.get("wing")
            )

        # Valores
        valores_scores = scores.get("valores", {})
        if valores_scores:
            # Converter para formato esperado pelo gerador
            valores_dict = {k: v for k, v in valores_scores.items() if k not in ["primary", "secondary", "tertiary"]}
            charts["valores"] = generate_valores_chart(valores_dict, top_n=5)

        return charts

    def _load_css(self) -> str:
        """Carrega o CSS dos templates."""
        css_path = TEMPLATES_DIR / "styles.css"
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()

    def _render_template(self, template: str, data: dict[str, Any]) -> str:
        """
        Substitui placeholders no template pelos valores reais.

        Args:
            template: String do template HTML
            data: Dicionário com dados para substituição

        Returns:
            HTML renderizado
        """
        result = template
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            # Converter None para string vazia
            str_value = "" if value is None else str(value)
            result = result.replace(placeholder, str_value)

        return result

    # ===== MÉTODOS DE CONTEÚDO (Relatório Simplificado) =====

    def _get_disc_short_description(self, profile: str) -> str:
        """Retorna descrição curta do perfil DISC."""
        descriptions = {
            "D": "Líder Decisivo",
            "I": "Influenciador Carismático",
            "S": "Estabilizador Confiável",
            "C": "Analista Preciso",
            "DI": "Líder Persuasivo",
            "DC": "Comandante Estratégico",
            "DS": "Diretor Paciente",
            "ID": "Inspirador Audacioso",
            "IS": "Conselheiro Empático",
            "IC": "Comunicador Analítico",
            "SI": "Apoiador Entusiasta",
            "SD": "Executor Fiel",
            "SC": "Especialista Dedicado",
            "CD": "Arquiteto Decisivo",
            "CI": "Especialista Persuasivo",
            "CS": "Perfeccionista Meticuloso"
        }
        return descriptions.get(profile, "Perfil Balanceado")

    def _get_disc_profile_title(self, profile: str) -> str:
        """Retorna título expandido do perfil DISC."""
        return self._get_disc_short_description(profile)

    def _get_disc_profile_summary(self, profile: str) -> str:
        """Retorna resumo do perfil DISC."""
        summaries = {
            "D": "Você é orientado a resultados, decisivo e direto. Gosta de desafios e de estar no controle.",
            "I": "Você é sociável, otimista e persuasivo. Inspira pessoas e cria conexões naturalmente.",
            "S": "Você é paciente, leal e cooperativo. Valoriza estabilidade e harmonia no ambiente.",
            "C": "Você é analítico, preciso e sistemático. Valoriza qualidade e precisão.",
            "DI": "Você combina assertividade com carisma. É um líder que influencia e motiva pessoas.",
            "DC": "Você é estratégico e objetivo. Toma decisões baseadas em dados e executa com precisão.",
            "IS": "Você é empático e comunicativo. Cria relacionamentos profundos e ambientes acolhedores.",
            "CS": "Você é confiável e meticuloso. Entrega consistência com atenção aos detalhes."
        }
        return summaries.get(profile, "Você possui um perfil equilibrado entre as diferentes dimensões do DISC.")

    def _get_disc_traits(self, disc_scores: dict[str, Any]) -> list:
        """Retorna lista de traços principais do perfil DISC."""
        traits = []
        profile = disc_scores.get("profile", "")

        if "D" in profile:
            traits.append("Decisivo e orientado a resultados")
            traits.append("Assume riscos calculados")
            traits.append("Direto na comunicação")

        if "I" in profile:
            traits.append("Carismático e persuasivo")
            traits.append("Networking natural")
            traits.append("Entusiasta e otimista")

        if "S" in profile:
            traits.append("Leal e confiável")
            traits.append("Paciente e cooperativo")
            traits.append("Valoriza estabilidade")

        if "C" in profile:
            traits.append("Analítico e preciso")
            traits.append("Atenção aos detalhes")
            traits.append("Valoriza qualidade")

        return traits if traits else ["Perfil balanceado em todas as dimensões"]

    def _format_spiral_colors(self, spiral_scores: dict[str, Any]) -> str:
        """Formata as cores da espiral."""
        primary = spiral_scores.get("primary", "orange").capitalize()
        secondary = spiral_scores.get("secondary", "blue").capitalize()
        return f"{primary}-{secondary}"

    def _format_spiral_colors_text(self, spiral_scores: dict[str, Any]) -> str:
        """Formata texto das cores."""
        return self._format_spiral_colors(spiral_scores)

    def _get_percentage(self, spiral_scores: dict[str, Any], color: str) -> str:
        """Calcula percentual de uma cor."""
        score = spiral_scores.get(color, 0)
        total = sum([spiral_scores.get(c, 0) for c in ["beige", "purple", "red", "blue", "orange", "green", "yellow", "turquoise"]])
        if total == 0:
            return "0"
        pct = (score / total) * 100
        return f"{pct:.0f}"

    def _get_spiral_short_description(self, spiral_scores: dict[str, Any]) -> str:
        """Descrição curta da combinação Espiral."""
        primary = spiral_scores.get("primary", "orange")
        secondary = spiral_scores.get("secondary", "blue")

        names = {
            "orange-blue": "Empreendedor Estruturado",
            "orange-green": "Inovador Consciente",
            "blue-orange": "Gestor Inovador",
            "red-orange": "Guerreiro Estratégico",
            "green-yellow": "Humanista Sistêmico",
            "yellow-turquoise": "Visionário Integrador"
        }

        key = f"{primary}-{secondary}"
        return names.get(key, "Perfil Multidimensional")

    def _get_spiral_combination_summary(self, spiral_scores: dict[str, Any]) -> str:
        """Resumo da combinação de cores da Espiral."""
        primary = spiral_scores.get("primary", "orange")
        secondary = spiral_scores.get("secondary", "blue")

        summaries = {
            "orange": "focado em inovação, crescimento e resultados mensuráveis",
            "blue": "valoriza estrutura, processos e disciplina",
            "green": "prioriza pessoas, propósito e impacto social",
            "red": "assertivo, com energia para conquistar e vencer",
            "yellow": "pensamento sistêmico e integração de múltiplas perspectivas",
            "purple": "valoriza relacionamentos, tradições e cultura forte"
        }

        return f"Você é {summaries.get(primary, 'equilibrado')} ({primary.capitalize()}), com influência de {summaries.get(secondary, 'outros valores')} ({secondary.capitalize()})."

    def _get_spiral_meaning(self, spiral_scores: dict[str, Any]) -> list:
        """Significado das cores dominantes."""
        primary = spiral_scores.get("primary", "orange")
        meanings = {
            "orange": [
                "Busca constante por inovação e melhoria",
                "Decisões baseadas em dados e métricas",
                "Foco em crescimento e escala do negócio"
            ],
            "blue": [
                "Valorização de processos e sistemas",
                "Planejamento de longo prazo",
                "Disciplina e consistência na execução"
            ],
            "green": [
                "Preocupação genuína com bem-estar da equipe",
                "Decisões considerando impacto social",
                "Cultura organizacional forte e inclusiva"
            ],
            "red": [
                "Coragem para tomar decisões difíceis",
                "Energia alta e disposição para 'guerrear'",
                "Assertividade em negociações"
            ]
        }
        return meanings.get(primary, ["Valores equilibrados em múltiplas dimensões"])

    def _get_paei_profile_name(self, code: str) -> str:
        """Nome do perfil PAEI."""
        names = {
            "Paei": "Produtor Solitário",
            "pAei": "Burocrata",
            "paEi": "Inventor (Arsonista)",
            "paeI": "Superfollower",
            "PAei": "Executor",
            "PaEi": "Visionário Desorganizado",
            "PaeI": "Líder de Torcida",
            "pAEi": "Falso Empreendedor",
            "pAeI": "Administrador Político",
            "paEI": "Demagogo",
            "PAEi": "Empreendedor",
            "PAeI": "Estadista",
            "PaEI": "Desenvolvedor",
            "pAEI": "Missionário",
            "PAEI": "Líder Completo"
        }
        return names.get(code, "Perfil Único")

    def _get_paei_interpretation(self, code: str) -> str:
        """Interpretação curta do código PAEI."""
        interpretations = {
            "Paei": "Você foca em produzir resultados, mas pode ter dificuldade com processos, inovação e pessoas.",
            "PaEi": "Você é forte em resultados e inovação, mas pode precisar de ajuda com processos e gestão de pessoas.",
            "PAEi": "Você é um empreendedor completo - produz, organiza e inova. Pode precisar trabalhar mais a integração da equipe.",
            "PAEI": "Você possui todos os papéis bem desenvolvidos - um líder completo e raro."
        }
        return interpretations.get(code, "Seu perfil de gestão possui características únicas que combinam diferentes papéis organizacionais.")

    def _get_paei_role_desc(self, role: str, score: float) -> str:
        """Descrição curta de cada papel PAEI."""
        if score >= 7:
            level = "Alto"
        elif score >= 4:
            level = "Médio"
        else:
            level = "Baixo"

        descriptions = {
            "P": {
                "Alto": "Você entrega resultados consistentemente",
                "Médio": "Você produz, mas pode melhorar a consistência",
                "Baixo": "Você pode ter dificuldade em executar e entregar"
            },
            "A": {
                "Alto": "Você tem processos e sistemas bem estabelecidos",
                "Médio": "Você tem alguma estrutura, mas pode melhorar",
                "Baixo": "Você pode ser desorganizado e caótico"
            },
            "E": {
                "Alto": "Você é altamente inovador e visionário",
                "Médio": "Você inova ocasionalmente",
                "Baixo": "Você pode resistir a mudanças e inovação"
            },
            "I": {
                "Alto": "Você é excelente em integrar e desenvolver pessoas",
                "Médio": "Você se importa com pessoas, mas pode melhorar",
                "Baixo": "Você pode ter dificuldade com gestão de pessoas"
            }
        }

        return descriptions.get(role, {}).get(level, "")

    def _get_enneagram_name(self, type_num: int) -> str:
        """Nome do tipo do Eneagrama."""
        names = {
            1: "O Perfeccionista",
            2: "O Ajudador",
            3: "O Realizador",
            4: "O Individualista",
            5: "O Investigador",
            6: "O Leal",
            7: "O Entusiasta",
            8: "O Desafiador",
            9: "O Pacificador"
        }
        return names.get(type_num, "Tipo Único")

    def _get_enneagram_shadow(self, type_num: int) -> str:
        """Padrões de sombra/autossabotagem do Eneagrama."""
        shadows = {
            3: "Você pode se sabotar ao focar excessivamente em imagem e aparências, negligenciando autenticidade. O medo de fracasso pode levá-lo a workaholismo e burnout.",
            1: "Perfeccionismo paralisante e crítica interna severa podem impedir ação. Você pode se sabotar ao nunca considerar algo 'bom o suficiente'.",
            8: "Tendência a dominar e controlar pode afastar pessoas-chave. Dificuldade em mostrar vulnerabilidade pode impedir conexões profundas."
        }
        return shadows.get(type_num, "Cada tipo tem padrões inconscientes que podem limitar crescimento.")

    def _get_enneagram_motivations(self, type_num: int) -> list:
        """Motivações core do tipo Eneagrama."""
        motivations = {
            3: [
                "Ser visto como bem-sucedido e admirado",
                "Alcançar metas e superar expectativas",
                "Evitar fracasso e rejeição"
            ],
            1: [
                "Fazer o que é certo e correto",
                "Melhorar a si mesmo e ao mundo",
                "Evitar erros e imperfeições"
            ],
            8: [
                "Estar no controle e ser forte",
                "Proteger a si mesmo e aos outros",
                "Evitar vulnerabilidade e fraqueza"
            ]
        }
        return motivations.get(type_num, ["Motivações únicas do seu tipo"])

    def _get_top_values(self, valores_scores: dict[str, Any], n: int = 3) -> list:
        """Retorna top N valores ordenados."""
        # Filtrar apenas os valores (excluir metadata como primary, secondary)
        valores_only = {k: v for k, v in valores_scores.items() if k not in ["primary", "secondary", "tertiary"]}

        # Ordenar por score
        sorted_valores = sorted(valores_only.items(), key=lambda x: x[1], reverse=True)[:n]

        return [{"name": v[0], "score": round(v[1], 1)} for v in sorted_valores]

    def _format_list_items(self, items: list) -> str:
        """Formata lista de items como HTML <li>."""
        return "\n".join([f"<li>{item}</li>" for item in items])

    def _format_ordered_list(self, items: list) -> str:
        """Formata lista ordenada com valores."""
        html_items = []
        for item in items:
            if isinstance(item, dict):
                html_items.append(f"<li><strong>{item['name']}</strong> ({item['score']}/10)</li>")
            else:
                html_items.append(f"<li>{item}</li>")
        return "\n".join(html_items)
