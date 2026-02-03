import pandas as pd

def analyze_deals_by_industry_and_country(df : pd.DataFrame):

    REQUIRED_COLUMNS = {'deal_id','country','industry'}

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    deals_by_industry_and_country = (
    df
    .groupby(["industry","country"], as_index=False)
    .agg(total_deals=("deal_id","count"))
)

    return(deals_by_industry_and_country)