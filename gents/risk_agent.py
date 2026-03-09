import pandas as pd

def risk_agent(df: pd.DataFrame) -> pd.DataFrame:
    risk_scores = []
    risk_levels = []

    for _, row in df.iterrows():

        score = 0

        # Temperature
        if row["temperature"] >= 40:
            score += 40
        elif row["temperature"] >= 35:
            score += 25
        elif row["temperature"] >= 30:
            score += 10

        # Humidity
        if row["humidity"] <= 15:
            score += 25
        elif row["humidity"] <= 30:
            score += 15

        # Air Quality
        if row["air_quality_index"] >= 150:
            score += 20
        elif row["air_quality_index"] >= 100:
            score += 10

        # Vegetation stress
        if row["vegetation_index"] < 0.3:
            score += 10

        # Wind impact
        if row["wind_speed"] > 20:
            score += 5

        # Determine risk level
        if score >= 70:
            level = "High"
        elif score >= 40:
            level = "Medium"
        else:
            level = "Low"

        risk_scores.append(score)
        risk_levels.append(level)

    df["risk_score"] = risk_scores
    df["risk_level"] = risk_levels

    return df
