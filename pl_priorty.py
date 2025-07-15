import polars as pl

# サンプル DataFrame
df = pl.DataFrame({
    "id":       [1, 1, 1, 2, 2, 3],
    "priority": [10, 20,  5, 30, 15,  7],
    "flag":     [True, False, True, False, False, True]
})

# ソート（flag True → False、priority 大 → 小 の順）
df_sorted = df.sort(
    by=["flag", "priority"],descending=[True, True]
)  # flag: descending, priority: descending :contentReference[oaicite:0]{index=0}

# id 列で重複を除去し、先頭（Trueかつ最大priority の組み合わせ）を残す
result = df_sorted.unique(
    subset="id",
    keep="first"
)  # subset=id, keep=first :contentReference[oaicite:1]{index=1}

print(result)
