import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_llm_json(system_prompt: str, user_prompt: str, schema: dict, model: str = "gpt-5"):
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
