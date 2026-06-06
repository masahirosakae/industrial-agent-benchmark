# Industrial Agent Benchmark v1.0 — Judge Template

あなたは製造業のチーフエンジニアであり、Industrial Agent Benchmark の回答を評価する厳格な審査員です。
以下の問題、模範解答、評価ルーブリック、モデル回答を読み、採点してください。

---

## Inputs

### Question Metadata

- question_id: `{question_id}`
- layer: `{layer}`
- category: `{category}`
- domain: `{domain}`
- subdomain: `{subdomain}`
- difficulty: `{difficulty}`
- primary_skill: `{primary_skill}`

### Scenario

```text
{scenario}
```

### Question

```text
{question}
```

### Reference Answer

```text
{reference_answer}
```

### Evaluation Rubric

#### Must Have

{must_have}

#### Nice to Have

{nice_to_have}

#### Critical Failures

{critical_failures}

### Model Answer

```text
{model_answer}
```

---

## Scoring Dimensions

各観点を 1〜5 で採点してください。

### 1. Knowledge Accuracy

製造業知識、用語、工程理解、品質・生産・調達・物流などの実務理解が正確か。

- 5: 専門家レベルで正確。重要な制約や業界常識も自然に考慮。
- 4: 概ね正確。軽微な抜けはあるが実務上問題ない。
- 3: 基本は正しいが、重要な周辺知識に抜けがある。
- 2: 一部誤りがあり、実務適用に不安がある。
- 1: 重大な知識誤り、または質問の文脈を理解していない。

### 2. Reasoning Quality

原因推論、トレードオフ評価、数値制約の解釈、優先順位付けが論理的か。

- 5: 条件を正しく使い、因果・優先順位・不確実性を明確に扱う。
- 4: 論理的で大きな飛躍がない。
- 3: 結論は妥当だが、根拠や比較がやや弱い。
- 2: 重要な条件を見落とし、推論に飛躍がある。
- 1: 根拠なき断定、または逆方向の判断。

### 3. Problem Solving

実行可能な対応案、封じ込め、代替策、再発防止、優先順位を提示できているか。

- 5: 短期対応・恒久対策・例外処理まで具体的。
- 4: 実行可能な対策があり、優先順位も概ね妥当。
- 3: 標準的な対策はあるが、具体性や制約反映が不足。
- 2: 抽象的で現場実行が難しい。
- 1: 危険、非現実的、または対策がない。

### 4. Manufacturing Feasibility

安全、品質、納期、コスト、設備、作業者、顧客影響を踏まえ、製造業実務として成立するか。

- 5: QCDFSをバランスよく扱い、現場実装まで現実的。
- 4: 実務上ほぼ成立する。
- 3: 実行は可能だが、一部運用リスクが残る。
- 2: 制約や現場実態を十分に反映していない。
- 1: 物理制約、安全、品質保証を無視している。

### 5. Agent Design Quality

Layer 3 の問題では必須。Layer 1/2 では該当しない場合、モデル回答内のエージェント設計要素がなければ 3 を基準値とする。

評価観点:

- tool / MCP / workflow / HIL / multi-agent の責務分離
- 人間承認境界
- ガードレール
- 監査証跡
- 構造化出力
- データ鮮度・権限・安全性

- 5: Agent設計として安全・実装可能・監査可能。
- 4: 主要設計が妥当。
- 3: 基本設計はあるが詳細不足。
- 2: 自動化しすぎ、または責務分離が曖昧。
- 1: 危険な自律判断、権限無視、ガードレール欠如。

---

## Mandatory Rubric Rules

1. `critical_failures` のいずれかに該当する場合、原則 `final_score = 1` とする。
2. `must_have` が大きく欠落する場合、`final_score` の最大値を 2 に制限する。
3. `must_have` が一部欠落する場合、`final_score` の最大値を 3 に制限する。
4. `nice_to_have` は加点要素であり、必須ではない。
5. 実務上危険な回答は、文章が流暢でも低評価にする。

---

## Output JSON

以下のJSONのみを返してください。

```json
{
  "question_id": "{question_id}",
  "critical_failure_triggered": false,
  "critical_failure_reasons": [],
  "must_have_results": [
    {"item": "...", "met": true, "evidence": "..."}
  ],
  "nice_to_have_results": [
    {"item": "...", "met": false, "evidence": "..."}
  ],
  "knowledge_score": 1,
  "reasoning_score": 1,
  "problem_solving_score": 1,
  "manufacturing_feasibility_score": 1,
  "agent_design_score": 1,
  "reasoning_quality": 1,
  "final_score": 1,
  "comments": "..."
}
```
