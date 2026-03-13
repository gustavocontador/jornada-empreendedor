"""
Renderizador de HTML para PDF usando WeasyPrint.
"""
from weasyprint import HTML, CSS
from pathlib import Path
import os


def render_pdf_from_html(html_content: str, output_path: str) -> str:
    """
    Renderiza HTML para PDF usando WeasyPrint.

    Args:
        html_content: Conteúdo HTML completo (com CSS inline ou externo)
        output_path: Caminho completo onde o PDF será salvo

    Returns:
        Caminho do arquivo PDF gerado
    """
    # Garantir que o diretório de output existe
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Converter HTML para PDF
    html_obj = HTML(string=html_content)
    html_obj.write_pdf(output_path)

    return output_path


def render_pdf_with_custom_css(
    html_content: str,
    output_path: str,
    css_path: str = None
) -> str:
    """
    Renderiza HTML para PDF com CSS customizado adicional.

    Args:
        html_content: Conteúdo HTML completo
        output_path: Caminho completo onde o PDF será salvo
        css_path: Caminho para arquivo CSS adicional (opcional)

    Returns:
        Caminho do arquivo PDF gerado
    """
    # Garantir que o diretório de output existe
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Preparar stylesheets
    stylesheets = []
    if css_path and os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
            stylesheets.append(CSS(string=css_content))

    # Converter HTML para PDF
    html_obj = HTML(string=html_content)
    html_obj.write_pdf(output_path, stylesheets=stylesheets)

    return output_path


# Configurações padrão para PDF
PDF_CONFIG = {
    'page_size': 'A4',
    'margin_top': '1.5cm',
    'margin_right': '1.5cm',
    'margin_bottom': '1.5cm',
    'margin_left': '1.5cm',
    'encoding': 'utf-8'
}
