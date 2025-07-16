import re
import polars as pl

# サンプル DataFrame
df = pl.DataFrame({
    "id": [
        "332 or D4234 or 843",
        "ABC or 123 or XYZ or 456",
        "789 or SINGLE or 111 or TOKEN or 222",
        "JUSTTEXT",
        "12345",
    ],
    "name": ["foo", "bar", "baz", "qux", "quux"],
    "col2021": [
        "X1 or Y2 or 300 or Z3",
        "400 or Z5",
        "NO_CHANGE",
        "600",
        "A or B or 7 or C",
    ],
})

# 1) 対象カラムの抽出
cols_to_clean = [
    name
    for name, dtype in zip(df.columns, df.dtypes)
    if dtype == pl.Utf8
       and (name.lower() == "id" or any(ch.isdigit() for ch in name))
]

# 2) セル内文字列処理関数
def remove_numeric_tokens(s: str) -> str:
    # "or" を区切り文字として分割（前後の空白を含めない）
    tokens = re.split(r"\s*or\s*", s)
    # 純粋な数値トークンのみを取り除く
    filtered = [t for t in tokens if not re.fullmatch(r"\d+", t)]
    # 残ったトークンを " or " で再結合し、前後空白をトリム
    return " or ".join(filtered).strip()

# 3) 各セルに関数を適用し DataFrame を更新
df_clean = df.with_columns([
    pl.col(col)
      .apply(remove_numeric_tokens)  # Python UDFで数値トークンを除去
      .alias(col)
    for col in cols_to_clean
])

print(df_clean)
