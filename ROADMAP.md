# Lộ trình Linear Algebra cho ML — 60 ngày, ngày nào cũng có commit

Nguồn học dùng trong lộ trình:

- **[LA]** `D:\Linear Algebra in ML` — *Mathematics for Machine Learning: Linear Algebra* (Imperial College, 5 module). Đây là xương sống lý thuyết.
- **[BC]** `D:\ML bootcamp` — *Python for Data Science & ML Bootcamp*. Dùng phần NumPy (mục 05) để khởi động, và các mục 15, 22, 23, 25 để áp dụng đại số tuyến tính vào ML thật.
- **Formula sheet:** `06_Resources\...\01__maths4ml-linearalgebra-formula.pdf`. In ra, dán cạnh bàn.

Ký hiệu đường dẫn video: `M2 › 02 › 01` nghĩa là module `02_vectors-...`, thư mục con `02_finding-...`, video `01_modulus-inner-product.mp4`.

---

## 1. Ý tưởng: một repo duy nhất, lớn dần mỗi ngày

Tạo repo GitHub tên `linalg-from-scratch`. Mỗi ngày bạn viết **một hàm tự cài đặt** (chỉ dùng Python thuần hoặc phép toán NumPy cơ bản, *không* gọi `np.linalg`), rồi viết **test so sánh với `np.linalg`**. Như vậy commit nào cũng có ý nghĩa, và cuối lộ trình bạn có một thư viện đại số tuyến tính nhỏ do chính mình viết.

```
linalg-from-scratch/
├── README.md              # nhật ký: ngày, chủ đề, link file
├── requirements.txt       # numpy, matplotlib, pytest
├── linalg/                # thư viện của bạn
│   ├── vectors.py
│   ├── matrices.py
│   ├── solve.py
│   ├── transforms.py
│   ├── eigen.py
│   └── decomp.py
├── tests/                 # test_<module>.py, so với np.linalg
├── notebooks/             # dayXX_<chu-de>.ipynb: hình vẽ, thí nghiệm
└── notes/                 # dayXX.md: tóm tắt lý thuyết bằng lời của bạn
```

**Quy tắc mỗi ngày (45–90 phút):**

1. 📺 Xem video trong cột *Học* (bật phụ đề `_vi.srt` nếu cần).
2. ✍️ Làm tay 2–3 ví dụ nhỏ trên giấy, ghi `notes/dayXX.md` (5–10 dòng).
3. 💻 Làm bài code trong cột *Bài code*, chạy `pytest` cho xanh.
4. ✅ `git add . && git commit -m "<message gợi ý>" && git push`.

**Để ô GitHub thật sự xanh:**

- Email trong `git config user.email` phải trùng email đã thêm vào tài khoản GitHub.
- Commit phải nằm trên nhánh mặc định (`main`) hoặc nhánh `gh-pages`, và repo không được là fork.
- Repo private chỉ hiện ô xanh khi bật *Settings → Profile → Private contributions*.
- Bonus: thêm GitHub Actions chạy `pytest` mỗi lần push (Ngày 3) để mỗi commit có dấu ✓.

> Ô xanh chỉ là phần thưởng phụ. Commit thật, có nội dung, mới làm hồ sơ của bạn có giá trị khi nhà tuyển dụng bấm vào xem.

---

## 2. Tổng quan

| Giai đoạn | Ngày | Nội dung | Nguồn |
|---|---|---|---|
| 0. Khởi động | 1–3 | NumPy, setup repo, CI | BC 05 |
| 1. Vector | 4–14 | Phép toán, dot product, projection, đổi cơ sở, độc lập tuyến tính | LA M1, M2 |
| 2. Ma trận | 15–24 | Biến đổi, nhân ma trận, Gauss, nghịch đảo, định thức | LA M3 |
| 3. Ánh xạ tuyến tính | 25–34 | Einstein summation, đổi cơ sở cho ma trận, trực giao, Gram–Schmidt, phản xạ | LA M4 |
| 4. Trị riêng | 35–44 | Eigen, chéo hóa, power iteration, PageRank | LA M5 |
| 5. Lấp chỗ trống | 45–52 | Rank, null space, chuẩn, least squares, QR, SVD | Ngoài khóa (xem mục 4) |
| 6. Áp dụng vào ML | 53–60 | Hồi quy tuyến tính, PCA, recommender, neural net, capstone | BC 15, 22, 23, 25 |

