# Machine learning from scratch

Tự cài đặt đại số tuyến tính bằng Python và NumPy, rồi dùng chính thư viện đó cho các thuật toán ML: hồi quy tuyến tính, PCA, recommender, neural net.

Lộ trình 60 ngày: [ROADMAP.md](ROADMAP.md). Mỗi ngày một hàm mới và test đối chiếu với `np.linalg`.

## Cấu trúc

```
linalg/      thư viện tự viết (không dùng np.linalg bên trong)
tests/       pytest, đối chiếu kết quả với NumPy
notebooks/   thí nghiệm, hình vẽ: dayXX_<chu-de>.ipynb
notes/       ghi chú lý thuyết: dayXX.md (mẫu: notes/_template.md)
```

## Chạy

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
```

## Tiến độ

| Ngày | Chủ đề | Code | Ghi chú |
|---|---|---|---|
| 01 | NumPy cơ bản, dựng repo | [notebook](notebooks/day01_numpy.ipynb) | [notes](notes/day01.md) |
