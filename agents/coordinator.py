from .collector_agent import collector_agent
from .analysis_agent import analysis_agent
from .risk_agent import risk_agent


def coordinator_run(uploaded_df=None):
    df = collector_agent(uploaded_df)
    df = analysis_agent(df)
    df = risk_agent(df)
    return df
