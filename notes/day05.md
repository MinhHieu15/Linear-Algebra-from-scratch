# Day 05 — Vectors: add and scale

**Watched:** 3Blue1Brown Ch 1 *Vectors* · LA M1 › 02 assignments *Exploring parameter space* and *Solving simultaneous equations*

## Key ideas (in my own words)

Answer each in 1–2 lines:

- What a vector is, in the 3Blue1Brown picture (an arrow) and in code (a list of numbers):
  As a picture, a vector is an arrow that starts at the origin and has a length and a direction.
  In code, it's a list of numbers: how far the arrow goes along each axis, e.g. `[2, -1]`.
- How to add two vectors, as arrows (tip to tail) and as numbers:
  Arrows: put the tail of v on the tip of u; u + v goes from the start of u to the tip of v.
  Numbers: add entry by entry, `[1, 2] + [3, -1] = [4, 1]`.
- What multiplying a vector by a number does (k > 1, 0 < k < 1, k < 0):
  k > 1 stretches the arrow, 0 < k < 1 shrinks it, k < 0 flips it to point the opposite way.
  In numbers, every entry is multiplied by k.
- Why `add` must reject two vectors of different lengths:
  Entries are added in pairs, so a 2D and a 3D vector have nothing to pair up with.
  They live in different spaces; raising ValueError shows the bug instead of hiding it.
- How a step in parameter space (`p - lr * grad`) uses scale and add:
  First scale: `scale(-lr, grad)` makes a small arrow pointing downhill.
  Then add: `add(p, step)` moves the point p along that arrow.

## Worked examples by hand

Do these on paper first, then check in NumPy:

1. With `u = [2, -1, 4]` and `v = [-3, 5, 1]`, compute `u + v`, `3 * u` and `u - v`.

   ```text
   u + v = [2-3, -1+5, 4+1] = [-1, 4, 5]
   3 * u = [6, -3, 12]
   u - v = [2+3, -1-5, 4-1] = [5, -6, 3]
   ```

2. Draw `u = [1, 2]`, `v = [3, -1]` and `u + v` on squared paper, tip to tail. Where does the arrow `u + v` end?

   ```text
   u ends at (1, 2). From there, v goes 3 right and 1 down: (1+3, 2-1) = (4, 1).
   u + v = [4, 1], so the arrow ends at (4, 1).
   ```

3. You are at `p = [2.0, 0.5]`, the gradient is `[40, -10]` and `lr = 0.01`. Write `scale(-lr, grad)` first, then `add(p, ...)`. What is the new `p`?

   ```text
   step  = scale(-0.01, [40, -10]) = [-0.4, 0.1]
   p_new = add([2.0, 0.5], [-0.4, 0.1]) = [1.6, 0.6]
   ```

## Still unclear

-
