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

        llm_analysis = analysis_agent_llm(site_row)
        llm_recommendation = recommendation_agent_llm(site_row, llm_analysis)
        llm_alert = alert_message_agent_llm(site_row, llm_analysis, llm_recommendation)

        site_row["llm_environmental_summary"] = llm_analysis["environmental_summary"]
        site_row["llm_key_issues"] = " | ".join(llm_analysis["key_issues"])
        site_row["llm_recommendation"] = llm_recommendation["recommendation"]
        site_row["llm_urgency"] = llm_recommendation["urgency"]
        site_row["send_alert"] = bool(
            site_row["risk_level"] == "High" or llm_recommendation["send_alert"]
        )
        site_row["alert_title"] = llm_alert["alert_title"]
        site_row["alert_message"] = llm_alert["alert_message"]

        result_rows.append(site_row)

    return pd.DataFrame(result_rows)
