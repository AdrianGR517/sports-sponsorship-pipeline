# Sports Sponsorship Data Pipeline

A small, reproducible data pipeline and reporting toolkit for sports sponsorship deals, built as a one-week **technical assessment** (sports analytics context). It ingests raw sponsor and competition data, cleans and normalizes it — including ML-based normalization of free-text industry labels — and produces analysis-ready tables to answer business questions such as *which country–industry pairs are most interesting* and *how sponsorship differs across competitions*.

The emphasis is on **data-modeling thinking, entity resolution, clean code and reproducibility** rather than on any single metric.

## Highlights

- **CLI-first design** — a [Typer](https://typer.tiangolo.com/) command-line app with two commands, `build` and `analyze`, covering the full flow from raw files to reporting tables.
- **ML-based industry normalization** — raw industry labels are messy (inconsistent acronyms, multiple categories glued together). The cleaning pipeline: expands acronyms (`IT`, `PR`, `HVAC`, …) → splits concatenated categories → embeds each label with a sentence-transformer (`all-MiniLM-L6-v2`) → groups semantically similar labels via agglomerative clustering (cosine distance) → names each cluster after its most central member. Hundreds of noisy labels collapse into a small set of consistent industries without hand-written mapping tables.
- **Dimensional-style data model** — the build step outputs a main deals table plus **bridge tables** for multi-valued attributes (country, industry, and a country–industry bridge), keeping the core table tidy and the many-to-many relationships explicit.
- **Reproducible by design** — environment fully pinned with [pixi](https://pixi.sh/); a `Dockerfile` and CI workflows are included.
- **Engineering hygiene** — input validation of required columns with clear errors, configurable logging to timestamped log files, timestamped output folders under `/out`.

## Usage

With [pixi](https://pixi.sh/) installed:

```bash
pixi install          # creates the pinned environment

# 1) Build: load raw data (folder of CSV/parquet, or Azure Blob), clean,
#    normalize industries, generate core + bridge tables
pixi run build <path-to-raw-data>

# 2) Analyze: generate reporting tables from the build output
pixi run analyze <path-to-build-output>
```

Or through the CLI directly:

```bash
python -m sponsoring build <route> [--blob] [--id-col-name deal_id] [--out-dir out] [--log-level INFO]
python -m sponsoring analyze <path> [--id-col deal_id] [--out-dir out] [--log-level INFO]
```

`--blob` lets `build` read directly from an Azure Blob Storage URL instead of a local folder.

## What `analyze` produces

Written to a timestamped folder under `/out`:

| Output | Question it answers |
|---|---|
| `summary.csv` | Overall snapshot of the cleaned deals dataset |
| `average_annual_usd_by_industry.csv` | Which industries pay more per year? |
| `average_annual_usd_by_country.csv` | Which countries pay more per year? |
| `average_annual_usd_by_industry_and_league.csv` | How does industry spend differ across competitions? |
| `total_deals_by_industry_and_country.csv` | Where is sponsorship volume concentrated? |
| `usd_by_industry_and_country.csv` | Country–industry pairs by deal count, average annual and total USD |

## Project structure

```
src/sponsoring/
├── cli.py                     # Typer CLI (build / analyze commands)
├── logging_config.py          # Timestamped file logging, configurable level
├── pipeline_build/
│   ├── build.py               # Orchestration: load → merge → transform → save
│   ├── load.py                # Local folder or Azure Blob ingestion (CSV/parquet)
│   ├── merge.py               # Joins the raw sources on the deal id
│   ├── transform.py           # Cleaning and typing
│   └── transformations.py     # Industry normalization (embeddings + clustering)
└── pipeline_analyze/
    ├── analyze.py             # Orchestration + input validation
    └── *.py                   # One module per reporting table
```

## Design decisions & trade-offs

- **Embeddings + clustering over a manual mapping table:** scales to unseen labels and avoids maintaining a dictionary, at the cost of some tuning (the number of clusters is currently fixed at 30 — a pragmatic choice for this dataset that would be worth making data-driven, e.g. via a distance threshold, in a production setting).
- **Bridge tables over exploded flat tables:** deals with multi-valued countries/industries without duplicating deal-level facts, at the cost of requiring joins at analysis time.
- **CSV outputs** were chosen for easy inspection by non-technical reviewers; parquet would be the production choice.

## Requirements

- [pixi](https://pixi.sh/) (manages Python and all dependencies from `pyproject.toml` / `pixi.lock`)
- Main libraries: pandas, pyarrow, scikit-learn, sentence-transformers, Typer, Azure Storage Blob

---

*Author: Adrián García Ruiz — [github.com/AdrianGR517](https://github.com/AdrianGR517)*
