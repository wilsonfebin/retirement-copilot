# =============================================================================
# app/agents/orchestrator.py
# =============================================================================

from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

client = OpenAI()


# =============================================================================
# SYSTEM PROMPT
# =============================================================================

SYSTEM_PROMPT = """
You are an enterprise-grade AI Retirement Planning CoPilot for HDFC Bank.

Your responsibilities:
- explain retirement readiness
- recommend suitable pension products
- compare guaranteed vs market-linked plans
- explain retirement tradeoffs
- summarize retirement risks
- provide grounded retirement guidance

Grounding Rules:
- ONLY use retrieved pension documents
- ONLY use provided simulation results
- NEVER use external financial knowledge
- NEVER invent pension features, guarantees, tax benefits, returns, lock-ins, or eligibility rules
- NEVER assume information not explicitly present in retrieved context
- prioritize factual grounding over conversational creativity

Conversation Rules:
- use conversation history only for conversational continuity
- do not use memory as factual knowledge
- always prioritize retrieved pension context and simulation outputs
- if this is a follow-up question,
  answer directly without regenerating the entire report
- avoid repeating previous explanations

Response Rules:
- keep responses concise and dashboard-oriented
- avoid long paragraphs
- use short actionable insights
- maximum 350 words
- avoid repetition
- avoid unnecessary disclaimers
- avoid generic financial advice
- provide the best grounded answer possible

Formatting Rules:
- use markdown headings
- use concise bullets
- maintain enterprise dashboard tone
- highlight only the most important retirement insights

Accuracy Rules:
- do not invent financial calculations
- do not generate unsupported retirement assumptions
- do not generate unsupported pension comparisons
- every recommendation must be supported by retrieved documents or simulation results
- if retrieved context is partially insufficient,
  briefly acknowledge limitations

Use ONLY:
1. Retrieved pension context
2. Simulation results
3. Conversation history for continuity
"""


# =============================================================================
# FILTER DETECTION
# =============================================================================

def detect_filters(query):

    query_lower = query.lower()

    guaranteed = (
        "guaranteed" in query_lower
    )

    market_linked = (
        "market linked" in query_lower
    )

    # =========================================================================
    # SINGLE FILTER
    # =========================================================================

    if guaranteed and not market_linked:

        return {
            "guaranteed_income": True
        }

    elif market_linked and not guaranteed:

        return {
            "market_linked": True
        }

    # =========================================================================
    # BOTH PRESENT → NO FILTER
    # =========================================================================

    return None


# =============================================================================
# BUILD CONTEXT
# =============================================================================

def build_context(documents):

    context_parts = []

    for i, doc in enumerate(documents):

        context_parts.append(

            f"""
DOCUMENT {i + 1}

SOURCE:
{doc.metadata.get("source")}

CONTENT:
{doc.page_content}
"""
        )

    return "\n\n".join(context_parts)


# =============================================================================
# EXTRACT PLAN NAMES
# =============================================================================

def extract_recommended_plans(documents):

    plans = []

    for doc in documents:

        source = doc.metadata.get(
            "source",
            ""
        )

        plan_name = (

            source
            .replace(".md", "")
            .replace("_", " ")
            .title()
        )

        if (
            plan_name
            and
            plan_name not in plans
        ):

            plans.append(plan_name)

    return plans


# =============================================================================
# STREAM RESPONSE
# =============================================================================

def stream_response(

    query,

    retrieval_context,

    simulation_result,

    conversation_history=""
):

    start_time = time.time()

    stream = client.chat.completions.create(

        model="gpt-4.1-mini",

        temperature=0.15,

        stream=True,

        messages=[

            {
                "role": "system",

                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",

                "content": f"""
CONVERSATION HISTORY:
{conversation_history}

CURRENT USER QUERY:
{query}

SIMULATION RESULT:
{simulation_result}

RETRIEVED PENSION CONTEXT:
{retrieval_context}

Generate a concise enterprise-style retirement response.

STRICT OUTPUT FORMAT:

## Retirement Readiness Summary

- concise readiness summary
- 2-3 bullets maximum

## Top Recommended Plans

- maximum 2 pension recommendations
- recommendations MUST be grounded in retrieved context

## Key Retirement Risks

- maximum 3 bullets
- mention only relevant risks

## Actionable Next Steps

- maximum 3 concise action items

IMPORTANT RULES:

- avoid repeating numbers excessively
- avoid long explanations
- avoid generic financial education
- avoid unsupported pension claims
- use concise dashboard-style insights
- prioritize clarity over verbosity
- do not regenerate full reports for follow-up questions
- if retrieved context is insufficient,
  acknowledge briefly and continue with grounded insights
"""
            }
        ]
    )

    collected_response = ""

    # =========================================================================
    # STREAMING
    # =========================================================================

    for chunk in stream:

        delta = chunk.choices[0].delta

        if delta.content:

            collected_response += (
                delta.content
            )

            yield {

                "type": "content",

                "chunk":
                    delta.content,

                "full_response":
                    collected_response
            }

    end_time = time.time()

    backend_time = round(

        end_time - start_time,

        2
    )

    # =========================================================================
    # TOKEN ESTIMATION
    # =========================================================================

    estimated_tokens = int(

        len(
            collected_response.split()
        ) * 1.3
    )

    estimated_cost = round(

        (estimated_tokens / 1_000_000)
        * 1.60,

        6
    )

    # =========================================================================
    # FINAL EVENT
    # =========================================================================

    yield {

        "type": "complete",

        "generated_response":
            collected_response,

        "backend_time":
            backend_time,

        "prompt_tokens":
            0,

        "completion_tokens":
            estimated_tokens,

        "total_tokens":
            estimated_tokens,

        "estimated_cost":
            estimated_cost
    }

    # =============================================================================
# NON-STREAMING RESPONSE
# =============================================================================

def generate_response(

    query,

    retrieval_context,

    simulation_result,

    conversation_history=""
):

    full_response = ""

    for event in stream_response(

        query=query,

        retrieval_context=retrieval_context,

        simulation_result=simulation_result,

        conversation_history=conversation_history
    ):

        if event["type"] == "content":

            full_response = event[
                "full_response"
            ]

    return full_response