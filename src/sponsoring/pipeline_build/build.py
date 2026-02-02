from src.sponsoring.pipeline_build.load import build_load
from src.sponsoring.pipeline_build.merge import build_merge
from src.sponsoring.pipeline_build.transform import build_transform
from pathlib import Path
from datetime import datetime   
import logging

ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

logger = logging.getLogger(__name__)


def run_build(route, source = 'folder', out_dir = Path("out")):
    out_dir.mkdir(parents=True, exist_ok=True)

    # Pipeline
    dfs_loaded      = build_load(route=route, source=source)
    df_merged       = build_merge(dfs_loaded)
    df_transformed  = build_transform(df_merged)

    out_file = out_dir / f"build_output_{ts}.csv" 
    logger.info("Saving to %s", out_file)
    df_transformed.to_csv(out_file, index=False)
    logger.info("Data saved at %s", out_file)
    return(out_file)