import os
import streamlit as st

st.set_page_config(page_title="EcoGuardian AI", layout="wide")

if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

import pandas as pd
import plotly.express as px

from agents.coordinator import coordinator_run
from utils.n8n_utils import send_to_n8n

st.set_page_config(page_title="EcoGuardian AI", layout="wide")

if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.title("🌍 EcoGuardian AI")
st.subheader("AI Multi-Agent Sustainability Monitoring Dashboard")

if "result_df" not in st.session_state:
    st.session_state.result_df = None

uploaded_file = st.file_uploader("Upload environmental CSV file", type=["csv"])

uploaded_df = None
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

if st.button("Run Multi-Agent Analysis"):
    st.session_state.result_df = coordinator_run(uploaded_df)
    st.success("Analysis completed successfully")

result_df = st.session_state.result_df

if result_df is not None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Sites", len(result_df))
    col2.metric("High Risk Sites", int((result_df["risk_level"] == "High").sum()))
    col3.metric("Average Risk Score", round(result_df["risk_score"].mean(), 1))

    st.markdown("## Results Table")
    st.dataframe(result_df, width="stretch")

    st.markdown("## Risk by Site")
    fig = px.bar(result_df, x="site", y="risk_score", color="risk_level")
    st.plotly_chart(fig, width="stretch")

    st.markdown("## Site Analysis")
    for _, row in result_df.iterrows():
        st.markdown(f"### {row['site']}")
        st.write(f"**Rule-Based Risk Level:** {row['risk_level']}")
        st.write(f"**Rule-Based Summary:** {row['analysis_summary']}")

        if "llm_environmental_summary" in result_df.columns:
            st.write(f"**LLM Environmental Summary:** {row['llm_environmental_summary']}")

        if "llm_key_issues" in result_df.columns:
            st.write(f"**LLM Key Issues:** {row['llm_key_issues']}")

        if "llm_recommendation" in result_df.columns:
            st.write(f"**LLM Recommendation:** {row['llm_recommendation']}")

        if "llm_urgency" in result_df.columns:
            st.write(f"**LLM Urgency:** {row['llm_urgency']}")

        if "alert_title" in result_df.columns:
            st.write(f"**Alert Title:** {row['alert_title']}")

        if "alert_message" in result_df.columns:
            st.write(f"**Alert Message:** {row['alert_message']}")

        if row["send_alert"]:
            st.warning("Alert should be sent for this site")

    st.markdown("## Send Alerts")
    webhook_url = st.secrets.get("N8N_WEBHOOK_URL", "")
    st.write("Webhook URL loaded:", bool(webhook_url))

    if st.button("Send High Risk Alerts to n8n"):
        if not webhook_url:
            st.error("N8N_WEBHOOK_URL is missing in secrets")
        else:
            alerts = result_df[result_df["send_alert"] == True]

            payload_columns = ["site", "risk_score", "risk_level", "send_alert"]

            optional_columns = [
                "llm_environmental_summary",
                "llm_recommendation",
                "alert_title",
                "alert_message",
            ]

            for col in optional_columns:
                if col in alerts.columns:
                    payload_columns.append(col)

            payload = {
                "project": "EcoGuardian AI",
                "total_sites": len(result_df),
                "high_risk_sites": alerts[payload_columns].to_dict(orient="records")
            }

            st.write("Payload being sent:")
            st.json(payload)

            result = send_to_n8n(payload, webhook_url)

            st.write("Response status:", result["status_code"])
            st.write("Response text:", result["response_text"])

            if result["status_code"] in [200, 201]:
                st.success("Data sent to n8n successfully")
            else:
                st.error(f"Failed to send data to n8n: {result['response_text']}")