Lý do có giai đoạn 5: khóa Imperial **không dạy SVD và least squares**, trong khi đó là hai công cụ quan trọng nhất của đại số tuyến tính trong ML (PCA và recommender system của bootcamp đều dựa trên chúng).

---

## 3. Lịch chi tiết

### Giai đoạn 0 — Khởi động (BC mục 05)

| Ngày | Học | Bài code | Commit |
|---|---|---|---|
| 1 | BC 05 › 002, 003 (NumPy arrays) | Tạo repo, `README.md`, `requirements.txt`, `.gitignore`. Notebook `day01_numpy.ipynb`: tạo vector, ma trận, `shape`, `reshape`, `arange`, `linspace`, `eye`. | `init: project skeleton + numpy basics` |
| 2 | BC 05 › 005, 006 (indexing, operations) | Notebook: slicing, boolean mask, broadcasting. Viết hàm `as_vector(x)` trong `linalg/vectors.py` nhận list hoặc array, trả về array 1D float, báo lỗi nếu không phải 1D. Test đầu tiên trong `tests/test_vectors.py`. | `feat: as_vector + first pytest` |
| 3 | BC 05 › 007, 008 (exercises) | Làm lại bộ bài NumPy Exercises không xem lời giải. Thêm `.github/workflows/test.yml` chạy `pytest` trên mỗi push. | `ci: run pytest on push` |

### Giai đoạn 1 — Vector (LA Module 1–2)

| Ngày | Học | Bài code | Commit |
|---|---|---|---|
| 4 | M1 › 01 › 01; M1 › 02 › 01, 02 | `notes/day04.md`: vì sao ML cần đại số tuyến tính (fit tham số = tìm điểm trong không gian tham số). Notebook: vẽ hàm lỗi SSE của mô hình `y = m·x + c` trên lưới (m, c) bằng `contourf`. | `notebook: parameter space contour` |
| 5 | M1 › 02, bài *exploring-parameter-space* và *solving-simultaneous-equations* | Làm 2 bài tập trong file `.html`. Code `add(u, v)`, `scale(k, v)` bằng vòng lặp, test với `u + v`, `k * v`. | `feat: vector add and scale` |
| 6 | M1 › 03 › 01 + bài *doing-some-vector-operations*; M1 › 04 › 01 | `sub`, `linear_combination(coeffs, vectors)`. Notebook: vẽ phép cộng vector bằng `plt.quiver` (quy tắc hình bình hành). | `feat: linear combination + quiver plot` |
| 7 | M2 › 01 › 01; M2 › 02 › 01 (modulus, inner product) | `dot(u, v)`, `norm(v)` (L2). Test với `np.dot`, `np.linalg.norm`. Test thêm tính chất: `dot(u,v) == dot(v,u)`, `dot(v,v) == norm(v)**2`. | `feat: dot product and L2 norm` |
| 8 | M2 › 02 › 02 (cosine) | `angle(u, v)` trả về radian, có `np.clip` để tránh lỗi làm tròn ngoài [-1, 1]. `cosine_similarity(u, v)`. Notebook: so sánh độ giống nhau của vài “vector từ” đồ chơi. | `feat: angle and cosine similarity` |
| 9 | M2 › 02 › 03 (projection) + bài *dot-product-of-vectors* | `scalar_projection(s, r)` và `vector_projection(s, r)` (chiếu s lên r). Notebook: vẽ hình chiếu. | `feat: scalar and vector projection` |
| 10 | M2 › 03 › 01 (changing basis) + bài *changing-basis* | `change_basis_orthogonal(v, basis)`: đổi tọa độ v sang cơ sở trực giao bằng phép chiếu. Test: dựng lại v từ tọa độ mới phải ra v gốc. | `feat: change of basis via projection` |
| 11 | M2 › 03 › 03 (basis, linear independence) | `is_linearly_independent(vectors)`. Hôm nay dùng cách “ngây thơ” cho 2D/3D (định thức hoặc kiểm tra tỉ lệ). Ngày 46 sẽ viết lại bằng rank. | `feat: linear independence check (2D/3D)` |
| 12 | M2 › 03 › 04, 05 (applications + bài *linear-dependency*) | Notebook: chiếu một đám điểm 2D lên đường thẳng tốt nhất bạn đoán được, đo tổng khoảng cách. (Đây là PCA thô sơ, nhớ lại ở Ngày 54.) | `notebook: projecting noisy data onto a line` |
| 13 | M2 › 04 › 01 (vector-operations-assessment) | Làm bài assessment. Giải từng câu bằng code trong `notebooks/day13_assessment.ipynb`, đối chiếu với đáp án tay. | `practice: module 2 assessment in code` |
| 14 | M2 › 04 › 02 (summary) — **ôn tập** | Viết `README` cho `linalg/vectors.py` (docstring đủ cho mọi hàm). Tăng test lên mỗi hàm ít nhất 3 case, gồm case biên (vector 0, vector song song). | `docs+test: polish vectors module` |

