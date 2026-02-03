import pandas as pd

def analyze_usd_by_industry_and_country(df : pd.DataFrame):

    REQUIRED_COLUMNS = {'deal_id','country','industry','usd_value_annual','usd_value_total'}

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    usd_by_country_and_industry = (
    df
    .groupby(["country","industry"], as_index=False)
    .agg(average_annual_amount=("usd_value_annual","mean"),
    total_usd_amount=("usd_value_total","sum"))
)

    return(usd_by_country_and_industry)