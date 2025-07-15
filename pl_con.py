import polars as pl

# サンプルデータフレーム
df = pl.DataFrame({
    "list_col": [["a", "b", "c"], ["d", "e"]],
    "str_col": ["X", "Y"]
})

# リスト型と文字列を結合する
result = df.with_columns([
    pl.concat_str([
        pl.col("list_col").list.join(","),  # リスト内をカンマ区切りで結合
        pl.lit(","),                       # リテラル文字列を挿入
        pl.col("str_col")                  # その後 str_col を連結
    ]).alias("combined")
])

print(result)
