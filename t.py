import re
from collections import deque
from typing import Callable, List

# トークンの種類
TOKEN_PATTERN = re.compile(r"""\s*(
    \(|\)           # 丸括弧
  | and\b           # 論理積
  | or\b            # 論理和
  | [^\s()]+        # 単語（括弧・空白以外の連続文字列）
)\s*""", flags=re.IGNORECASE | re.VERBOSE)

# 演算子の優先順位
PRECEDENCE = {
    'or': 1,
    'and': 2,
}

def tokenize(expr: str) -> List[str]:
    """
    文字列をトークンのリストに分割
    例: "(apple or orange) and banana" → ['(', 'apple', 'or', 'orange', ')', 'and', 'banana']
    """
    tokens = TOKEN_PATTERN.findall(expr)
    return [tok.strip() for tok in tokens]

def to_rpn(tokens: List[str]) -> List[str]:
    """
    シャントイングヤードアルゴリズムで中置記法→逆ポーランド記法（RPN）に変換
    """
    output_queue = []
    op_stack = []

    for tok in tokens:
        lower = tok.lower()
        if lower in ('and', 'or'):
            # 演算子の場合
            while op_stack:
                top = op_stack[-1]
                if top.lower() in PRECEDENCE and PRECEDENCE[top.lower()] >= PRECEDENCE[lower]:
                    output_queue.append(op_stack.pop())
                else:
                    break
            op_stack.append(lower)
        elif tok == '(':
            op_stack.append(tok)
        elif tok == ')':
            # 左括弧までポップ
            while op_stack and op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            op_stack.pop()  # '(' を除去
        else:
            # 単語（オペランド）
            output_queue.append(tok)

    # 残った演算子を出力
    while op_stack:
        output_queue.append(op_stack.pop())

    return output_queue

def eval_rpn(rpn: List[str], evaluator: Callable[[str], bool]) -> bool:
    """
    RPN を評価。単語の真偽は evaluator() で判定。
    """
    stack = []
    for tok in rpn:
        lower = tok.lower()
        if lower == 'and':
            b = stack.pop()
            a = stack.pop()
            stack.append(a and b)
        elif lower == 'or':
            b = stack.pop()
            a = stack.pop()
            stack.append(a or b)
        else:
            # 単語トークン
            result = evaluator(tok)
            stack.append(result)
    if len(stack) != 1:
        raise ValueError("RPN evaluation error: stack = {}".format(stack))
    return stack[0]

def evaluate(expr: str, evaluator: Callable[[str], bool]) -> bool:
    """
    1) トークン化  2) RPN 変換  3) 評価
    """
    tokens = tokenize(expr)
    rpn = to_rpn(tokens)
    return eval_rpn(rpn, evaluator)

# ————————————————
# 使用例
# ————————————————
if __name__ == "__main__":
    # 判定の対象となる「現状持っている単語」の集合
    have = {"apple", "banana", "cherry"}

    # evaluator を定義
    def has_word(w: str) -> bool:
        return w.lower() in have

    tests = [
        "(apple or orange) and banana",       # True
        "apple and (banana or date)",         # True
        "(apple and orange) or (banana and cherry)",  # True
        "apple and orange",                   # False
        "(kiwi or lemon) and cherry",         # False
    ]

    for expr in tests:
        print(f"{expr:40} → {evaluate(expr, has_word)}")
