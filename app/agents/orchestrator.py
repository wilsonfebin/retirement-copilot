from openai import OpenAI

from app.rag.retriever import retrieve_documents
from app.agents.simulation_agent import run_retirement_simulation
from app.observability.traces import logger
from app.utils.helpers import format_retirement_response

client = OpenAI()


SYSTEM_PROMPT = """
You are an AI Retirement Planning CoPilot for HDFC Bank.

Your responsibilities:
- recommend suitable retirement products
- explain retirement readiness
- compare guaranteed vs market-linked plans
- explain financial tradeoffs
- remain grounded in retrieved pension knowledge
- avoid hallucinations

Always:
- explain suitability
- explain retirement gaps
- explain investment risks
- provide practical recommendations

Do not invent financial numbers.
Use only provided simulation results and retrieved context.
"""


def detect_filters(query):

    query_lower = query.lower()

    filters = {}

    if "guaranteed" in query_lower:
        filters["guaranteed_income"] = True

    if "market linked" in query_lower:
        filters["market_linked"] = True

    return filters


def build_context(documents):

    context_parts = []

    for i, doc in enumerate(documents):

        context_parts.append(
            f"""
DOCUMENT {i + 1}

SOURCE:
{doc.metadata.get("source")}

METADATA:
{doc.metadata}

CONTENT:
{doc.page_content}
"""
        )

    return "\n\n".join(context_parts)


def extract_recommended_plans(documents):

    plans = []

    for doc in documents:

        source = doc.metadata.get("source", "")

        plan_name = (
            source
            .replace(".md", "")
            .replace("_", " ")
            .title()
        )

        if plan_name not in plans:
            plans.append(plan_name)

    return plans


def generate_response(
    query,
    retrieval_context,
    simulation_result
):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
USER QUERY:
{query}

SIMULATION RESULT:
{simulation_result}

RETRIEVED PENSION CONTEXT:
{retrieval_context}

Generate:
1. Retirement readiness assessment
2. Pension projection explanation
3. Suitable pension plan recommendations
4. Gap analysis if retirement target is weak
5. Actionable recommendations
"""
            }
        ]
    )

    return response.choices[0].message.content


def run_retirement_copilot():

    query = """
    I am 52 years old with ₹35L corpus and ₹35K monthly SIP.
    I want guaranteed retirement income at age 60.
    Which pension plans are suitable for me?
    """

    logger.info(f"Received query: {query}")

    filters = detect_filters(query)

    logger.info(f"Applied filters: {filters}")

    documents = retrieve_documents(
        query=query,
        filters=filters,
        k=4
    )

    logger.info(f"Retrieved {len(documents)} documents")

    retrieval_context = build_context(documents)

    recommended_plans = extract_recommended_plans(documents)

    logger.info(f"Recommended plans: {recommended_plans}")

    simulation_result = run_retirement_simulation(
        current_age=52,
        retirement_age=60,
        current_corpus=3500000,
        monthly_investment=35000,
        annual_return=0.10
    )

    logger.info("Simulation completed")

    generated_response = generate_response(
        query=query,
        retrieval_context=retrieval_context,
        simulation_result=simulation_result
    )

    logger.info("Generated final retirement copilot response")

    formatted_response = format_retirement_response(
        simulation_result=simulation_result,
        recommended_plans=recommended_plans,
        generated_response=generated_response
    )

    logger.info("Formatted structured response")

    return formatted_response