from phoenix.otel import register

from opentelemetry import trace


# =============================================================================
# REGISTER PHOENIX
# =============================================================================

tracer_provider = register(

    project_name="retirement-copilot",

    endpoint="http://localhost:4317"
)


# =============================================================================
# OPENINFERENCE TRACER
# =============================================================================

tracer = tracer_provider.get_tracer(
    __name__
)


# =============================================================================
# OPENTELEMETRY TRACER
# =============================================================================

otel_tracer = trace.get_tracer(
    __name__
)


# =============================================================================
# INITIALIZER
# =============================================================================

def initialize_phoenix():

    print(
        "Phoenix tracing initialized."
    )

    return tracer