# =============================================================================
# app/observability/phoenix_config.py
# =============================================================================

import os

from opentelemetry import trace


# =============================================================================
# ENABLE FLAG
# =============================================================================

ENABLE_PHOENIX = os.getenv(

    "ENABLE_PHOENIX",

    "false"

).lower() == "true"


# =============================================================================
# PHOENIX ENABLED
# =============================================================================

if ENABLE_PHOENIX:

    from phoenix.otel import register

    tracer_provider = register(

        project_name="retirement-copilot",

        endpoint="http://localhost:4317",

        verbose=False
    )

    tracer = tracer_provider.get_tracer(
        __name__
    )

    otel_tracer = trace.get_tracer(
        __name__
    )


# =============================================================================
# PHOENIX DISABLED
# =============================================================================

else:

    otel_tracer = trace.get_tracer(
        __name__
    )

    class NoOpTracer:

        def chain(self, func):

            return func

    tracer = NoOpTracer()


# =============================================================================
# INITIALIZER
# =============================================================================

def initialize_phoenix():

    if ENABLE_PHOENIX:

        print(
            "Phoenix tracing initialized."
        )

    else:

        print(
            "Phoenix disabled."
        )