import pandas as pd
from datetime import datetime

def collector_agent(uploaded_df: pd.DataFrame | None = None) -> pd.DataFrame:
    if uploaded_df is not None and not uploaded_df.empty:
        return uploaded_df.copy()

    data = [
        {
            "site": "Abha Farm",
            "timestamp": datetime.now().isoformat(),
            "temperature": 38,
            "humidity": 15,
            "air_quality_index": 115,
            "wind_speed": 18,
            "vegetation_index": 0.31,
        },
        {
            "site": "Riyadh Site",
            "timestamp": datetime.now().isoformat(),
            "temperature": 42,
            "humidity": 10,
            "air_quality_index": 135,
            "wind_speed": 22,
            "vegetation_index": 0.24,
        },
        {
            "site": "Jazan Farm",
            "timestamp": datetime.now().isoformat(),
            "temperature": 34,
            "humidity": 28,
            "air_quality_index": 90,
            "wind_speed": 12,
            "vegetation_index": 0.45,
        },
    ]

    return pd.DataFrame(data)
