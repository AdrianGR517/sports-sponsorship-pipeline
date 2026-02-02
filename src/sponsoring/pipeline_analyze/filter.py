import pandas as pd
import logging

logger = logging.getLogger(__name__)


def analyze_filter(
    df: pd,
    *,
    competition: str | None = None,
    branding: str | None = None,
    sport: str | None = None    
    ):
    
    df_filtered = df.copy()

    if competition is not None:
        if 'team_competition' not in df.columns:
            raise ValueError("Missing required columns for filter: 'team_competition'")
        
        df_filtered = df_filtered[df_filtered['team_competition'] == competition]

    if branding is not None:
        if 'branding_fact' not in df.columns:
            raise ValueError("Missing required columns for filter: 'branding_fact'")
        
        df_filtered = df_filtered[df_filtered['branding_fact'] == branding]


    if sport is not None:
        if 'sport_fact' not in df.columns:
            raise ValueError("Missing required columns for filter: 'sport_fact'")

        df_filtered = df_filtered[df_filtered['sport_fact'] == sport]


    return(df_filtered)