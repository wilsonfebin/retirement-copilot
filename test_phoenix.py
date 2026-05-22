from phoenix.otel import register


tracer_provider = register(

    project_name="retirement-copilot"
)

tracer = tracer_provider.get_tracer(
    __name__
)


@tracer.chain
def test_function(name):

    return f"Hello {name}"


print(
    test_function("Febin")
)
