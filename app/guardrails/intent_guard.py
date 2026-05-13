from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def classify_query_intent(query):

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        temperature=0,

        messages=[

            {
                "role": "system",
                "content": """
You are a retirement-domain intent classifier.

Classify whether the user query is broadly related to:
- retirement planning
- pension products
- retirement income
- financial planning
- investment planning
- retirement readiness
- pension suitability
- long-term savings

Allow niche or uncommon retirement-related Indian HDFC Bank scenarios.

Reject only clearly unrelated queries.

Return ONLY one word:

VALID
or
INVALID
"""
            },

            {
                "role": "user",
                "content": query
            }
        ]
    )

    result = (
        response.choices[0]
        .message.content
        .strip()
        .upper()
    )

    return result == "VALID"
