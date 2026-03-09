import pandas as pd

def classify_temperature(temp: float) -> str:
    if temp >= 40:
        return "Critical"
    if temp >= 35:
        return "High"
    if temp >= 30:
        return "Moderate"
    return "Normal"

def classify_humidity(humidity: float) -> str:
    if humidity <= 12:
        return "Critical Low"
    if humidity <= 20:
        return "Low"
    if humidity <= 30:
        return "Moderate"
    return "Good"

def classify_air_quality(aqi: float) -> str:
    if aqi >= 150:
        return "Very Poor"
    if aqi >= 120:
        return "Poor"
    if aqi >= 80:
        return "Moderate"
    return "Good"

def analysis_agent(df: pd.DataFrame) -> pd.DataFrame:
    analyzed = df.copy()

    analyzed["temperature_status"] = analyzed["temperature"].apply(classify_temperature)
    analyzed["humidity_status"] = analyzed["humidity"].apply(classify_humidity)
    analyzed["aqi_status"] = analyzed["air_quality_index"].apply(classify_air_quality)

    analyzed["analysis_summary"] = analyzed.apply(
        lambda row: (
            f"Temperature is {row['temperature_status']}, "
            f"humidity is {row['humidity_status']}, "
            f"and air quality is {row['aqi_status']}."
        ),
        axis=1
    )
    return analyzed
