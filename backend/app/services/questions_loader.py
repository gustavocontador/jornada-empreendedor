"""
Questions Loader - Carrega e cacheia perguntas do YAML.

Este módulo carrega o questionário completo do arquivo YAML e
mantém em cache para performance.
"""
import os
from typing import Dict, Any, List, Optional
import yaml
from pathlib import Path

# Cache global das perguntas
_QUESTIONS_CACHE: Optional[Dict[str, Any]] = None


def _load_yaml_file() -> Dict[str, Any]:
    """
    Carrega arquivo YAML do questionário.

    Returns:
        Dicionário com todo o conteúdo do YAML
    """
    # Caminho relativo ao backend
    yaml_path = Path(__file__).parent.parent.parent.parent.parent / "questions" / "questionario-completo-v1.yaml"

    if not yaml_path.exists():
        raise FileNotFoundError(f"Arquivo de perguntas não encontrado: {yaml_path}")

    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data


def get_questions_data() -> Dict[str, Any]:
    """
    Retorna dados completos do questionário (com cache).

    Returns:
        Dicionário com metadata, seções e perguntas
    """
    global _QUESTIONS_CACHE

    if _QUESTIONS_CACHE is None:
        _QUESTIONS_CACHE = _load_yaml_file()

    return _QUESTIONS_CACHE


def reload_questions() -> Dict[str, Any]:
    """
    Recarrega perguntas do arquivo YAML (ignora cache).

    Útil para desenvolvimento ou quando o YAML é atualizado.

    Returns:
        Dicionário com dados atualizados
    """
    global _QUESTIONS_CACHE
    _QUESTIONS_CACHE = _load_yaml_file()
    return _QUESTIONS_CACHE


def get_question_by_id(question_id: str) -> Optional[Dict[str, Any]]:
    """
    Busca pergunta específica por ID.

    Args:
        question_id: ID da pergunta (ex: 'q001', 'q042')

    Returns:
        Dicionário com dados da pergunta ou None se não encontrada
    """
    data = get_questions_data()
    perguntas = data.get("perguntas", [])

    for pergunta in perguntas:
        if pergunta.get("id") == question_id:
            return pergunta

    return None


def get_questions_by_section(section_id: str) -> List[Dict[str, Any]]:
    """
    Retorna todas as perguntas de uma seção específica.

    Args:
        section_id: ID da seção (ex: 'intro', 'comportamento_valores')

    Returns:
        Lista de perguntas da seção
    """
    data = get_questions_data()
    perguntas = data.get("perguntas", [])

    return [p for p in perguntas if p.get("secao") == section_id]


def get_sections() -> List[Dict[str, Any]]:
    """
    Retorna todas as seções do questionário.

    Returns:
        Lista de seções com metadata
    """
    data = get_questions_data()
    return data.get("secoes", [])


def get_metadata() -> Dict[str, Any]:
    """
    Retorna metadata do questionário.

    Returns:
        Dicionário com metadata (nome, versão, tempo estimado, etc.)
    """
    data = get_questions_data()
    return data.get("metadata", {})


def get_total_questions() -> int:
    """
    Retorna número total de perguntas.

    Returns:
        Número de perguntas no questionário
    """
    data = get_questions_data()
    return len(data.get("perguntas", []))