### Giai đoạn 2 — Ma trận (LA Module 3)

| Ngày | Học | Bài code | Commit |
|---|---|---|---|
| 15 | M3 › 01 › 01 (matrices & simultaneous equations) | `linalg/matrices.py`: `matvec(A, v)` bằng 2 vòng lặp. Test với `A @ v`. | `feat: matrix-vector product` |
| 16 | M3 › 02 › 01 (how matrices transform space) | Notebook: vẽ lưới ô vuông và ảnh của nó qua ma trận 2×2 bất kỳ. Viết hàm `plot_transform(A)` dùng lại được. | `viz: plot 2D linear transformation` |
| 17 | M3 › 02 › 02 (types of transformation) | `rotation(theta)`, `scaling(sx, sy)`, `shear(k)`, `reflection_x()`, `reflection_y()` trong `linalg/transforms.py`. Vẽ từng cái bằng `plot_transform`. | `feat: 2D transformation constructors` |
| 18 | M3 › 02 › 03 (composition) + bài *using-matrices-to-make-transformations* | `matmul(A, B)` bằng 3 vòng lặp, test với `A @ B`. Test thêm: `matmul(A, B) != matmul(B, A)` nói chung; xoay 90° hai lần = xoay 180°. | `feat: matmul + composition tests` |
| 19 | — (ngày luyện) | `transpose(A)`, `identity(n)`, `is_symmetric(A)`. Benchmark `matmul` của bạn vs `@` với n = 50, 100, 200, ghi kết quả vào notes. | `feat: transpose/identity + benchmark` |
| 20 | M3 › 03 › 01 (Gaussian elimination) | `linalg/solve.py`: `row_echelon(A)` (khử Gauss, có hoán đổi hàng khi pivot = 0). | `feat: gaussian elimination to row echelon` |
| 21 | M3 › 03 › 01 (xem lại) | `back_substitution(U, b)` và `solve(A, b)` = khử + thế ngược. Test với `np.linalg.solve` trên ma trận ngẫu nhiên 3×3 đến 10×10. | `feat: solve linear system` |
| 22 | M3 › 03 › 02 (from elimination to inverse) | `inverse(A)` bằng Gauss–Jordan trên `[A | I]`. Test `A @ inverse(A) ≈ I`. Ném `ValueError` nếu ma trận suy biến. | `feat: inverse via gauss-jordan` |
| 23 | M3 › 03 › 03 (bài *solving-linear-equations-using-the-inverse*); M3 › 04 › 01 (determinants) | `det(A)`: (a) khai triển cofactor đệ quy, (b) tích đường chéo sau khử Gauss (nhớ đổi dấu khi hoán đổi hàng). So tốc độ hai cách với n = 8. | `feat: determinant two ways` |
| 24 | M3 › 04 › 02 (summary) — **ôn tập** | Bài toán “táo và chuối” trong video: lập hệ, giải bằng `solve` của bạn. Thêm test: `det(AB) = det(A)·det(B)`, `det(A) = 0` ⇔ `inverse` báo lỗi. | `test: matrix properties` |

