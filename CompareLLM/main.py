from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import os
import json

load_dotenv()

# Clients
openai_client = OpenAI()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# 🔹 OpenAI Response
def get_openai_response(query):
    response = openai_client.chat.completions.create(
        model="gpt-4.1", messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content.strip()


# 🔹 Gemini Response
def get_gemini_response(query):
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=query)
    return response.text


# 🔥 Judge Model
def judge_responses(query, openai_res, gemini_res):
    judge_prompt = f"""
    You are an AI judge.

    Compare the two responses for the given query and decide:
    1. Which answer is more correct
    2. Which has better reasoning
    3. Final best answer

    Return ONLY JSON:
    {{
        "winner": "openai" or "gemini",
        "reason": "short explanation",
        "final_answer": "best combined answer"
    }}

    Query: {query}

    OpenAI Response:
    {openai_res}

    Gemini Response:
    {gemini_res}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": judge_prompt}],
    )

    return json.loads(response.choices[0].message.content)


# 🔥 MAIN FLOW
query = input("👉 Enter your query: ")

openai_output = get_openai_response(query)
gemini_output = get_gemini_response(query)

print("\n🧠 OpenAI:\n", openai_output)
print("\n🧪 Gemini:\n", gemini_output)

judgement = judge_responses(query, openai_output, gemini_output)

print("\n⚖️ Judge Decision:")
print("Winner:", judgement["winner"])
print("Reason:", judgement["reason"])
print("Final Answer:", judgement["final_answer"])
