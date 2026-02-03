import pandas as pd

def analyze_summary(df : pd.DataFrame):


    REQUIRED_COLUMNS = {'deal_id','brand_name','team_name','usd_value_total'}

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )
    
    summary_df = pd.DataFrame()

    total_companies = df.brand_name.nunique()
    total_teams     = df.team_name.nunique()
    total_deals     = df.deal_id.nunique()
    total_usd       = df.drop_duplicates(subset=["deal_id"])["usd_value_total"].sum()

    summary_df['variable']  = ['companies', 'teams', 'deals', 'usd_invested']
    summary_df['totals']    = [total_companies, total_teams, total_deals, total_usd]

    return(summary_df)