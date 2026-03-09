from agents.llm_utils import call_llm_json

ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "environmental_summary": {"type": "string"},
        "key_issues": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["environmental_summary", "key_issues"],
    "additionalProperties": False
}

def analysis_agent_llm(site_row: dict) -> dict:
    system_prompt = """
You are an environmental analysis agent.
Analyze environmental site conditions clearly and professionally.
Focus on heat stress, humidity stress, air quality, and vegetation condition.
Return only valid JSON.
""".strip()

    user_prompt = f"""
Analyze this site:

Site: {site_row['site']}
Temperature: {site_row['temperature']}
Humidity: {site_row['humidity']}
Air Quality Index: {site_row['air_quality_index']}
Wind Speed: {site_row['wind_speed']}
Vegetation Index: {site_row['vegetation_index']}
Rule-based temperature status: {site_row.get('temperature_status', '')}
Rule-based humidity status: {site_row.get('humidity_status', '')}
Rule-based AQI status: {site_row.get('aqi_status', '')}
Rule-based risk level: {site_row.get('risk_level', '')}
Rule-based risk score: {site_row.get('risk_score', '')}
""".strip()

    return call_llm_json(system_prompt, user_prompt, ANALYSIS_SCHEMA)
