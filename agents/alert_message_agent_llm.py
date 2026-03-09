from agents.llm_utils import call_llm_json

ALERT_SCHEMA = {
    "type": "object",
    "properties": {
        "alert_title": {"type": "string"},
        "alert_message": {"type": "string"}
    },
    "required": ["alert_title", "alert_message"],
    "additionalProperties": False
}

def alert_message_agent_llm(site_row: dict, analysis_output: dict, recommendation_output: dict) -> dict:
    system_prompt = """
You are an alert message agent.
Write a short professional alert title and message for operations teams.
Return only valid JSON.
""".strip()

    user_prompt = f"""
Create an alert message for this site.

Site data:
{site_row}

Analysis:
{analysis_output}

Recommendation:
{recommendation_output}
""".strip()

    return call_llm_json(system_prompt, user_prompt, ALERT_SCHEMA)
