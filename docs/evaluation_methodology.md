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


---

## 9. v1.1 採点方針 (Additive, Backward Compatible)

v1.1 では、上位モデル間の識別力を高めるために採点フローを拡張する。
**Section 1〜8 の v1.0 採点ロジックは変更せず**、`schema_version: "1.1"` の問題
(v1.1 新規 90 問) に対してのみ本章のロジックを適用する。
v1.0 既存問題 (`schema_version` 未指定 / `"1.0"`) は従来通り Section 1〜8 で採点する。

### 9.1 採点優先順位 (v1.1)

v1.1 問題の採点は以下の **厳密な順序** で実行する。
上位ステップで final_score が確定 (= 1) した場合、下位ステップは評価のみ行い記録するが
スコアには影響しない (透明性のため Judge ログには全項目を残す)。

| # | ステップ | 役割 | 早期確定 |
|---|---|---|---|
| 1 | `critical_failures` 判定 | v1.0 と同じ。一発アウト条件 | true → final_score = 1 |
| 2 | `disallowed_answers` 判定 | 禁則回答パターンとのマッチ | hit → final_score = 1 |
| 3 | `score_cap_rules` 評価 | 発火した rule の `max_score` を上限 caps に追加 | (上限を集める) |
| 4 | `numeric_checks` 採点 | 各 check の pass/fail を判定し numeric_pass_ratio を算出 | `required: true` の fail → final_score = 1 |
| 5 | `must_have` 判定 | v1.0 と同じ。must_have_ratio を算出 | (Section 2.2 の上限ルールを caps に追加) |
| 6 | `structured_output_requirements` 評価 | 必須キー充足 / フォーマット適合 | format 不正 (パース不能) → final_score = 1 |
| 7 | `generic_answer_penalty` 評価 | 条件発火で penalty を算出 (既定 -1, 下限 1) | (後段で減算) |
| 8 | `nice_to_have` 判定 | v1.0 と同じ。nice_to_have_ratio を算出 | — |
| 9 | `reasoning_quality` 採点 | v1.0 と同じ。1〜5 | — |

このうち **ステップ 1, 2, および 4 の `required: true` 失敗、ステップ 6 のフォーマット不正** が
final_score = 1 への早期確定経路となる。

### 9.2 最終スコア算出式 (v1.1)

```
matrix_score = v1.0 Section 2.3 マトリクスによる基本スコア
               (must_have_ratio, nice_to_have_ratio, reasoning_quality から決定)

caps = {5}
  + (must_have_ratio < 0.5 ⇒ {2})
  + (0.5 <= must_have_ratio < 0.8 ⇒ {3})
  + (numeric_pass_ratio < 0.25 ⇒ {2})
  + (0.25 <= numeric_pass_ratio < 0.5 ⇒ {3})
  + (structured_output_requirements.required かつ schema_pass = false ⇒ {3})
  + (score_cap_rules で発火した各 rule の max_score)

penalty = generic_answer_penalty.enabled かつ conditions のいずれか発火 ⇒ -1
        : それ以外 ⇒ 0

floor   = 1

final_score = max( min(matrix_score, min(caps)) + penalty , floor )
```

ただし、ステップ 1 / 2 / 4(required) / 6(format 不正) のいずれかが発火した場合、
上記計算をスキップして **final_score = 1** を即時返す。

### 9.3 score_cap_rules の適用順

- 各 rule の `condition` を Judge が独立に評価する。
- 発火した rule の `max_score` を `caps` 集合に追加し、最終的に `min(caps)` を採用する。
- 複数 rule が発火した場合、**最も厳しい (= 最小) max_score** が有効となる。
- `score_cap_rules` は **減点ではなく上限制限** として機能する。
  matrix_score が cap より小さい場合は cap は作用しない。

### 9.4 numeric_checks の採点方法

各 check `c` について、Judge は以下を行う:

1. エージェント回答から `c.name` に対応する数値を抽出 (単位を含めて識別)。
2. 抽出した値 `v` を `c.expected_value` と `c.tolerance` に照らして判定:
   - `tolerance = "exact"`: `v == expected`
   - `tolerance = "±X%"`: `|v - expected| / |expected| <= X/100`
   - `tolerance = "±X"`: `|v - expected| <= X`
   - `tolerance = "<="`/`">="`/`"<"`/`">"`: 比較演算
   - `expected_value = "[a, b]"`: `a <= v <= b`
3. 単位 (`c.unit`) が一致しない場合は **fail**。
4. 抽出できない (回答中に対応値なし) 場合は **fail**。
5. 計算過程は示されているが最終値が誤っている場合は **fail**。

```
numeric_pass_ratio = (pass した check 数) / (全 check 数)
```

`c.required = true` のチェックが 1 つでも fail した場合、final_score = 1 に早期確定する。
`required` 未指定 / false の check は pass_ratio にのみ寄与する。

### 9.5 generic_answer_penalty の減点方法

- `enabled: false` の場合は本ステップをスキップ (penalty = 0)。
- `enabled: true` の場合、`conditions` に列挙された各条件を Judge が独立に判定し、
  **いずれか 1 つ以上が発火** した時点で `penalty = -1` を確定する。
