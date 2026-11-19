# Day 03 — NumPy exercises + comparing floats

**Watched:** BC 05 › 007 Numpy Exercises Overview (and 008 Solutions, after finishing)

## Key ideas (in my own words)

Answer each in 1–2 lines:

- `axis=0` vs `axis=1`: axis = 0 operates with columns, while axis = 1 operates with rows
- Diagonal and trace: Trace is sum of Diagonal of a square matrix
- Transpose: Swapping rows and columns
- Why floats can't be compared with `==`: Because Inherent nature of their binary representation
- Tolerance (`tol`):  refers to the maximum allowed difference between two numerical values when checking if they are “close"

## Worked examples by hand

Do these on paper first, then check in NumPy:

1. `A = [[1, 2, 3], [4, 5, 6]]`: write `A.sum(axis=0)`, `A.sum(axis=1)` and `A.T`.

   ```text
   A.sum(axis = 0) = [5, 7, 9] (1,3)
   A.sum(axis = 1) = [6, 15]   (2,)
   A.T = [[1, 4], [2, 5], [3, 6]] (3,2)
   ```

2. `B = [[2, 7], [1, 8]]`: what is the trace of `B`?

   ```text
   np.diag(B) = [2, 8]
   np.trace(B) = 10
   ```

3. With `tol = 0.01`, which are "close"? `[1.0, 2.0]` vs `[1.005, 2.0]` · `[1.0, 2.0]` vs `[1.02, 2.0]` · `[0.0]` vs `[-0.009]`

   ```text
   np.all(np.abs([1.0, 2.0] - [1.005, 2.0])) = 0.005 < 0.01 => Close
   np.all(np.abs([1.0, 2.0] - [1.02, 2.0]))  = 0.02 > 0.01  => Not Close
   np.all(np.abs([0.0] - [-0.009]))          = 0.009 < 0.01 => Close
   ```

## Exercises I got wrong or needed help with

-

## is_zero_vector and vectors_close

- What they do:
  - `is_zero_vector(v, tol)`: True if every entry has |entry| < tol.
    Tiny rounding errors like 1e-12 still count as zero.
  - `vectors_close(u, v, tol)`: True if every pair of entries differs by less
    than tol, i.e. |u_i - v_i| < tol for all i. Same as asking whether u - v
    is a zero vector.
- Why `vectors_close` raises on different lengths:
  Vectors of different lengths live in different spaces, so "are they close?"
  has no yes/no answer. Getting different lengths means the caller has a bug.
  Returning False would hide it; raising ValueError shows it immediately.

## Still unclear

-
