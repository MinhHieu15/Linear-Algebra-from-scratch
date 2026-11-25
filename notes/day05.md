# Day 05 — Vectors: add and scale

**Watched:** 3Blue1Brown Ch 1 *Vectors* · LA M1 › 02 assignments *Exploring parameter space* and *Solving simultaneous equations*

## Key ideas (in my own words)

Answer each in 1–2 lines:

- What a vector is, in the 3Blue1Brown picture (an arrow) and in code (a list of numbers):
- How to add two vectors, as arrows (tip to tail) and as numbers:
- What multiplying a vector by a number does (k > 1, 0 < k < 1, k < 0):
- Why `add` must reject two vectors of different lengths:
- How a step in parameter space (`p - lr * grad`) uses scale and add:

## Worked examples by hand

Do these on paper first, then check in NumPy:

1. With `u = [2, -1, 4]` and `v = [-3, 5, 1]`, compute `u + v`, `3 * u` and `u - v`.

2. Draw `u = [1, 2]`, `v = [3, -1]` and `u + v` on squared paper, tip to tail. Where does the arrow `u + v` end?

3. You are at `p = [2.0, 0.5]`, the gradient is `[40, -10]` and `lr = 0.01`. Write `scale(-lr, grad)` first, then `add(p, ...)`. What is the new `p`?

## Still unclear

-
