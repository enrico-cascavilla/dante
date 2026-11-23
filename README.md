# Dante

## Requirements

- [git](https://git-scm.com/)
- [uv](https://docs.astral.sh/uv/): manages Python 3.12, the virtual environment and dependencies
- [direnv](https://direnv.net/), hooked into the shell (`eval "$(direnv hook zsh)"` in `~/.zshrc`)

DVC is a dev dependency of the project: `uv sync` installs it.

## Setup

```bash
git clone https://github.com/enrico-cascavilla/dante.git
cd dante
direnv allow          # loads UV_PROJECT_ENVIRONMENT=dante-env from .envrc
uv sync               # creates dante-env with the locked dependencies
uv run dvc pull       # downloads the data from the DVC remote
```

Run `direnv allow` before `uv sync`, otherwise uv creates the environment as `.venv`.

## Project structure

```
data/raw/            original data, never edited, versioned with DVC
data/processed/      data produced by code
artifacts/           trained models
notebooks/           exploration only
src/dante_gen/       production code (importable package)
  models/            one module per model
scripts/             command-line entry points
tests/               pytest test suite
```

## Data

In `data/raw/`, versioned with [DVC](https://dvc.org/): Git tracks the pointer `data/raw.dvc`, the files are stored on [DagsHub](https://dagshub.com/enrico-cascavilla/dante).

| File | Content |
|---|---|
| `divina_commedia.parquet` | *Divina Commedia*, 14,233 verses: cantica, canto, tercet, verse number, text |
| `vita_nuova_poetry.csv` | *Vita Nuova*, poems (682 verses), from [Digital Dante](https://digitaldante.columbia.edu/) |
| `vita_nuova_prose.csv` | *Vita Nuova*, prose (71 paragraphs), same source |
