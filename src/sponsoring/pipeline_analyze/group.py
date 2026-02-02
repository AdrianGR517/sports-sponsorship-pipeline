import pandas as pd
import logging

logger = logging.getLogger(__name__)


def analyze_group(df):

    REQUIRED_COLUMNS = {'deal_id', 'industry', 'country', 'usd_value_total', 'usd_value_annual'}

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )
    
    df_by_id = (
        df
        .groupby("deal_id", as_index=False)
        .agg(country=("country", "first"),
            industry=("industry", "first"),
            usd_value_total=("usd_value_total", "first"),
            usd_value_annual=("usd_value_annual","first"))
    )

    df_grouped = (
    df_by_id
    .groupby(["country", "industry"], as_index=False)
    .agg(total_usd_amount=("usd_value_total", "sum"),
         avg_annual_usd_amount=("usd_value_annual","mean"))
    )

    return(df_grouped)