import pandas as pd
from utils.sample_data import get_sample_environment_data

def collector_agent(uploaded_df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    إذا رفع المستخدم ملف CSV نستخدمه.
    غير ذلك نستخدم بيانات تجريبية.
    """
    if uploaded_df is not None and not uploaded_df.empty:
        return uploaded_df.copy()
    return get_sample_environment_data()
