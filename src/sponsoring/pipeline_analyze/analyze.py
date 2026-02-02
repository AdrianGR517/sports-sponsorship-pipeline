from src.sponsoring.pipeline_analyze.load import analyze_load
from src.sponsoring.pipeline_analyze.filter import analyze_filter
from src.sponsoring.pipeline_analyze.group import analyze_group
from pathlib import Path
from datetime import datetime
import logging

ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

logger = logging.getLogger(__name__)


def run_analyze(
    path: str,
    *,
    competition: str | None = None,
    branding: str | None = None,
    sport: str | None = None,
    out_dir = Path("out")
):
    
    out_dir.mkdir(parents=True, exist_ok=True)

    # Pipeline
    df_loaded   = analyze_load(path_str=path)
    df_filtered = analyze_filter(df=df_loaded, competition=competition, branding=branding, sport=sport)
    df_grouped  = analyze_group(df=df_filtered)


    out_file = out_dir / f"analyze_output_{ts}.csv" 
    logger.info("Saving to %s", out_file)

    df_grouped.to_csv(out_file, index=False)
    logger.info("Data saved at %s", out_file)

    return()