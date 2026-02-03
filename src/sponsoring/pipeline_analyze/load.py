import pandas as pd
import typer
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def analyze_load(path_str : str, id_col : str = 'deal_id'):

    path = Path(path_str)

    if not path.exists():
        raise typer.BadParameter(f"Folder {path_str} not found")
    
    if not (path / 'main.csv').exists():
        raise typer.BadParameter(f"File {path_str}/main.csv not found")
    if not (path / 'bridge_branding.csv').exists():
        raise typer.BadParameter(f"File {path_str}/bridge_branding.csv not found")
    if not (path / 'bridge_country.csv').exists():
        raise typer.BadParameter(f"File {path_str}/bridge_country.csv not found")
    if not (path / 'bridge_industry.csv').exists():
        raise typer.BadParameter(f"File {path_str}/bridge_industry.csv not found")

    main_df = pd.read_csv(path_str + '/main.csv')
    bridge_branding_df = pd.read_csv(path_str + '/bridge_branding.csv')
    bridge_country_df  = pd.read_csv(path_str + '/bridge_country.csv')
    bridge_industry_df = pd.read_csv(path_str + '/bridge_industry.csv')

    analyze_df = (
        main_df
        .merge(bridge_branding_df, on=id_col, how="inner")
        .merge(bridge_country_df, on=id_col, how="inner")
        .merge(bridge_industry_df, on=id_col, how="inner")
        )

    return(analyze_df)