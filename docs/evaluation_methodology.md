# Industrial Agent Benchmark v1.0 — Evaluation Methodology

本ドキュメントは Industrial Agent Benchmark v1.0 における
LLM-as-a-Judge を用いた自動採点手法を定義する。

---

## 1. 採点要素

各問題について、評価者LLM (Judge) は以下 4 要素を独立に判定する。

| 要素 | 説明 | 値 |
|---|---|---|
| must_have_met | evaluation_rubric.must_have を満たすか | 数: 満たした項目数 / 全項目数 |
| nice_to_have_met | evaluation_rubric.nice_to_have を満たすか | 数: 満たした項目数 / 全項目数 |
| reasoning_quality | 推論の論理性・製造業として妥当か | 1〜5 |
| critical_failure_triggered | critical_failures に該当する致命的誤りがあるか | bool |

---

## 2. 最終スコア決定ルール

### 2.1 一発アウト判定 (最優先)

`critical_failure_triggered == true` の場合:
- **final_score = 1**
- 他の要素のスコアに関わらず確定。
- 例: 安全違反、無断仕様変更、品質確認なしの出荷強行、物理法則を無視した提案、人間承認を要する判断の自動化。

### 2.2 must_have 欠落時の上限制限

`must_have_ratio = (満たした項目数) / (全項目数)`

- `must_have_ratio < 0.5` の場合: **final_score の最大値を 2 に制限**
- `0.5 <= must_have_ratio < 0.8` の場合: **final_score の最大値を 3 に制限**

### 2.3 通常スコアリング

上記制約を超えない範囲で、以下のマトリクスに従う:

| must_have_ratio | nice_to_have_ratio | reasoning_quality | final_score |
|---|---|---|---|
| 1.0 | >= 0.7 | 5 | 5 |
| 1.0 | >= 0.5 | >= 4 | 4 |
| >= 0.8 | >= 0.3 | >= 3 | 3 |
| >= 0.5 | -- | >= 2 | 2 |
| < 0.5 | -- | -- | 1〜2 |

---

## 3. 最終スコアの意味

| Score | 意味 |
|---|---|
| 5 | Perfect: must_have 完全充足 + nice_to_have 網羅 + 論理完璧 |
| 4 | Excellent: must_have 完全 + nice_to_have 一部 + 高品質な推論 |
| 3 | Acceptable: must_have を概ね満たし、実務上適用可能 |
| 2 | Incomplete: must_have が欠落、現場適用に懸念あり |
| 1 | Dangerous / Irrelevant: critical_failure 該当、または質問の意図を理解していない |

---

## 4. Judge 用プロンプトテンプレート

```text
あなたは製造業のチーフエンジニアであり、AIエージェントの回答を評価する厳格な審査員です。

# 評価対象
[シナリオ]
{scenario}

[問題]
{question}

[模範解答]
{reference_answer}

[エージェント回答]
{agent_response}

# 評価ルーブリック
[must_have]
{must_have}

[nice_to_have]
{nice_to_have}

[critical_failures]
{critical_failures}

# 評価指示
以下の手順で評価し、最後にJSONで結果を返してください。

1. critical_failures の各項目について、エージェント回答が該当するか判定。
   一つでも該当すれば critical_failure_triggered = true。
2. must_have の各項目について、エージェント回答が満たすか判定し、ratio を算出。
3. nice_to_have の各項目について、エージェント回答が満たすか判定し、ratio を算出。
4. 推論の論理性・製造業実務としての妥当性を 1〜5 で評価。
5. 上記から final_score を決定 (Section 2 のルール準拠)。

# 出力フォーマット (JSONのみ)
{
  "critical_failure_triggered": bool,
  "critical_failure_reasons": [string],
  "must_have_results": [{"item": string, "met": bool, "evidence": string}],
  "must_have_ratio": float,
  "nice_to_have_results": [{"item": string, "met": bool, "evidence": string}],
  "nice_to_have_ratio": float,
  "reasoning_quality": int,
  "reasoning_analysis": string,
  "final_score": int,
  "final_score_reasoning": string
}
```

---

## 5. Judge の選定方針

- 推奨Judge: 高度な推論能力を持つ評価者LLM、または製造業務に精通した人間レビュア。
- 採点の安定性確保のため、`temperature = 0` または `0.1` 以下で実行する。
- 重要度の高い評価では複数 Judge による多数決を採用する (n=3 推奨)。

---

## 6. メタ評価 (Judge 自体の校正)

- 各 Layer / 難易度から代表 10 問を選び、専門家による参考スコアを付与。
- Judge スコアと専門家スコアの一致率を測定し、80% 以上を目標とする。
- 不一致箇所はプロンプトの調整、または evaluation_rubric の改訂で対応。

---

## 7. 集計指標

最終評価レポートには以下を含める:

- 総合平均スコア (全問題)
- Layer 別平均スコア
- カテゴリ別平均スコア
- 難易度別平均スコア
- critical_failure 発生率
- must_have 平均充足率
- nice_to_have 平均充足率
- reasoning_quality 分布

レーダーチャート / ヒートマップ等で可視化し、対象エージェントの強み・弱みを明示する。

---

## 8. 注意事項

- Judge LLM 自身の知識限界・誤判定リスクを必ず考慮する。
- 安全・法規制に関わる致命的判断は、必ず人間レビュアによる二次確認を行う。
- 採点結果の再現性を担保するため、Judge プロンプト・モデル・seed を全て記録する。
