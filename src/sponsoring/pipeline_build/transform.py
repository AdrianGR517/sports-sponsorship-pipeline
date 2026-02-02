from src.sponsoring.pipeline_build.transformations import industries_cluster_pipeline, explode_all
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def build_transform(df):

    REQUIRED_COLUMNS = {'deal_id', 'deal_name', 'sport_fact', 'branding_fact', 'team_competition',
                        'industry', 'country', 'usd_value_total', 'usd_value_annual'}

    NUMERIC_COLS = {'usd_value_total', 'usd_value_annual'}

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

    df_transformed = pd.DataFrame()

    logger.info("Selecting only the relevant columns")
    
    df_transformed[['deal_name','deal_id','team_competition','usd_value_total','usd_value_annual']] = df[['deal_name','deal_id','team_competition','usd_value_total','usd_value_annual']]
    df_transformed['sport_fact']         = df.sport_fact.fillna('Soccer').str.split(" | ",regex=False)
    df_transformed['branding_fact']      = df.branding_fact.fillna('No branding').str.split(" | ",regex=False)
    df_transformed['country']       = df["hq_buyer"].replace('', pd.NA).combine_first(df["hq_seller"]).dropna().str.split(" | ",regex=False)

    logger.info("Grouping the industries in categories")

    df_transformed['industry']      = industries_cluster_pipeline(df.industry)

    logger.info("Removing the deals with zero usd_value_total")

    df_transformed_not_null = df_transformed[df_transformed.usd_value_total > 0]
    
    output_df = explode_all(df_transformed_not_null[['deal_id', 'deal_name', 'sport_fact', 'branding_fact', 'team_competition',
                                                     'industry', 'country', 'usd_value_total', 'usd_value_annual']])
    return(output_df)