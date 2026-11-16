# Linear Algebra from scratch

Implementing linear algebra from scratch in Python and NumPy: vectors, matrices, solving linear systems, inverses, determinants, change of basis, Gram–Schmidt, eigenvalues, QR and SVD.

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
| 02 | Indexing, masks, broadcasting, `as_vector` | [notebook](notebooks/day02_indexing.ipynb) · [vectors.py](linalg/vectors.py) | [notes](notes/day02.md) |
| 03 | NumPy exercises, `is_zero_vector`, `vectors_close` | [notebook](notebooks/day03_exercises.ipynb) · [vectors.py](linalg/vectors.py) | [notes](notes/day03.md) |
