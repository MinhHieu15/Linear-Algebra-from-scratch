# Linear Algebra for ML — 60 days, one commit every day

Sources used in this roadmap:

- **[LA]** `D:\Linear Algebra in ML` — *Mathematics for Machine Learning: Linear Algebra* (Imperial College, 5 modules). This is the theory backbone.
- **[BC]** `D:\ML bootcamp` — *Python for Data Science & ML Bootcamp*. Section 05 (NumPy) is the warm-up; sections 15, 22, 23 and 25 are where you apply linear algebra to real ML.
- **Formula sheet:** `06_Resources\...\01__maths4ml-linearalgebra-formula.pdf`. Print it and keep it next to your desk.

Video path notation: `M2 › 02 › 01` means module `02_vectors-...`, subfolder `02_finding-...`, video `01_modulus-inner-product.mp4`.

---

## 1. The idea: one repo that grows every day

Create a GitHub repo called `Linear-Algebra-from-scratch`. Every day you write **one function yourself** (plain Python or basic NumPy operations, *never* `np.linalg`), then write **a test that compares it against `np.linalg`**. Every commit means something, and by the end you have a small linear algebra library you wrote yourself.

```
Linear-Algebra-from-scratch/
├── README.md              # log: day, topic, links to files
├── requirements.txt       # numpy, matplotlib, pytest, ...
├── linalg/                # your library
│   ├── vectors.py
│   ├── matrices.py
│   ├── solve.py
│   ├── transforms.py
│   ├── eigen.py
│   └── decomp.py
├── tests/                 # test_<module>.py, checked against np.linalg
├── notebooks/             # dayXX_<topic>.ipynb: plots, experiments
└── notes/                 # dayXX.md: theory summary in your own words
```

**Daily routine (45–90 minutes):**

1. 📺 Watch the video in the *Study* column.
2. ✍️ Work 2–3 small examples by hand, write `notes/dayXX.md` (5–10 lines).
3. 💻 Do the task in the *Coding task* column and get `pytest` green.
4. ✅ `git add . && git commit -m "<suggested message>" && git push`.

**To make the GitHub squares actually turn green:**

- The email in `git config user.email` must match an email added to your GitHub account.
- Commits must be on the default branch (`main`) or `gh-pages`, and the repo must not be a fork.
- Private repos only show squares if you enable *Settings → Profile → Private contributions*.
- Bonus: add GitHub Actions to run `pytest` on every push (Day 3) so every commit gets a ✓.

> Green squares are a side reward. Real commits with real content are what make your profile worth something when a recruiter clicks through.

---

## 2. Overview

| Phase | Days | Content | Source |
|---|---|---|---|
| 0. Warm-up | 1–3 | NumPy, repo setup, CI | BC 05 |
| 1. Vectors | 4–14 | Operations, dot product, projection, change of basis, linear independence | LA M1, M2 |
| 2. Matrices | 15–24 | Transformations, matrix multiplication, Gaussian elimination, inverse, determinant | LA M3 |
| 3. Linear mappings | 25–34 | Einstein summation, change of basis for matrices, orthogonality, Gram–Schmidt, reflections | LA M4 |
| 4. Eigenvalues | 35–44 | Eigen, diagonalization, power iteration, PageRank | LA M5 |
| 5. Filling the gaps | 45–52 | Rank, null space, norms, least squares, QR, SVD | Outside the course (see section 4) |
| 6. Applying to ML | 53–60 | Linear regression, PCA, recommender, neural net, capstone | BC 15, 22, 23, 25 |

