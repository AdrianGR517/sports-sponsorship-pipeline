from src.sponsoring.pipeline_build.transformations import industries_cluster_pipeline
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def build_transform(df):

    REQUIRED_COLUMNS = {'deal_id','brand_name','team_name','industry','hq_seller','hq_buyer','team_competition',
                        'branding_fact','status','partnership_type','length','usd_value_annual','usd_value_total'}

    NUMERIC_COLS = {'length','usd_value_total', 'usd_value_annual'}

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )
    
    for col in NUMERIC_COLS:
        converted = pd.to_numeric(df[col], errors="coerce")

        # Valores que no se pudieron convertir
        n_invalid = converted.isna().sum()

        if n_invalid > 0:
            raise ValueError(
                f"Column '{col}' must contain numeric values"
            )

    logger.info("Cleaning the outliers")

    df0 = df[df['usd_value_total'] > 0]
    df1 = df0[df0['usd_value_annual'] < 1e10]

    df_transformed = pd.DataFrame()

    logger.info("Selecting only the relevant columns")
    
    df_transformed[['deal_id','brand_name','team_name','deal_type','deal_status','length']] = (
    df1[['deal_id','brand_name','team_name','partnership_type','status','length']]
    )
    df_transformed['branding']      = df1.branding_fact.fillna('No branding').str.split(" | ",regex=False)
    df_transformed['competition']   = df1.team_competition
    df_transformed['industry']      = industries_cluster_pipeline(df1.industry)
    df_transformed['country']       = df1["hq_buyer"].replace('', pd.NA).combine_first(df1["hq_seller"]).dropna().str.split(" | ",regex=False)
    df_transformed[['usd_value_annual','usd_value_total']]      = df1[['usd_value_annual','usd_value_total']]
    logger.info("Grouping the industries in categories")

    df_transformed['industry']      = industries_cluster_pipeline(df1.industry)
    
    return(df_transformed)