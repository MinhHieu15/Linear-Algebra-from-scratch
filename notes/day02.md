# Day 02 — Indexing, masks, operations, broadcasting

**Watched:** BC 05 › 004 Quick Note on Array Indexing, 005 Numpy Array Indexing, 006 Numpy Operations

## Key ideas (in my own words)

Answer each in 1–2 lines:
array can use simple operators like plus, negative, multiply,

- Slicing `start:stop:step`:
- View vs copy: if you change the index in view, it affects the original array too! copy not
- `M[:, 1]` vs `M[:, 1:2]`: M[:,1] => All rows, [1] column , M[:,1:2] => All rows, all from 1 => 2 columns but not including 2! 
- Boolean mask: true/false condition in array
- Broadcasting rule (shapes line up from the right):

## Worked examples by hand

Do these on paper first, then check in NumPy:

1. `u = [1, 2, 3]`, `w = [4, 5, 6]`: compute `u * w`, then `sum(u * w)`. What is this number called?
u*w = [4, 10, 18]
sum(u*w) = 4 + 10 +18 = 32
dot product : Tich vo huong
np.dot(u,w)
2. `M = [[1, 2], [3, 4]]`: subtract the column means. Write the result.
means = [2, 3] (shape(2,))
M - means = [[-1, -1],[1, 1]]

3. Which pairs of shapes broadcast? `(4, 3)` with `(3,)` · `(4, 3)` with `(4,)` · `(4, 3)` with `(4, 1)`
(4,3) with (3,)
(4,3) with (4,1)
## as_vector

- What my function does: change an arange of numbers into a 1D array or vetor
- Edge cases I tested: check if input is 1D array, 2D array or scalar

## Still unclear

-
