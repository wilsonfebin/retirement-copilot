from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

client = OpenAI()


SYSTEM_PROMPT = """
You are an AI Retirement Planning CoPilot for HDFC Bank.

Your responsibilities:
- recommend suitable retirement products
- explain retirement readiness
- compare guaranteed vs market-linked plans
- explain financial tradeoffs

Grounding Rules:
- ONLY use retrieved pension documents
- ONLY use provided simulation results
- NEVER use external financial knowledge
- NEVER invent pension features, guarantees, returns, tax benefits, or eligibility rules
- NEVER assume details not explicitly present in retrieved context
- if information is unavailable in retrieved documents,
  explicitly say:
  "I could not find this information in the retrieved pension documents."

Conversation Rules:
- use conversation history only for conversational continuity
- do not rely on memory as factual source
- always prioritize retrieved documents and simulation outputs
- if the query is a follow-up question,
  answer directly without regenerating full reports
- avoid repeating previous explanations

Response Rules:
- keep answers concise and practical
- use short paragraphs
- use bullet points where useful
- avoid repetition
- avoid lengthy financial disclaimers
- keep total response under 500 words
- keep follow-up answers under 150 words
- focus on actionable retirement guidance grounded in retrieved documents

Accuracy Rules:
- do not invent financial numbers
- do not generalize retirement advice
- do not generate unsupported pension comparisons
- every recommendation must be supported by retrieved context
- if retrieved context is insufficient,
  clearly acknowledge the limitation

Use ONLY:
1. Retrieved pension context
2. Simulation results
3. Conversation history for contextual understanding
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

METADATA:
{doc.metadata}

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

        if plan_name not in plans:

            plans.append(plan_name)

    return plans


# =============================================================================
# STREAMING RESPONSE
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

        temperature=0.2,

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

Generate a retirement response STRICTLY using:

1. Retrieved pension context
2. Simulation results
3. Conversation history for conversational continuity

Do NOT use external financial knowledge.

If information is missing from retrieved documents,
explicitly say:
"I could not find this information in the retrieved pension documents."

STRICT FORMAT:
1. Retirement readiness summary
2. Top recommended plans
3. Key retirement risks
4. Actionable next steps

Rules:
- maximum 400-500 words
- short paragraphs
- bullet points preferred
- avoid repeating numbers
- avoid generic financial disclaimers

If this is a follow-up question:
- answer directly
- avoid full report regeneration
- keep response concise
- reference previous retirement analysis
"""
            }
        ]
    )

    collected_response = ""

    for chunk in stream:

        delta = chunk.choices[0].delta

        if delta.content:

            collected_response += delta.content

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
        len(collected_response.split()) * 1.3
    )

    estimated_cost = round(
        (estimated_tokens / 1_000_000) * 1.60,
        6
    )

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