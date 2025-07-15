import polars as pl

# サンプルデータ
df = pl.DataFrame({
    "text_col": [
        "列車が火事を起こした",
        "apple orange",
        "banana grape",
        "cherry"
    ],
    "cond_col": [
        "(apple or banana)",
        "(apple and orange)",
        "(banana and grape) or apple",
        "not banana"
    ]
})

def eval_cond(text: str, cond: str) -> bool:
    """
    任意の ( )、and、or、not を含む簡易条件式を受け取り、
    text に対して評価した真偽値を返す。
    """
    # 1) トークン化：括弧まわりをスペースで分離
    toks = cond.replace("(", " ( ").replace(")", " ) ").split()
    # 2) 各トークンを Python 式に変換
    py_tokens = []
    for t in toks:
        lt = t.lower()
        if lt in ("and", "or", "not", "(", ")"):
            py_tokens.append(lt)
        else:
            # 単語 t が text に含まれるかをチェックする式に変換
            # repr() を使ってシングルクォート付き文字列リテラル化
            py_tokens.append(f"({repr(t)} in text)")
    # 3) 結合して式文字列を生成
    expr = " ".join(py_tokens)
    # 4) text をローカル変数にバインドして eval
    return eval(expr, {"__builtins__": {}}, {"text": text})

# Polars で struct+apply
result_df = df.with_columns(
    pl.struct(["text_col", "cond_col"])
      .map_elements(lambda row: eval_cond(row["text_col"], row["cond_col"]),return_dtype=pl.Boolean)
      .alias("satisfies")
)

print(result_df)
