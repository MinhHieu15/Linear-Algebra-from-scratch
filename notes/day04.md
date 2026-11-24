# Day 04 — Why linear algebra? Two problems from the course

**Watched:** LA M1 › 01 › 01 Introduction · M1 › 02 › 01 Motivations for linear algebra · M1 › 02 › 02 Getting a handle on vectors

## Key ideas (in my own words)

Answer each in 1–2 lines:

- Why the apples-and-bananas problem is a linear algebra problem:
  Because we have multiple linear equations with unknown prices.
  We can represent them using matrices and vectors.
- What `A p = c` means (rows of A, the vector p, the vector c):
  Because we have multiple linear equations with unknown prices.
  We can represent them using matrices and vectors.
- What "parameter space" means:
  Parameter space is the space containing all possible combinations of model parameters.
  In this problem, each point [mu, sigma] represents one Gaussian distribution.
- What SSE measures:
  SSE (Sum of Squared Errors) measures the total squared difference between
  the observed data and the predicted values.
- What the gradient is, and why we step against it:
  The gradient is a vector pointing in the direction of the steepest increase in SSE.
  We move in the opposite direction to reduce SSE.
- Learning rate too big / too small:
  A learning rate that is too big can overshoot the minimum and cause instability.
  A learning rate that is too small makes convergence very slow.

## Worked examples by hand

Do these on paper first, then check in NumPy:

1. With `A = [[2, 3], [10, 1]]` and `p = [1, 2]`, compute `A p` row by row. Which trip is wrong, and by how much?

   ```text
   A @ p = [8, 12]
   residual = [0, -1]
   ```

2. Solve `2a + 3b = 8`, `10a + b = 13` by hand (substitution). Check your answer against Part A4.

   ```python
   A = np.array([[2, 3], [10, 1]])
   c = np.array([8, 13])

   p = np.linalg.solve(A, c)

   print(p)
   print(A @ p)
   ```

3. You are at `p = [1.65, 0.12]` and the gradient is `[-600, 400]`. With `lr = 0.0001`, write the new `p`.

   ```python
   p = np.array([1.65, 0.12])
   grad = np.array([-600, 400])
   lr = 0.0001

   p_new = p - lr * grad

   print(p_new)
   ```

## The plot I'm proudest of today

My favorite plot is the Gradient Descent path on the parameter space contour plot.

It shows how the parameters mu and sigma move step by step toward the minimum SSE. I learned how the gradient and learning rate work together to optimize a model.

## Still unclear

-
