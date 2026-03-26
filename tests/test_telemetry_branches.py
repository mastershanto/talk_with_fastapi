from __future__ import annotations

from fastapi import FastAPI

import app.core.telemetry as telemetry


def test_init_telemetry_skips_tracing_when_disabled(monkeypatch) -> None:
    called = {"logging": 0, "tracing": 0}

    monkeypatch.setattr(telemetry, "_configure_logging", lambda: called.__setitem__("logging", called["logging"] + 1))
    monkeypatch.setattr(telemetry, "_configure_tracing", lambda: called.__setitem__("tracing", called["tracing"] + 1))
    monkeypatch.setattr(telemetry.settings, "OTEL_ENABLED", False)

    telemetry.init_telemetry(FastAPI())

    assert called["logging"] == 1
    assert called["tracing"] == 0


def test_init_telemetry_enables_instrumentation_when_enabled(monkeypatch) -> None:
    called = {"tracing": 0, "fastapi": 0, "sqlalchemy": 0}

    monkeypatch.setattr(telemetry.settings, "OTEL_ENABLED", True)
    monkeypatch.setattr(telemetry, "_configure_logging", lambda: None)
    monkeypatch.setattr(telemetry, "_configure_tracing", lambda: called.__setitem__("tracing", called["tracing"] + 1))

    monkeypatch.setattr(
        telemetry.FastAPIInstrumentor,
        "instrument_app",
        lambda app, tracer_provider=None: called.__setitem__("fastapi", called["fastapi"] + 1),
    )
    monkeypatch.setattr(
        telemetry.SQLAlchemyInstrumentor,
        "instrument",
        lambda self, engine: called.__setitem__("sqlalchemy", called["sqlalchemy"] + 1),
    )

    telemetry.init_telemetry(FastAPI())

    assert called["tracing"] == 1
    assert called["fastapi"] == 1
    assert called["sqlalchemy"] == 1


def test_configure_tracing_uses_console_exporter_when_no_endpoint(monkeypatch) -> None:
    called = {"console": 0, "otlp": 0}

    class DummyProvider:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def add_span_processor(self, processor) -> None:
            self.processor = processor

    monkeypatch.setattr(telemetry.settings, "OTEL_SAMPLE_RATE", 0.25)
    monkeypatch.setattr(telemetry.settings, "OTEL_EXPORTER_OTLP_ENDPOINT", None)
    monkeypatch.setattr(telemetry, "TracerProvider", lambda **kwargs: DummyProvider(**kwargs))
    monkeypatch.setattr(telemetry.trace, "set_tracer_provider", lambda provider: None)
    monkeypatch.setattr(telemetry, "BatchSpanProcessor", lambda exporter: exporter)

    def _console_exporter() -> object:
        called["console"] += 1
        return object()

    def _otlp_exporter(endpoint: str | None = None) -> object:
        called["otlp"] += 1
        return object()

    monkeypatch.setattr(telemetry, "ConsoleSpanExporter", _console_exporter)
    monkeypatch.setattr(telemetry, "OTLPSpanExporter", _otlp_exporter)

    telemetry._configure_tracing()

    assert called["console"] == 1
    assert called["otlp"] == 0


def test_configure_tracing_uses_otlp_exporter_when_endpoint_set(monkeypatch) -> None:
    called = {"console": 0, "otlp": 0}

    class DummyProvider:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def add_span_processor(self, processor) -> None:
            self.processor = processor

    monkeypatch.setattr(telemetry.settings, "OTEL_SAMPLE_RATE", 0.25)
    monkeypatch.setattr(telemetry.settings, "OTEL_EXPORTER_OTLP_ENDPOINT", "http://collector:4318/v1/traces")
    monkeypatch.setattr(telemetry, "TracerProvider", lambda **kwargs: DummyProvider(**kwargs))
    monkeypatch.setattr(telemetry.trace, "set_tracer_provider", lambda provider: None)
    monkeypatch.setattr(telemetry, "BatchSpanProcessor", lambda exporter: exporter)

    def _console_exporter() -> object:
        called["console"] += 1
        return object()

    def _otlp_exporter(endpoint: str | None = None) -> object:
        called["otlp"] += 1
        return object()

    monkeypatch.setattr(telemetry, "ConsoleSpanExporter", _console_exporter)
    monkeypatch.setattr(telemetry, "OTLPSpanExporter", _otlp_exporter)

    telemetry._configure_tracing()

    assert called["console"] == 0
    assert called["otlp"] == 1
