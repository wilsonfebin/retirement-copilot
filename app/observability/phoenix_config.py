import os

from phoenix.otel import register

from opentelemetry import trace


ENABLE_PHOENIX = os.getenv(
    "ENABLE_PHOENIX",
    "false"
).lower() == "true"


if ENABLE_PHOENIX:

    tracer_provider = register(

        project_name="retirement-copilot",

        endpoint="http://localhost:4317",

        verbose=False
    )

    tracer = tracer_provider.get_tracer(
        __name__
    )

else:

    tracer = trace.get_tracer(
        __name__
    )


otel_tracer = trace.get_tracer(
    __name__
)


def initialize_phoenix():

    if ENABLE_PHOENIX:

        print(
            "Phoenix tracing initialized."
        )

    else:

        print(
            "Phoenix disabled."
        )