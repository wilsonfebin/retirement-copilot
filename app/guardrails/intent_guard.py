
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
from openai import APIConnectionError

def classify_query_intent(query):

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            temperature=0,

            messages=[

                {
                    "role": "system",

                    "content": """

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
           response
           .choices[0]
           .message.content
           .strip()
           .upper()
        )

        print(
          f"Intent Classification: {result}"
        )  

        if "INVALID" in result:
            return False

        return True

    except APIConnectionError:

        print(
            "OpenAI connection failed "
            "during intent classification."
        )

        # =====================================================
        # FAIL OPEN
        # =====================================================

        return True

    except Exception as e:

        print(
            f"Intent classification error: {e}"
        )

        return True