Why phase 5 exists: the Imperial course **does not cover SVD or least squares**, yet these are the two most important linear algebra tools in ML (the bootcamp's PCA and recommender sections both rely on them).

---

## 3. Detailed schedule

### Phase 0 — Warm-up (BC section 05)

| Day | Study | Coding task | Commit |
|---|---|---|---|
| 1 | BC 05 › 002, 003 (NumPy arrays) | Create the repo, `README.md`, `requirements.txt`, `.gitignore`. Notebook `day01_numpy.ipynb`: create vectors and matrices, `shape`, `reshape`, `arange`, `linspace`, `eye`. | `init: project skeleton + numpy basics` |
| 2 | BC 05 › 005, 006 (indexing, operations) | Notebook: slicing, boolean masks, broadcasting. Write `as_vector(x)` in `linalg/vectors.py`: takes a list or array, returns a 1D float array, raises an error if it is not 1D. First test in `tests/test_vectors.py`. | `feat: as_vector + first pytest` |
| 3 | BC 05 › 007, 008 (exercises) | Redo the NumPy Exercises without looking at the solutions. Write `is_zero_vector` and `vectors_close` (float comparison with a tolerance) in `linalg/vectors.py`. Add the CI badge to the README. | `feat: zero check + vector comparison with tolerance` |

### Phase 1 — Vectors (LA Modules 1–2)

| Day | Study | Coding task | Commit |
|---|---|---|---|
| 4 | M1 › 01 › 01; M1 › 02 › 01, 02 | `notes/day04.md`: why ML needs linear algebra (fitting parameters = finding a point in parameter space). Notebook: plot the SSE of the model `y = m·x + c` over an (m, c) grid with `contourf`. | `notebook: parameter space contour` |
| 5 | M1 › 02, assignments *exploring-parameter-space* and *solving-simultaneous-equations* | Do both exercises in the `.html` files. Write `add(u, v)` and `scale(k, v)` with loops, test against `u + v` and `k * v`. | `feat: vector add and scale` |
| 6 | M1 › 03 › 01 + assignment *doing-some-vector-operations*; M1 › 04 › 01 | `sub`, `linear_combination(coeffs, vectors)`. Notebook: draw vector addition with `plt.quiver` (parallelogram rule). | `feat: linear combination + quiver plot` |
| 7 | M2 › 01 › 01; M2 › 02 › 01 (modulus, inner product) | `dot(u, v)`, `norm(v)` (L2). Test against `np.dot` and `np.linalg.norm`. Also test properties: `dot(u,v) == dot(v,u)`, `dot(v,v) == norm(v)**2`. | `feat: dot product and L2 norm` |
| 8 | M2 › 02 › 02 (cosine) | `angle(u, v)` in radians, with `np.clip` to avoid rounding errors outside [-1, 1]. `cosine_similarity(u, v)`. Notebook: compare the similarity of a few toy "word vectors". | `feat: angle and cosine similarity` |
| 9 | M2 › 02 › 03 (projection) + assignment *dot-product-of-vectors* | `scalar_projection(s, r)` and `vector_projection(s, r)` (project s onto r). Notebook: draw the projection. | `feat: scalar and vector projection` |
| 10 | M2 › 03 › 01 (changing basis) + assignment *changing-basis* | `change_basis_orthogonal(v, basis)`: coordinates of v in an orthogonal basis using projections. Test: rebuilding v from the new coordinates gives the original v. | `feat: change of basis via projection` |
| 11 | M2 › 03 › 03 (basis, linear independence) | `is_linearly_independent(vectors)`. Today use a "naive" approach for 2D/3D (determinant or ratio check). Day 46 rewrites it using rank. | `feat: linear independence check (2D/3D)` |
| 12 | M2 › 03 › 04, 05 (applications + assignment *linear-dependency*) | Notebook: project a cloud of 2D points onto the best line you can guess, measure the total distance. (This is a crude PCA; you will come back to it on Day 54.) | `notebook: projecting noisy data onto a line` |
| 13 | M2 › 04 › 01 (vector-operations-assessment) | Take the assessment. Solve each question in code in `notebooks/day13_assessment.ipynb` and check against your hand answers. | `practice: module 2 assessment in code` |
| 14 | M2 › 04 › 02 (summary) — **review** | Write full docstrings for every function in `linalg/vectors.py`. Bring every function to at least 3 test cases, including edge cases (zero vector, parallel vectors). | `docs+test: polish vectors module` |

### Phase 2 — Matrices (LA Module 3)

| Day | Study | Coding task | Commit |
|---|---|---|---|
| 15 | M3 › 01 › 01 (matrices & simultaneous equations) | `linalg/matrices.py`: `matvec(A, v)` with two loops. Test against `A @ v`. | `feat: matrix-vector product` |
| 16 | M3 › 02 › 01 (how matrices transform space) | Notebook: draw a square grid and its image under any 2×2 matrix. Write a reusable `plot_transform(A)`. | `viz: plot 2D linear transformation` |
| 17 | M3 › 02 › 02 (types of transformation) | `rotation(theta)`, `scaling(sx, sy)`, `shear(k)`, `reflection_x()`, `reflection_y()` in `linalg/transforms.py`. Plot each with `plot_transform`. | `feat: 2D transformation constructors` |
| 18 | M3 › 02 › 03 (composition) + assignment *using-matrices-to-make-transformations* | `matmul(A, B)` with three loops, test against `A @ B`. Also test: `matmul(A, B) != matmul(B, A)` in general; two 90° rotations = one 180° rotation. | `feat: matmul + composition tests` |
| 19 | — (practice day) | `transpose(A)`, `identity(n)`, `is_symmetric(A)`. Benchmark your `matmul` vs `@` for n = 50, 100, 200 and record the results in your notes. | `feat: transpose/identity + benchmark` |
| 20 | M3 › 03 › 01 (Gaussian elimination) | `linalg/solve.py`: `row_echelon(A)` (Gaussian elimination, with row swaps when a pivot is 0). | `feat: gaussian elimination to row echelon` |
| 21 | M3 › 03 › 01 (rewatch) | `back_substitution(U, b)` and `solve(A, b)` = elimination + back substitution. Test against `np.linalg.solve` on random matrices from 3×3 to 10×10. | `feat: solve linear system` |
| 22 | M3 › 03 › 02 (from elimination to inverse) | `inverse(A)` via Gauss–Jordan on `[A | I]`. Test `A @ inverse(A) ≈ I`. Raise `ValueError` for singular matrices. | `feat: inverse via gauss-jordan` |
| 23 | M3 › 03 › 03 (assignment *solving-linear-equations-using-the-inverse*); M3 › 04 › 01 (determinants) | `det(A)`: (a) recursive cofactor expansion, (b) product of the diagonal after Gaussian elimination (flip the sign on each row swap). Compare the speed of both for n = 8. | `feat: determinant two ways` |
| 24 | M3 › 04 › 02 (summary) — **review** | The "apples and bananas" problem from the video: set up the system and solve it with your `solve`. Add tests: `det(AB) = det(A)·det(B)`, `det(A) = 0` ⇔ `inverse` raises. | `test: matrix properties` |

### Phase 3 — Linear mappings (LA Module 4)

| Day | Study | Coding task | Commit |
|---|---|---|---|
| 25 | M4 › 01 › 01 (Einstein summation) | Rewrite `dot`, `matvec`, `matmul`, `transpose`, `trace` with `np.einsum` in `notebooks/day25_einsum.ipynb`. Test they match your own versions. | `notebook: einsum versions of core ops` |
| 26 | — (einsum practice) | Use `einsum` for: batched matmul (shapes `(b,n,m)·(b,m,k)`), outer product, sum of the diagonal. You will use this skill directly in PyTorch. | `practice: batched einsum` |
| 27 | M4 › 02 › 01 (matrices changing basis) | `to_basis(v, B)` and `from_basis(v_b, B)` for a **non**-orthogonal basis (using `inverse` or `solve`). Test the round trip. | `feat: change of basis (general)` |
| 28 | M4 › 02 › 02 (transformation in a changed basis) | `transform_in_basis(A, B)` = `B⁻¹ A B`. Example: a 45° rotation written in a skewed basis. Plot it to verify. | `feat: similarity transform B^-1 A B` |
| 29 | M4 › 03 › 01 (orthogonal matrices) | `is_orthogonal(A)`. Tests: rotation matrices are orthogonal; `Aᵀ = A⁻¹`; `det = ±1`; multiplying a vector does not change its `norm`. | `feat: orthogonal matrix check` |
| 30 | M4 › 04 › 01 (Gram–Schmidt) | `linalg/decomp.py`: `gram_schmidt(vectors)` returns an orthonormal basis. Skip linearly dependent vectors (norm < 1e-10). | `feat: gram-schmidt` |
| 31 | M4 › 04 › 01 (rewatch) | Write **modified** Gram–Schmidt. Experiment: with nearly parallel vectors, compare `‖QᵀQ − I‖` for the classical and modified versions. Write down what you see. | `experiment: classical vs modified GS` |
| 32 | M4 › 04 › 02 (reflecting in a plane) | `reflect_in_plane(v, basis_of_plane)`: build an orthonormal basis E with Gram–Schmidt, reflect in that basis, then transform back: `E T E⁻¹`. | `feat: reflection in a plane` |
| 33 | — (practice day) | Small application: compress a grayscale image by projecting onto k orthonormal basis vectors (e.g. the first k rows of the image matrix after Gram–Schmidt). Plot original vs reconstruction. | `notebook: projection-based image compression` |
| 34 | **Review Modules 3–4** | Every function in `matrices.py`, `solve.py`, `transforms.py`, `decomp.py` has a docstring + ≥3 tests. Update the progress table in the README. | `docs+test: polish matrices & mappings` |

### Phase 4 — Eigenvalues & PageRank (LA Module 5)

| Day | Study | Coding task | Commit |
|---|---|---|---|
| 35 | M5 › 01 › 01, 02 (what are eigen-things) | Notebook: using `plot_transform`, color the vectors that **keep their direction** after the transformation. Find the eigenvectors of scaling, shear and rotation by eye. | `viz: eigenvectors visually` |
| 36 | M5 › 02 › 01 (special eigen cases) | `eig_2x2(A)`: solve the characteristic equation `λ² − tr(A)λ + det(A) = 0`, handle complex roots (rotations). Test against `np.linalg.eig`. | `feat: closed-form 2x2 eigen` |
| 37 | M5 › 02 › 02 (calculating eigenvectors) | For each λ, find the eigenvector by solving `(A − λI)x = 0`. Test `A v ≈ λ v`. | `feat: eigenvectors from null space` |
| 38 | — (algorithm) | `linalg/eigen.py`: `power_iteration(A, iters, tol)` returns the largest eigenvalue + its vector. Plot convergence against iteration count. | `feat: power iteration` |
| 39 | — (algorithm) | `inverse_iteration(A, mu)` finds the eigenvalue closest to `mu`. Add deflation to get the 2–3 largest eigenvalues of a symmetric matrix. | `feat: inverse iteration + deflation` |
| 40 | M5 › 03 › 01 (changing to the eigenbasis) | `diagonalize(A)` returns `C, D` with `A = C D C⁻¹`. `matrix_power(A, n)` via diagonalization; compare with multiplying n times. | `feat: diagonalization + fast power` |
| 41 | M5 › 03 › 02 (eigenbasis example) | Application: the n-th Fibonacci number by diagonalizing `[[1,1],[1,0]]`. Compare with a loop for n ≤ 70. | `notebook: fibonacci via eigen` |
| 42 | M5 › 04 › 01 (PageRank) | `pagerank(link_matrix, d=0.85)` with power iteration on the 6-page network from the video. Test that the ranks sum to 1. | `feat: pagerank` |
| 43 | — (mini project) | Apply PageRank to a real graph: write or download a small edge list (e.g. Wikipedia pages you pick and the links between them). Print the top 10. | `project: pagerank on a real graph` |
| 44 | M5 › 05 › 01, 02 (summary, wrap-up) — **review** | Redo the course exercises in the `.html` files that you got wrong the first time. Write `notes/module-recap.md` summarizing all 5 modules on one page. | `docs: course recap` |

### Phase 5 — Filling the gaps (outside the Imperial course)

Suggested material: *3Blue1Brown — Essence of Linear Algebra* (YouTube, matching chapters), *Gilbert Strang — MIT 18.06* (lectures 9–10, 14–17, 29), the book *Mathematics for Machine Learning* (Deisenroth et al., free PDF, chapters 2–4).

| Day | Topic | Coding task | Commit |
|---|---|---|---|
| 45 | Rank, reduced row echelon form | `rref(A)` and `rank(A)`. Test against `np.linalg.matrix_rank`. | `feat: rref and rank` |
| 46 | Column space, null space | `null_space(A)` from RREF. Rewrite `is_linearly_independent` using `rank` (any dimension). Test: `A @ null_space(A) ≈ 0`. | `refactor: independence via rank + null space` |
| 47 | Vector and matrix norms | `norm(v, p)` for p = 1, 2, ∞; `frobenius(A)`. Notebook: plot the "unit ball" for L1, L2, L∞ (link to Lasso/Ridge). | `feat: p-norms + unit ball plot` |
| 48 | Least squares, normal equations | `lstsq_normal(A, b)` solving `AᵀA x = Aᵀb`. Fit a line and a parabola to noisy data. Test against `np.linalg.lstsq`. | `feat: least squares via normal equations` |
| 49 | QR decomposition | `qr(A)` using your Gram–Schmidt from Day 30. `lstsq_qr(A, b)`. Compare accuracy with the normal equations when A is nearly singular (large condition number). | `feat: QR + stable least squares` |
| 50 | QR algorithm for eigenvalues | `eig_qr(A)`: iterate `A ← RQ`. Test on symmetric matrices against `np.linalg.eigh`. | `feat: QR algorithm for eigenvalues` |
| 51 | SVD (theory) | `svd_via_eig(A)`: get V and σ from the eigenvalues of `AᵀA`, then `U = AV/σ`. Test that `A ≈ U Σ Vᵀ`. | `feat: SVD from eigendecomposition` |
| 52 | SVD (application) | Compress an image with truncated SVD at rank k = 5, 20, 50. Plot the images and the energy curve `cumsum(σ²)/sum(σ²)`. Write `pinv(A)` (pseudo-inverse) from SVD. | `project: image compression with SVD` |

### Phase 6 — Applying to ML (BC sections 15, 22, 23, 25)

| Day | Study | Coding task | Commit |
|---|---|---|---|
| 53 | BC 15 › 001, 003, 004 (Linear Regression) | Fit the bootcamp's `USA_Housing` data with your `lstsq_qr`. Compare coefficients with `sklearn.linear_model.LinearRegression`. | `ml: linear regression from scratch vs sklearn` |
| 54 | BC 22 › 001 (PCA theory) | `pca(X, k)`: standardize → covariance matrix → eigenvalues/eigenvectors (using `eig_qr` or `svd_via_eig`). | `ml: PCA from scratch` |
| 55 | BC 22 › 002 (PCA with Python) | Run your PCA on `load_breast_cancer` as in the video. Compare with `sklearn.decomposition.PCA` (eigenvector signs may be flipped). Scatter-plot the 2 components. | `ml: PCA on breast cancer vs sklearn` |
| 56 | BC 23 › 001, 002 (Recommender) | Build the user × movie matrix from the bootcamp's MovieLens data. Compute movie similarity with your `cosine_similarity` from Day 8 (instead of `corrwith`). | `ml: item similarity with cosine` |
| 57 | BC 23 › 003 | Matrix factorization: truncated SVD on the rating matrix (fill blanks with the mean), predict ratings, measure RMSE on a test set. | `ml: SVD recommender` |
| 58 | BC 25 (Neural Nets, theory part) | Forward pass of a 2-layer network using only `matmul` and `einsum`: `X → XW₁+b₁ → ReLU → ·W₂+b₂`. Check shapes at every step. | `ml: neural net forward pass as matrix ops` |
| 59 | — | Backprop by hand (gradients are products with transposed matrices), train the network on 2D toy data, plot the decision boundary. | `ml: backprop with matrix calculus` |
| 60 | **Capstone** | Write a complete README: index of all 60 days, your best visuals (grid transforms, PageRank, SVD image compression, PCA). Tag `v1.0`. | `release: v1.0 Linear-Algebra-from-scratch` |

---

## 4. When you fall behind

- **Missed a day:** commit at least one new test or a `notes/dayXX.md`. Don't break the streak, but don't fake commits either.
- **A task is too hard:** split it over 2 days (Days 20–21, for example, can easily become 3). The 60 days are a frame; stretching to 75 is fine.
- **Review:** each phase ends with a review day. If tests are still red, fix them then.

## 5. End-of-roadmap checklist

- [ ] Solve linear systems, compute inverses and determinants with your own code
- [ ] Explain dot product, projection and change of basis with a drawing
- [ ] Implement Gram–Schmidt, QR, power iteration, PageRank
- [ ] Understand and implement SVD, use it for image compression and a recommender
- [ ] Your PCA and linear regression match scikit-learn
- [ ] Repo has green CI, a clear README, ~60 meaningful commits
