"""
Configuração do Sentry para error tracking em tempo real.

Captura exceções não tratadas, erros de performance e contexto completo
para diagnóstico rápido de problemas em produção.
"""
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import logging

logger = logging.getLogger(__name__)


def init_sentry(dsn: str = None, environment: str = "development", traces_sample_rate: float = 1.0) -> None:
    """
    Inicializa Sentry para error tracking.

    Args:
        dsn: Sentry DSN (Data Source Name) - obter em sentry.io
        environment: Ambiente (development, staging, production)
        traces_sample_rate: Taxa de amostragem de traces (0.0 a 1.0)
    """
    if not dsn:
        logger.warning(
            "Sentry DSN não configurado. Error tracking desabilitado.",
            extra={"environment": environment}
        )
        return

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        traces_sample_rate=traces_sample_rate,
        integrations=[
            FastApiIntegration(transaction_style="url"),
            SqlalchemyIntegration(),
        ],
        # Capturar informações de requisições
        send_default_pii=False,  # Não enviar PII por padrão (LGPD/GDPR)
        # Configurações de performance
        profiles_sample_rate=1.0 if environment == "development" else 0.1,
        # Antes de enviar evento, adicionar contexto customizado
        before_send=before_send_handler,
    )

    logger.info(
        "Sentry inicializado",
        extra={
            "environment": environment,
            "traces_sample_rate": traces_sample_rate,
            "dsn_configured": bool(dsn)
        }
    )


def before_send_handler(event, hint):
    """
    Handler executado antes de enviar evento ao Sentry.

    Adiciona contexto customizado e filtra eventos desnecessários.

    Args:
        event: Evento do Sentry
        hint: Informações adicionais do evento

    Returns:
        Event modificado ou None para ignorar evento
    """
    # Adicionar contexto customizado
    if 'exception' in hint:
        exc = hint['exception']
        event['contexts'] = event.get('contexts', {})
        event['contexts']['custom'] = {
            'exception_type': type(exc).__name__,
            'exception_module': type(exc).__module__,
        }

    # Filtrar exceções conhecidas/esperadas (se necessário)
    # Exemplo: if event.get('exception', {}).get('values', [{}])[0].get('type') == 'HTTPException':
    #     return None  # Não enviar ao Sentry

    return event


def capture_message(message: str, level: str = "info", **extra_context):
    """
    Captura mensagem customizada no Sentry.

    Args:
        message: Mensagem a ser capturada
        level: Nível de severidade (info, warning, error, fatal)
        **extra_context: Contexto adicional a ser anexado
    """
    with sentry_sdk.push_scope() as scope:
        for key, value in extra_context.items():
            scope.set_context(key, value)

        sentry_sdk.capture_message(message, level)


def capture_exception(exception: Exception, **extra_context):
    """
    Captura exceção no Sentry com contexto adicional.

    Args:
        exception: Exceção a ser capturada
        **extra_context: Contexto adicional a ser anexado
    """
    with sentry_sdk.push_scope() as scope:
        for key, value in extra_context.items():
            scope.set_context(key, value)

        sentry_sdk.capture_exception(exception)
