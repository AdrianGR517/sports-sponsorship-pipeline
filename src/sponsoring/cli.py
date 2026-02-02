from typing import Optional
from src.sponsoring.logging_config import setup_logging
from src.sponsoring.pipeline_build.build import run_build
from src.sponsoring.pipeline_analyze.analyze import run_analyze
import typer
from datetime import datetime
from pathlib import Path

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

from . import __version__ as cli_version

# App init
app = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.echo(f"Example Package Version: {cli_version}")
        raise typer.Exit()


@app.callback()
def main_cb(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, help="Display tool version"
    )
):
    pass

@app.command()
def build(
    route: str = typer.Argument(..., help="Route of the parquet or csv data"),
    blob: bool = typer.Option(False, "--blob", help="Indicates that route is a azure storage blob url"),
    out_dir: Path = typer.Option(Path("out"), help="Output path"),
    log_level: str = typer.Option("INFO", "--log-level", help="Logging level"),
    ):
    
    source = "blob" if blob else "folder"
    
    log_file = setup_logging(level=log_level)
    typer.echo(f"Logging -> {log_file}")  

    out_file = run_build(
        route=route,
        source=source,
        out_dir=out_dir
    )
    return(out_file)

@app.command()
def analyze(
    path: str = typer.Argument(..., help="Route of the parquet or csv data"),
    competition: str | None = typer.Option(None, "--competition", help="Team competition to filter by, disabled by default"),
    branding: str | None = typer.Option(None, "--branding", help="Team branding to filter by, disabled by default"),
    sport: str | None = typer.Option(None, "--sport", help="Team sport to filter by, disabled by default"),
    out_dir : Path = typer.Option(Path("out"), help="Output path"),
    log_level: str = typer.Option("INFO", "--log-level", help="Logging level")
    ):

    log_file = setup_logging(level=log_level)
    typer.echo(f"Logging -> {log_file}")  
    
    run_analyze(
        path=path,
        competition=competition,
        branding=branding,
        sport=sport,
        out_dir=out_dir
    )

    return()

def main():
    # app init
    app(prog_name="example-package")
