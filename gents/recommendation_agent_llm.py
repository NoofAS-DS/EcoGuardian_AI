from agents.llm_utils import call_llm_json

RECOMMENDATION_SCHEMA = {
    "type": "object",
    "properties": {
        "recommendation": {"type": "string"},
        "urgency": {"type": "string"},
        "send_alert": {"type": "boolean"}
    },
    "required": ["recommendation", "urgency", "send_alert"],
    "additionalProperties": False
}

def recommendation_agent_llm(site_row: dict, analysis_output: dict) -> dict:
    system_prompt = """
You are a sustainability recommendation agent.
Generate practical and operational recommendations.
Be specific, concise, and action-oriented.
Return only valid JSON.
""".strip()

    user_prompt = f"""
Site data:
{site_row}

Analysis output:
{analysis_output}

Decide:
1. What operational recommendation should be given?
2. What is the urgency? (Low, Medium, High)
3. Should an alert be sent? true or false

Important:
If environmental risk is clearly high, send_alert should be true.
""".strip()

    return call_llm_json(system_prompt, user_prompt, RECOMMENDATION_SCHEMA)