### Giai đoạn 3 — Ánh xạ tuyến tính (LA Module 4)

| Ngày | Học | Bài code | Commit |
|---|---|---|---|
| 25 | M4 › 01 › 01 (Einstein summation) | Viết lại `dot`, `matvec`, `matmul`, `transpose`, `trace` bằng `np.einsum` trong `notebooks/day25_einsum.ipynb`. Test kết quả khớp bản tự viết. | `notebook: einsum versions of core ops` |
| 26 | — (ngày luyện einsum) | Dùng `einsum` cho: batch matmul (shape `(b,n,m)·(b,m,k)`), outer product, tổng các phần tử đường chéo. Đây là kỹ năng dùng thẳng trong PyTorch. | `practice: batched einsum` |
| 27 | M4 › 02 › 01 (matrices changing basis) | `to_basis(v, B)` và `from_basis(v_b, B)` cho cơ sở **không** trực giao (dùng `inverse` hoặc `solve`). Test vòng đi vòng về. | `feat: change of basis (general)` |
| 28 | M4 › 02 › 02 (transformation in a changed basis) | `transform_in_basis(A, B)` = `B⁻¹ A B`. Ví dụ: xoay 45° viết trong một cơ sở lệch. Vẽ để kiểm chứng. | `feat: similarity transform B^-1 A B` |
| 29 | M4 › 03 › 01 (orthogonal matrices) | `is_orthogonal(A)`. Test: ma trận xoay là trực giao; `Aᵀ = A⁻¹`; `det = ±1`; nhân vector không làm đổi `norm`. | `feat: orthogonal matrix check` |
| 30 | M4 › 04 › 01 (Gram–Schmidt) | `linalg/decomp.py`: `gram_schmidt(vectors)` trả về cơ sở trực chuẩn. Bỏ qua vector phụ thuộc tuyến tính (norm < 1e-10). | `feat: gram-schmidt` |
| 31 | M4 › 04 › 01 (xem lại) | Viết **modified** Gram–Schmidt. Thí nghiệm: với các vector gần song song, so `‖QᵀQ − I‖` của bản cổ điển và bản modified. Ghi nhận xét. | `experiment: classical vs modified GS` |
| 32 | M4 › 04 › 02 (reflecting in a plane) | `reflect_in_plane(v, basis_of_plane)`: dùng Gram–Schmidt dựng cơ sở trực chuẩn E, phản xạ trong cơ sở đó, rồi đổi về: `E T E⁻¹`. | `feat: reflection in a plane` |
| 33 | — (ngày luyện) | Ứng dụng nhỏ: nén ảnh xám bằng phép chiếu lên k vector cơ sở trực chuẩn (ví dụ k hàng đầu của ma trận ảnh sau Gram–Schmidt). Vẽ ảnh gốc vs ảnh dựng lại. | `notebook: projection-based image compression` |
| 34 | **Ôn tập Module 3–4** | Mỗi hàm trong `matrices.py`, `solve.py`, `transforms.py`, `decomp.py` có docstring + ≥3 test. Cập nhật bảng tiến độ trong README. | `docs+test: polish matrices & mappings` |

### Giai đoạn 4 — Trị riêng & PageRank (LA Module 5)

