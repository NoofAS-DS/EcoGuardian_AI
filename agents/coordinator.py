from .collector_agent import collector_agent
from .analysis_agent import analysis_agent
from .risk_agent import risk_agent
from .analysis_agent_llm import analysis_agent_llm
from .recommendation_agent_llm import recommendation_agent_llm
from .alert_message_agent_llm import alert_message_agent_llm
import pandas as pd

def coordinator_run(uploaded_df=None):
    df = collector_agent(uploaded_df)
    df = analysis_agent(df)
    df = risk_agent(df)

    result_rows = []

    for _, row in df.iterrows():
        site_row = row.to_dict()

        try:
            llm_analysis = analysis_agent_llm(site_row)
            llm_recommendation = recommendation_agent_llm(site_row, llm_analysis)
            llm_alert = alert_message_agent_llm(site_row, llm_analysis, llm_recommendation)

            site_row["llm_environmental_summary"] = llm_analysis.get("environmental_summary", "")
            site_row["llm_key_issues"] = " | ".join(llm_analysis.get("key_issues", []))
            site_row["llm_recommendation"] = llm_recommendation.get("recommendation", "")
            site_row["llm_urgency"] = llm_recommendation.get("urgency", "")
            site_row["send_alert"] = bool(
                site_row.get("risk_level") == "High" or llm_recommendation.get("send_alert", False)
            )
            site_row["alert_title"] = llm_alert.get("alert_title", "")
            site_row["alert_message"] = llm_alert.get("alert_message", "")
            site_row["llm_error"] = ""

        except Exception as e:
            site_row["llm_environmental_summary"] = ""
            site_row["llm_key_issues"] = ""
            site_row["llm_recommendation"] = ""
            site_row["llm_urgency"] = ""
            site_row["send_alert"] = bool(site_row.get("risk_level") == "High")
            site_row["alert_title"] = ""
            site_row["alert_message"] = ""
            site_row["llm_error"] = str(e)

        result_rows.append(site_row)

    result_df = pd.DataFrame(result_rows)

    if "send_alert" not in result_df.columns:
        result_df["send_alert"] = result_df["risk_level"].eq("High")

    return result_df