- 複数条件が発火しても **重複加算しない** (1 回適用)。
- 適用後の値が `floor (= 1)` を下回らないようクリップする。

各条件の判定基準:

| 条件 | 判定 |
|---|---|
| `scenario_specific_numbers_not_used` | シナリオ本文中の有意な数値 (3桁以上 or %値) のうち、回答中に再出現するものが 1/3 未満 |
| `no_priority_order` | 「優先順位」「順序」「最初に / 次に」等の順序語が一切なく、列挙が並列のみ |
| `no_tradeoff_analysis` | QCD (品質 / コスト / 納期) または安全のいずれかについてトレードオフ言及がない |
| `generic_framework_only` | "PDCA を回す", "5W1H で整理する" 等メタ手法のみで具体行動が欠落 |
| `no_named_stakeholder` | "品質保証責任者", "顧客 SQE", "工場長" 等の役割名が一切登場しない |

### 9.6 structured_output_requirements の評価方法

| 状況 | 扱い |
|---|---|
| `required: false` | 本ステップをスキップ |
| `format` 指定の形式でパースできない (例: JSON 構文エラー) | **final_score = 1 に早期確定** |
| `required_fields` のキーが欠落 | 欠落数を `must_have` の欠落件数に **加算** (Section 2.2 の must_have_ratio に反映) |
| `required_fields` のキーは存在するが値が空 / null | 欠落と同等扱い |
| 余剰キー | 既定では無視 (将来 `schema_strict` 導入時に厳格化) |

Judge は `structured_output_results = {schema_pass: bool, missing_fields: [...], parse_error: ...}` を出力に含める。

### 9.7 disallowed_answers の扱い

- 各エントリは自然言語の禁則条件文字列。
- Judge は回答全体に対し意味的にマッチするかを判定する。
- マッチした場合は **critical_failures と同等** と見なし、final_score = 1 を早期確定する。
- `critical_failures` と `disallowed_answers` は **論理 OR** で結合される
  (いずれかが発火すれば final_score = 1)。
- 両方が発火した場合は両方の発火理由を Judge 出力 (`critical_failure_reasons` /
  `disallowed_match_reasons`) に記録する。

### 9.8 critical_failures との優先順位関係

採点優先順位 (§9.1) のとおり、`critical_failures` (ステップ 1) と
`disallowed_answers` (ステップ 2) は両方とも **最優先** で評価され、
他のすべてのスコア要素より上位に位置する。

```
優先順位 (高 → 低):
  critical_failures
  disallowed_answers
  score_cap_rules
  numeric_checks (required: true は critical 相当に昇格)
  must_have
  structured_output_requirements (format パース不可は critical 相当に昇格)
  generic_answer_penalty
  nice_to_have
  reasoning_quality
```

すなわち、`disallowed_answers` ヒットや `numeric_checks (required)` 失敗は、
たとえ `must_have` を完全充足し `nice_to_have` も高水準でも、
**final_score = 1 を覆さない**。

### 9.9 Judge プロンプト追記 (v1.1)

v1.0 の Judge プロンプト (Section 4) に対して、`schema_version: "1.1"` の問題では
以下のセクションを追加する (実装は別タスクで判 template 更新時に行う):

```text
# 追加評価項目 (v1.1)
[disallowed_answers]
{disallowed_answers}

[score_cap_rules]
{score_cap_rules}

[numeric_checks]
{numeric_checks}

[structured_output_requirements]
{structured_output_requirements}

[generic_answer_penalty]
{generic_answer_penalty}

# 追加出力 JSON フィールド
{
  ...,
  "disallowed_match_reasons": [string],
  "score_cap_rules_fired": [{"condition": string, "max_score": int}],
  "numeric_check_results": [{"name": string, "extracted_value": string, "pass": bool, "evidence": string}],
  "numeric_pass_ratio": float,
  "structured_output_results": {"schema_pass": bool, "missing_fields": [string], "parse_error": string|null},
  "generic_answer_penalty_fired": [string],
  "applied_caps": [int],
  "applied_penalty": int
}
```

### 9.10 メタ評価 (Judge 校正) の v1.1 追加観点

- v1.1 新規 90 問のうち各カテゴリから 1 問ずつ計 11 問を「v1.1 校正セット」として人手スコア付与する。
- 校正セットで Judge の以下 4 項目について人手一致率 90% 以上を達成基準とする:
  - `numeric_check_results[*].pass`
  - `structured_output_results.schema_pass`
  - `disallowed_match_reasons` (該当の有無)
  - `score_cap_rules_fired` の rule ID 集合
- 未達の場合は `expected_value` / `tolerance` / `required_fields` / `disallowed_answers` 文言を再調整する。

### 9.11 適用範囲と互換性

- 本章は `schema_version: "1.1"` の問題にのみ適用される。
- v1.0 既存 90 問 (`schema_version` フィールドなし) は Section 1〜8 のロジックのみで採点され、
  本章の影響を受けない。
- 評価結果レポートにおいては、v1.0 と v1.1 のスコアを **同一指標 (1〜5)** として比較可能だが、
  v1.1 の方が score_cap や penalty により下方圧力が強いため、
  カテゴリ別 / schema_version 別の分布を併記することを推奨する。