| Ngày | Học | Bài code | Commit |
|---|---|---|---|
| 35 | M5 › 01 › 01, 02 (what are eigen-things) | Notebook: dùng `plot_transform`, tô màu các vector **không đổi hướng** sau biến đổi. Tìm bằng mắt eigenvector của scaling, shear, rotation. | `viz: eigenvectors visually` |
| 36 | M5 › 02 › 01 (special eigen cases) | `eig_2x2(A)`: giải phương trình đặc trưng `λ² − tr(A)λ + det(A) = 0`, xử lý trường hợp nghiệm phức (xoay). Test với `np.linalg.eig`. | `feat: closed-form 2x2 eigen` |
| 37 | M5 › 02 › 02 (calculating eigenvectors) | Với mỗi λ, tìm eigenvector bằng cách giải `(A − λI)x = 0`. Test `A v ≈ λ v`. | `feat: eigenvectors from null space` |
| 38 | — (thuật toán) | `linalg/eigen.py`: `power_iteration(A, iters, tol)` trả về trị riêng lớn nhất + vector. Vẽ đồ thị hội tụ theo số vòng lặp. | `feat: power iteration` |
| 39 | — (thuật toán) | `inverse_iteration(A, mu)` tìm trị riêng gần `mu` nhất. Thêm deflation để lấy 2–3 trị riêng lớn nhất của ma trận đối xứng. | `feat: inverse iteration + deflation` |
| 40 | M5 › 03 › 01 (changing to the eigenbasis) | `diagonalize(A)` trả về `C, D` với `A = C D C⁻¹`. `matrix_power(A, n)` qua chéo hóa; so với nhân lặp n lần. | `feat: diagonalization + fast power` |
| 41 | M5 › 03 › 02 (eigenbasis example) | Ứng dụng: số Fibonacci thứ n bằng chéo hóa ma trận `[[1,1],[1,0]]`. So kết quả với vòng lặp cho n ≤ 70. | `notebook: fibonacci via eigen` |
| 42 | M5 › 04 › 01 (PageRank) | `pagerank(link_matrix, d=0.85)` bằng power iteration trên mạng nhỏ 6 trang trong video. Test tổng rank = 1. | `feat: pagerank` |
| 43 | — (dự án mini) | Áp PageRank vào đồ thị thật: tự viết hoặc tải một danh sách cạnh nhỏ (ví dụ các trang Wikipedia bạn tự chọn và liên kết giữa chúng). In top 10. | `project: pagerank on a real graph` |
| 44 | M5 › 05 › 01, 02 (summary, wrap-up) — **ôn tập** | Làm lại các bài tập khóa học trong `.html` mà bạn làm sai lần đầu. Viết `notes/module-recap.md` tóm tắt 5 module trong một trang. | `docs: course recap` |

### Giai đoạn 5 — Lấp chỗ trống (ngoài khóa Imperial)

Tài liệu gợi ý: *3Blue1Brown — Essence of Linear Algebra* (YouTube, xem chương tương ứng), *Gilbert Strang — MIT 18.06* (bài 9–10, 14–17, 29), sách *Mathematics for Machine Learning* (Deisenroth và cộng sự, bản PDF miễn phí, chương 2–4).

| Ngày | Chủ đề | Bài code | Commit |
|---|---|---|---|
| 45 | Rank, reduced row echelon form | `rref(A)` và `rank(A)`. Test với `np.linalg.matrix_rank`. | `feat: rref and rank` |
| 46 | Column space, null space | `null_space(A)` từ RREF. Viết lại `is_linearly_independent` bằng `rank` (cho mọi chiều). Test: `A @ null_space(A) ≈ 0`. | `refactor: independence via rank + null space` |
| 47 | Các chuẩn vector và ma trận | `norm(v, p)` cho p = 1, 2, ∞; `frobenius(A)`. Notebook: vẽ “quả cầu đơn vị” của L1, L2, L∞ (liên hệ Lasso/Ridge). | `feat: p-norms + unit ball plot` |
| 48 | Least squares, phương trình chuẩn | `lstsq_normal(A, b)` giải `AᵀA x = Aᵀb`. Fit đường thẳng và parabol vào dữ liệu nhiễu. Test với `np.linalg.lstsq`. | `feat: least squares via normal equations` |
| 49 | Phân tích QR | `qr(A)` dùng Gram–Schmidt từ Ngày 30. `lstsq_qr(A, b)`. So độ chính xác với phương trình chuẩn khi A gần suy biến (số điều kiện lớn). | `feat: QR + stable least squares` |
| 50 | Thuật toán QR tìm trị riêng | `eig_qr(A)`: lặp `A ← RQ`. Test trên ma trận đối xứng với `np.linalg.eigh`. | `feat: QR algorithm for eigenvalues` |
| 51 | SVD (lý thuyết) | `svd_via_eig(A)`: lấy V và σ từ trị riêng của `AᵀA`, rồi `U = AV/σ`. Test dựng lại `A ≈ U Σ Vᵀ`. | `feat: SVD from eigendecomposition` |
| 52 | SVD (ứng dụng) | Nén ảnh bằng SVD rút gọn hạng k = 5, 20, 50. Vẽ ảnh và đồ thị năng lượng `cumsum(σ²)/sum(σ²)`. Viết `pinv(A)` (giả nghịch đảo) từ SVD. | `project: image compression with SVD` |

