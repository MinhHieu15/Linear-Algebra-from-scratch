# Machine learning from scratch

Implementing linear algebra from scratch in Python and NumPy, then using that same library for ML algorithms: linear regression, PCA, a recommender system and a neural net.

60-day plan: [ROADMAP.md](ROADMAP.md). One new function per day, each with tests checked against `np.linalg`.

## Layout

```
linalg/      the library (no np.linalg inside)
tests/       pytest, results checked against NumPy
notebooks/   experiments and plots: dayXX_<topic>.ipynb
notes/       theory notes: dayXX.md (template: notes/_template.md)
```

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
```

## Progress

| Day | Topic | Code | Notes |
|---|---|---|---|
| 01 | NumPy basics, repo setup | [notebook](notebooks/day01_numpy.ipynb) | [notes](notes/day01.md) |
