from src.sponsoring.pipeline_build.load import build_load
from src.sponsoring.pipeline_build.merge import build_merge
from src.sponsoring.pipeline_build.transform import build_transform
from pathlib import Path
from datetime import datetime
import pandas as pd
import logging

ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

logger = logging.getLogger(__name__)


def run_build(route, source = 'folder', id_col = 'deal_id', out_dir = Path("out")):
    out_path = out_dir / f"build_{ts}" 
    out_path.mkdir(parents=True, exist_ok=True)

    # Pipeline
    dfs_loaded      = build_load(route=route, source=source)
    df_merged       = build_merge(dfs_loaded, column_merge=id_col)
    df_transformed  = build_transform(df_merged)

    columns_to_explode = [c for c in df_transformed.columns if type(df_transformed.loc[0,c]) in (list, set)]
    columns_main = [id_col] + [c for c in df_transformed.columns if c not in columns_to_explode and c != id_col]

    logger.info("Saving to %s", out_path)

    main_df = df_transformed[columns_main]
    out_file_main = out_path / "main.csv"
    main_df.to_csv(out_file_main, index=False)

    for col in columns_to_explode:
        bridge_df = df_transformed[[id_col,col]].explode(col)
        out_file_bridge = out_path / f"bridge_{col}.csv"
        bridge_df.to_csv(out_file_bridge, index=False)


    # Creating the country-industry bridge table
    
    country_industry_df = df_transformed[['deal_id','country','industry']].explode('country').explode('industry')

    bridge_country_industry_df = pd.DataFrame()
    bridge_country_industry_df['deal_id']           = country_industry_df.deal_id
    bridge_country_industry_df['country-industry']  = country_industry_df.country + ' - ' + country_industry_df.industry

    bridge_country_industry_df.to_csv(out_path / 'bridge_country_industry.csv', index=False)

    logger.info("Data saved at %s", out_path)
    return(out_path)