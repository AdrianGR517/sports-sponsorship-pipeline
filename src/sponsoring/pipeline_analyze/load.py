import pandas as pd
import typer
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def analyze_load(path_str : str):

    path = Path(path_str)

    if not path.exists():
        raise typer.BadParameter(f"File {path_str} not found")
    
    extension = path_str.split('.')[-1]

    if extension == 'parquet':
        df = pd.read_parquet(path_str)

    elif extension == 'csv':
        df = pd.read_csv(path_str)

    else:
        raise typer.BadParameter("File must be in .parquet or .csv format")
    
    return(df)