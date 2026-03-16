"""Telemetry and structured logging setup.

This module is intentionally lightweight: it configures structured JSON logs and
initializes OpenTelemetry tracing (OTLP exporter by default) when enabled.

Usage:
    from app.telemetry import init_telemetry
    init_telemetry(app)
"""

from __future__ import annotations

import logging

from pythonjsonlogger.json import JsonFormatter
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SpanExporter
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from fastapi import FastAPI

from app.config import settings
from app.database import engine


def _configure_logging() -> None:
    """Configure JSON structured logging for all application logs."""

    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"levelname": "severity"},
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Instrument logging so spans show trace_id / span_id
    LoggingInstrumentor().instrument(set_logging_format=False)


def _configure_tracing() -> None:
    """Configure OpenTelemetry tracing."""

    # Use OpenTelemetry resource to enrich traces with service metadata
    resource = Resource.create(
        {
            "service.name": settings.OTEL_SERVICE_NAME,
            "deployment.environment": settings.ENVIRONMENT,
        }
    )

    # Use sampling ratio to avoid high volume in prod.
    sampler = TraceIdRatioBased(settings.OTEL_SAMPLE_RATE)

    provider = TracerProvider(resource=resource, sampler=sampler)
    trace.set_tracer_provider(provider)

    # OTLP exporter if configured, otherwise console exporter as fallback.
    endpoint = settings.OTEL_EXPORTER_OTLP_ENDPOINT
    exporter: SpanExporter
    if endpoint:
        exporter = OTLPSpanExporter(endpoint=endpoint)
    else:
        exporter = ConsoleSpanExporter()

    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)


def init_telemetry(app: FastAPI) -> None:
    """Initialize structured logs + OpenTelemetry instrumentation."""

    # Always configure structured logs.
    _configure_logging()

    # Only enable tracing if explicitly enabled.
    if not settings.OTEL_ENABLED:
        logging.getLogger(__name__).debug("OpenTelemetry disabled via settings")
        return

    _configure_tracing()

    # Instrument FastAPI / Starlette and SQLAlchemy for automatic spans
    FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())
    SQLAlchemyInstrumentor().instrument(engine=engine)