### Giai đoạn 6 — Áp dụng vào ML (BC mục 15, 22, 23, 25)

| Ngày | Học | Bài code | Commit |
|---|---|---|---|
| 53 | BC 15 › 001, 003, 004 (Linear Regression) | Fit dữ liệu `USA_Housing` của bootcamp bằng `lstsq_qr` của bạn. So hệ số với `sklearn.linear_model.LinearRegression`. | `ml: linear regression from scratch vs sklearn` |
| 54 | BC 22 › 001 (PCA lý thuyết) | `pca(X, k)`: chuẩn hóa → ma trận hiệp phương sai → trị riêng/vector riêng (dùng `eig_qr` hoặc `svd_via_eig`). | `ml: PCA from scratch` |
| 55 | BC 22 › 002 (PCA with Python) | Chạy PCA tự viết trên `load_breast_cancer` như trong video. So với `sklearn.decomposition.PCA` (chú ý dấu của vector có thể ngược). Vẽ scatter 2 thành phần. | `ml: PCA on breast cancer vs sklearn` |
| 56 | BC 23 › 001, 002 (Recommender) | Dựng ma trận user × movie từ dữ liệu MovieLens trong bootcamp. Tính độ tương đồng phim bằng `cosine_similarity` của Ngày 8 (thay cho `corrwith`). | `ml: item similarity with cosine` |
| 57 | BC 23 › 003 | Matrix factorization: SVD rút gọn trên ma trận rating (điền trung bình vào ô trống), dự đoán rating, đo RMSE trên tập test. | `ml: SVD recommender` |
| 58 | BC 25 (Neural Nets, phần lý thuyết) | Forward pass của mạng 2 lớp chỉ bằng `matmul` và `einsum`: `X → XW₁+b₁ → ReLU → ·W₂+b₂`. Kiểm tra shape từng bước. | `ml: neural net forward pass as matrix ops` |
| 59 | — | Backprop bằng tay (gradient là các phép nhân ma trận chuyển vị), train mạng trên dữ liệu 2D đồ chơi, vẽ biên quyết định. | `ml: backprop with matrix calculus` |
| 60 | **Capstone** | Viết README hoàn chỉnh: mục lục 60 ngày, ảnh minh họa đẹp nhất (biến đổi lưới, PageRank, SVD nén ảnh, PCA). Gắn tag `v1.0`. | `release: v1.0 linalg-from-scratch` |

---

## 4. Khi bị chậm tiến độ

- **Không kịp một ngày:** commit ít nhất một test mới hoặc một ghi chú `notes/dayXX.md`. Không bỏ trống chuỗi, nhưng cũng không bịa commit.
- **Một bài quá khó:** chia nhỏ ra 2 ngày (ví dụ Ngày 20–21 dư sức tách thành 3). Lộ trình 60 ngày là khung, kéo dài thành 75 ngày vẫn ổn.
- **Đọc lại:** cuối mỗi giai đoạn có một ngày ôn tập. Nếu test còn đỏ, sửa vào ngày đó.

## 5. Checklist cuối lộ trình

- [ ] Tự giải hệ phương trình, tính nghịch đảo, định thức bằng code của mình
- [ ] Giải thích được dot product, projection, đổi cơ sở bằng hình vẽ
- [ ] Viết được Gram–Schmidt, QR, power iteration, PageRank
- [ ] Hiểu và tự cài SVD, dùng nó cho nén ảnh và recommender
- [ ] PCA và linear regression tự viết cho kết quả khớp scikit-learn
- [ ] Repo có CI xanh, README rõ ràng, ~60 commit có nội dung
