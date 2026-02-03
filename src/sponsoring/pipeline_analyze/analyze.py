from src.sponsoring.pipeline_analyze.load import analyze_load
from src.sponsoring.pipeline_analyze.summary import analyze_summary
from src.sponsoring.pipeline_analyze.avg_by_country import analyze_avg_usd_by_country
from src.sponsoring.pipeline_analyze.avg_by_industry import analyze_avg_usd_by_industry
from src.sponsoring.pipeline_analyze.avg_by_industry_and_league import analyze_avg_usd_by_industry_and_league
from src.sponsoring.pipeline_analyze.deals_by_industry_and_country import analyze_deals_by_industry_and_country
from src.sponsoring.pipeline_analyze.usd_by_industry_and_country import analyze_usd_by_industry_and_country
from pathlib import Path
from datetime import datetime
import pandas as pd
import logging

ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

logger = logging.getLogger(__name__)


def run_analyze(
    path: str,
    *,
    id_col : str = "deal_id",
    out_dir = Path("out")
):
    
    out_path = out_dir / f"analyze_{ts}" 
    out_path.mkdir(parents=True, exist_ok=True)

    analysis_df  = analyze_load(path_str=path, id_col=id_col)

    REQUIRED_COLUMNS = {'deal_id','brand_name','team_name','country','industry','competition'}

    missing = REQUIRED_COLUMNS - set(analysis_df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )
    
    # Creating the summary dataframe
    summary_df = analyze_summary(analysis_df)
    summary_df.to_csv(str(out_path) + '/summary.csv')

    # Creating the avg usd by industry dataframe
    avg_ind_df = analyze_avg_usd_by_industry(analysis_df)
    avg_ind_df.to_csv(str(out_path) + '/average_annual_usd_by_industry.csv')

    # Creating the avg usd by country dataframe
    avg_count_df = analyze_avg_usd_by_country(analysis_df)
    avg_count_df.to_csv(str(out_path) + '/average_annual_usd_by_country.csv')

    # Creating the avg usd by industry and league dataframe
    avg_ind_league_df = analyze_avg_usd_by_industry_and_league(analysis_df)
    avg_ind_league_df.to_csv(str(out_path) + '/average_annual_usd_by_industry_and_league.csv')

    # Creating the total deals by industry and country dataframe
    deals_ind_count_df = analyze_deals_by_industry_and_country(analysis_df)
    deals_ind_count_df.to_csv(str(out_path) + '/total_deals_by_industry_and_country.csv') 

    # Creating the usd by industry and country dataframe
    usd_ind_count_df = analyze_usd_by_industry_and_country(analysis_df)
    usd_ind_count_df.to_csv(str(out_path) + '/usd_by_industry_and_country.csv') 

    return()