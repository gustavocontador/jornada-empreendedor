"""
Configuração de logging estruturado para observabilidade.

Implementa logging JSON estruturado em todos os pontos críticos da aplicação
para facilitar diagnóstico de erros e monitoramento.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configura logging estruturado em formato JSON.

    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Criar logger raiz
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remover handlers existentes
    logger.handlers.clear()

    # Criar handler para stdout
    handler = logging.StreamHandler(sys.stdout)

    # Formato JSON estruturado
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d',
        rename_fields={
            'asctime': 'timestamp',
            'levelname': 'level',
            'pathname': 'file',
            'lineno': 'line'
        }
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Log inicial
    logger.info(
        "Logging estruturado configurado",
        extra={"log_level": log_level, "format": "JSON"}
    )


def get_logger(name: str) -> logging.Logger:
    """
    Retorna logger configurado para um módulo específico.

    Args:
        name: Nome do módulo (geralmente __name__)

    Returns:
        Logger configurado
    """
    return logging.getLogger(name)
