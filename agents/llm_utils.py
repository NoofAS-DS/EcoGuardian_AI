import json
import os
from openai import OpenAI

def call_llm_json(system_prompt: str, user_prompt: str, schema: dict, model: str = "gpt-4o-mini"):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "agent_output",
                "schema": schema,
                "strict": True,
            }
        },
    )

    return json.loads(response.output_text)
