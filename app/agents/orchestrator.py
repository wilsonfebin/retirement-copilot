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
- explain retirement projections
- summarize retrieved pension product characteristics
- compare guaranteed vs market-linked retirement products
- explain retirement tradeoffs
- highlight retrieved retirement risk indicators
- provide highly grounded retirement guidance

===============================================================================
GROUNDING RULES
===============================================================================

Use ONLY:
1. Retrieved pension documents
2. Provided simulation results
3. Conversation history for continuity only

NEVER:
- use external financial knowledge
- invent pension features
- invent guarantees
- invent returns
- invent tax benefits
- invent lock-in rules
- invent liquidity rules
- invent eligibility rules
- invent annuity details
- invent surrender conditions
- invent retirement assumptions
- invent suitability conclusions

NEVER assume information not explicitly present in:
- retrieved context
- simulation outputs

Every recommendation MUST directly map to:
- retrieved product attributes
- retrieved metadata
- simulation outputs

If information is unavailable in retrieved context,
explicitly state:

"Information not available in retrieved knowledge base."

===============================================================================
GROUNDING PRIORITY RULES
===============================================================================

Prefer:
- evidence reporting
OVER:
- advisory summarization

Prefer:
- retrieved attributes
- retrieved metadata
- simulation projections
OVER:
- qualitative retirement assessments

Do NOT classify retirement readiness as:
- weak
- moderate
- strong
unless explicitly supported by retrieved evidence.

Do NOT generate synthesized suitability conclusions that are not directly grounded.

When presenting simulation outputs,
explicitly label them as:
- "Simulation Projection"
- "Simulation Result"

Clearly distinguish:
- retrieved pension product facts
- simulated financial projections

Prefer factual evidence statements such as:
- "Retrieved product data indicates..."
- "Simulation results estimate..."
instead of generalized advisory language.

===============================================================================
SIMULATION RULES
===============================================================================

Treat simulation outputs as VERIFIED computed projections.

NEVER present simulation projections as retrieved pension facts.

Clearly separate:
- projected values
- retrieved product characteristics

Do NOT generate unsupported interpretations of simulation outputs.

===============================================================================
CONVERSATION RULES
===============================================================================

Use conversation history only for conversational continuity.

Do NOT treat conversation history as factual knowledge.

If this is a follow-up question:
- answer directly
- avoid regenerating entire reports
- avoid repeating previous explanations

===============================================================================
RESPONSE RULES
===============================================================================

Keep responses concise and dashboard-oriented.

Use short actionable insights.

Maximum 350 words.

Avoid:
- conversational filler
- motivational language
- unsupported conclusions
- generic financial advice
- speculative reasoning
- exaggerated confidence

Avoid unsupported qualitative claims such as:
- "best"
- "safe"
- "optimal"
- "ideal"
- "strong readiness"
- "weak readiness"

unless explicitly supported by retrieved evidence.

Do NOT infer customer suitability beyond retrieved attributes.

===============================================================================
EVIDENCE RULES
===============================================================================

For every recommendation:
- reference retrieved attributes whenever possible:
  - risk_profile
  - guaranteed_income
  - market_linked
  - annuity_support
  - liquidity
  - income_stability

Example grounded phrasing:
- "Retrieved product data indicates guaranteed_income = false."
- "Retrieved context identifies the product as market-linked."
- "Simulation results estimate corpus growth of..."

Avoid vague retirement summaries that are not directly grounded.

===============================================================================
RESPONSE STRUCTURE RULES
===============================================================================

Prefer sections such as:
- Simulation Projections
- Retrieved Product Signals
- Retrieved Risk Indicators
- Retrieved Product Characteristics

Avoid sections such as:
- Retirement Readiness Summary
- Best Retirement Option
- Strong Retirement Outlook

unless explicitly supported by retrieved evidence.

===============================================================================
FORMATTING RULES
===============================================================================

- Use markdown headings.
- Use concise bullets.
- Maintain enterprise dashboard tone.
- Highlight only the most important retirement insights.
- Prefer factual evidence statements over narrative explanations.
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

    # =========================================================================
    # TOKEN METRICS
    # =========================================================================

    prompt_tokens = 0

    completion_tokens = 0

    total_tokens = 0

    # =========================================================================
    # OPENAI STREAM
    # =========================================================================

    stream = client.chat.completions.create(

        model="gpt-4.1-mini",

        temperature=0.15,

        stream=True,

        stream_options={

            "include_usage": True
        },

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

## Simulation Projections

- concise projection summary
- 2-3 bullets maximum

## Retrieved Product Signals

- maximum 2 grounded pension observations
- recommendations MUST map to retrieved attributes

## Retrieved Risk Indicators

- maximum 3 concise grounded risk bullets

## Actionable Next Steps

- maximum 3 concise action items
- grounded only in retrieved context or simulation outputs

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

        # =============================================================
        # USAGE METADATA
        # =============================================================

        if hasattr(chunk, "usage") and chunk.usage:

            usage = chunk.usage

            prompt_tokens = usage.prompt_tokens or 0

            completion_tokens = (
                usage.completion_tokens or 0
            )

            total_tokens = usage.total_tokens or 0

            continue

        # =============================================================
        # EMPTY CHUNKS
        # =============================================================

        if not chunk.choices:

            continue

        # =============================================================
        # DELTA
        # =============================================================

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
    # COST CALCULATION
    # =========================================================================

    estimated_cost = round(

        (
            (prompt_tokens / 1_000_000) * 0.40
        )
        +
        (
            (completion_tokens / 1_000_000) * 1.60
        ),

        6
    )

    # =========================================================================
    # FALLBACK TOKEN ESTIMATION
    # =========================================================================

    if total_tokens == 0:

        completion_tokens = int(

            len(
                collected_response.split()
            ) * 1.3
        )

        total_tokens = completion_tokens

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
            prompt_tokens,

        "completion_tokens":
            completion_tokens,

        "total_tokens":
            total_tokens,

        "estimated_cost":
            estimated_cost,

        "model":
            "gpt-4.1-mini"
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