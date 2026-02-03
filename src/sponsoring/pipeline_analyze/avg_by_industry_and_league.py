import pandas as pd

def analyze_avg_usd_by_industry_and_league(df : pd.DataFrame):

    REQUIRED_COLUMNS = {'deal_id','industry','competition','usd_value_annual'}

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    avg_usd_by_industry_and_league = (
    df
    .groupby(["industry","competition"], as_index=False)
    .agg(average_annual_amount=("usd_value_annual","mean"))
)

    return(avg_usd_by_industry_and_league)