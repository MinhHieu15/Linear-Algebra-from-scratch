# Day 03 — NumPy exercises + comparing floats

**Watched:** BC 05 › 007 Numpy Exercises Overview (and 008 Solutions, after finishing)

## Key ideas (in my own words)

Answer each in 1–2 lines:

- `axis=0` vs `axis=1`:
- Diagonal and trace:
- Transpose:
- Why floats can't be compared with `==`:
- Tolerance (`tol`):

## Worked examples by hand

Do these on paper first, then check in NumPy:

1. `A = [[1, 2, 3], [4, 5, 6]]`: write `A.sum(axis=0)`, `A.sum(axis=1)` and `A.T`.
2. `B = [[2, 7], [1, 8]]`: what is the trace of `B`?
3. With `tol = 0.01`, which are "close"? `[1.0, 2.0]` vs `[1.005, 2.0]` · `[1.0, 2.0]` vs `[1.02, 2.0]` · `[0.0]` vs `[-0.009]`

## Exercises I got wrong or needed help with

-

## is_zero_vector and vectors_close

- What they do:
- Why `vectors_close` raises on different lengths:

## Still unclear

-
