# Industrial Agent Benchmark v1.1.0-pre

> Manufacturing 版 Humanity's Last Exam を目指す、製造業エージェント評価ベンチマーク

本リポジトリは、製造業ドメインにおける AI エージェントの能力を、
**専門知識 / 推論 / 問題解決 / Agent 設計** の 4 観点から総合評価するための
ベンチマークデータセットおよび評価方法を提供する。

> ℹ️ 現在の状態: **v1.1.0-pre (プレリリース)**  
> 凍結済みの既存問題群を保持し、v1.1-pre で 140 問へ拡張、Judge v2 と `evaluation_set_v2` を追加した。  
> 詳細は [`docs/v1.1_release_notes.md`](docs/v1.1_release_notes.md) と [`docs/public_evaluation_summary.md`](docs/public_evaluation_summary.md) を参照。

---

## 1. 目的

単純な定義・暗記問題ではなく、以下の能力を評価する。

1. **製造業専門知識** — 受注、生産計画、調達、品質、出荷、保全、変更管理など実務知識の状況判断
2. **製造業推論能力** — FTA / 5Why / FMEA / CAPA / トレードオフ判断 / データ整合性評価
3. **製造業問題解決能力** — 数値条件・矛盾データ・顧客承認・規制制約下の意思決定
4. **Industrial Agent 能力** — Tool Trajectory、HIL Boundary、Agent Safety、Structured Decision、構造化出力、権限境界

---

## 2. バージョン

| バージョン | 状態 | 内容概要 |
|---|---|---|
| v1.0 | 凍結 | 90 問 + LLM-as-a-Judge 基本評価方法 |
| **v1.1.0-pre** | **プレリリース (本リリース)** | 140 問 + Judge v2 + `evaluation_set_v2` + 識別力検証結果 |
| v1.1.0 | 計画中 | v1.1-pre + Change Control / Compliance / Factory Management / Numeric Capacity Planning |
| v1.2 | 計画中 | Robotics & Automation、サプライチェーン制約、規制連動シナリオ |
| v2.0 | 計画中 | Agent Evaluation Platform (harness / MCP mock / sandbox) との統合評価 |

凍結済みの既存問題群・既存スキーマ・既存 Judge は v1.1-pre でも **変更していない**。v1.1 は追加・拡張のみで構成される。

---

## 3. v1.1-pre 追加内容

### 3.1 問題追加 (90 → 140 問)

| Layer | カテゴリ | 追加 |
|---|---|---:|
| 1 | Maintenance & Engineering | +10 |
| 2 | Risk Tradeoff | +10 |
| 2 | Data Integrity | +10 |
| 3 | Agent Safety | +5 |
| 3 | Structured Decision | +5 |
| 3 | Tool Trajectory | +5 |
| 3 | Human-in-the-Loop Boundary | +5 |

### 3.2 スキーマ拡張 (後方互換)

任意フィールドとして以下を追加。既存問題群は当該フィールドを持たず、Judge v2 は欠如時に後方互換的に動作する。

- `schema_version`
- `score_cap_rules`
- `numeric_checks`
- `generic_answer_penalty`
- `structured_output_requirements`
- `disallowed_answers`

詳細は [`docs/benchmark_spec.md`](docs/benchmark_spec.md) を参照。

### 3.3 Judge v2

[`judge_template_v2.md`](judge_template_v2.md) を新規追加。

- 採点優先順位を明示 (`critical_failures` → `disallowed_answers` → `must_have` → `score_cap_rules` → `numeric_checks` → `structured_output_requirements` → `generic_answer_penalty` → `nice_to_have` → `reasoning_quality`)
- `score_cap_rules` / `numeric_checks` / `generic_answer_penalty` / `structured_output_requirements` を機械的に適用
- Evidence requirement (加点根拠を回答本文から引用または要約)
- 出力 JSON に `applicable_score_caps` / `must_have_results` / `numeric_check_results` 等を含む

採点フローの詳細は [`docs/evaluation_methodology.md`](docs/evaluation_methodology.md) を参照。

### 3.4 evaluation_set_v2

[`evaluation_set_v2.yaml`](evaluation_set_v2.yaml) を新規追加 (30 問、Knowledge / Reasoning / Agent 各 10 問)。

v1.1 で追加されたカテゴリを重点的に含め、Judge v2 の識別力検証用に設計されている。

### 3.5 Anonymized Evaluation Results

中立 ID (`model_a`〜`model_d`) による 4 モデル × 30 問 = 120 件の Judge v2 全件採点を実施した。

| model_id | avg_final_score |
|---|---:|
| model_a | 3.93 |
| model_b | 3.93 |
| model_c | 3.33 |
| model_d | 1.27 |

- スコアは 1〜5 点に分布 (旧評価で見られた 4〜5 集中を改善)
- 最高平均と最低平均の差は **2.67 点**
- `score_cap_rules` / `numeric_checks` / `generic_answer_penalty` / `critical_failures` が実際に発動

公開可能な詳細は [`docs/public_evaluation_summary.md`](docs/public_evaluation_summary.md) を参照。

---

## 4. データセット統計 (v1.1-pre)

| 項目 | 値 |
|---|---:|
| 総問題数 | 140 |
| Layer 1 (Industrial Knowledge) | 50 |
| Layer 2 (Industrial Reasoning) | 50 |
| Layer 3 (Industrial Agent) | 40 |

最新のドメイン分布・難易度分布は `benchmark_data/index.yaml` を参照。

---

## 5. クイックスタート

### 必要環境

- Python 3.10 以上
- PyYAML (`pip install pyyaml`)

### バリデーション

```bash
python scripts/validate_dataset.py
```

期待出力:

```
Checked: 140 problem files
Errors:  0
Warnings:0
```

### Judge v2 入力の準備 (中立 ID を使用)

```bash
python scripts/prepare_judge_inputs_v2.py model_a
```

### 個別問題の参照

```bash
cat benchmark_data/knowledge/order/IK-ORDER-001.yaml
cat benchmark_data/agent/hil_boundary/IA-HILB-001.yaml
```

---

## 6. ディレクトリ構成

```
industrial-agent-benchmark/
├── README.md
├── docs/                                    # 設計・評価・リリース関連ドキュメント
├── benchmark_data/
│   ├── index.yaml / index.csv               # 全問題インデックス
│   ├── knowledge/                           # Layer 1
│   │   ├── order/                           (5)  既存
│   │   ├── production_planning/             (5)  既存
│   │   ├── procurement/                     (5)  既存
│   │   ├── manufacturing_preparation/       (5)  既存
│   │   ├── manufacturing_execution/         (5)  既存
│   │   ├── quality/                         (5)  既存
│   │   ├── shipping/                        (5)  既存
│   │   ├── improvement/                     (5)  既存
│   │   └── maintenance_engineering/         (10) v1.1 追加
│   ├── reasoning/                           # Layer 2
│   │   ├── fta/                             (5)  既存
│   │   ├── 5why/                            (5)  既存
│   │   ├── fmea/                            (5)  既存
│   │   ├── capa/                            (5)  既存
│   │   ├── quality_improvement/             (5)  既存
│   │   ├── abnormality_analysis/            (5)  既存
│   │   ├── risk_tradeoff/                   (10) v1.1 追加
│   │   └── data_integrity/                  (10) v1.1 追加
│   └── agent/                               # Layer 3
│       ├── workflow_design/                 (4)  既存
│       ├── agent_design/                    (4)  既存
│       ├── mcp/                             (3)  既存
│       ├── tool_selection/                  (3)  既存
│       ├── human_in_the_loop/               (3)  既存
│       ├── multi_agent_coordination/        (3)  既存
│       ├── agent_safety/                    (5)  v1.1 追加
│       ├── structured_decision/             (5)  v1.1 追加
│       ├── tool_trajectory/                 (5)  v1.1 追加
│       └── hil_boundary/                    (5)  v1.1 追加
│
├── evaluation_set_v1.yaml                   # 旧評価サブセット (凍結)
├── evaluation_set_v2.yaml                   # v1.1 評価サブセット (新規)
├── judge_template_v2.md                     # v1.1 Judge (新規)
└── scripts/
    ├── generate_dataset.py
    ├── validate_dataset.py                  # v1.1 拡張に対応
    └── prepare_judge_inputs_v2.py           # v1.1 追加
```

---

## 7. ドキュメント

### リリース・公開関連 (v1.1-pre)

| 種類 | パス |
|---|---|
| リリースノート | [`docs/v1.1_release_notes.md`](docs/v1.1_release_notes.md) |
| 公開版識別力サマリ | [`docs/public_evaluation_summary.md`](docs/public_evaluation_summary.md) |
| ベンチマークカード | [`docs/benchmark_card.md`](docs/benchmark_card.md) |

### 仕様・評価方法

| 種類 | パス |
|---|---|
| スキーマ仕様 (v1.1 後方互換拡張を含む) | [`docs/benchmark_spec.md`](docs/benchmark_spec.md) |
| 評価方法 (Judge v1 + v1.1 採点フロー追記) | [`docs/evaluation_methodology.md`](docs/evaluation_methodology.md) |
| 難易度定義 | [`docs/difficulty_definition.md`](docs/difficulty_definition.md) |

### v1.1 設計パッケージ

| 種類 | パス |
|---|---|
| 設計パッケージ索引 | [`docs/v1.1_README.md`](docs/v1.1_README.md) |
| 設計計画 | [`docs/v1.1_design_plan.md`](docs/v1.1_design_plan.md) |
| Rubric 設計 | [`docs/v1.1_rubric_design.md`](docs/v1.1_rubric_design.md) |
| カテゴリ設計 | [`docs/v1.1_category_plan.md`](docs/v1.1_category_plan.md) |
| 問題タイトル一覧 | [`docs/v1.1_question_titles.md`](docs/v1.1_question_titles.md) |

---

## 8. 非公開・非含有

以下は本リリースに **含めない**:

- `results_v2/` (Judge v2 採点結果、raw answers、judge inputs、judgements、leaderboard)
- `results/` (旧評価時点の非公開評価成果物)
- 内部の非公開メモ
- モデル ID 対応表
- 提供元名・製品名・運用名
- API キー、シークレット、認証情報

これらは `.gitignore` または運用ルールにより公開リポジトリへ含めない。

---

## 9. スキーマ概要

各問題は以下の構造を持つ (基本必須フィールド + v1.1 任意拡張)。

```yaml
id: IK-MAINT-001
schema_version: "1.1"
layer: industrial_knowledge
category: maintenance_engineering
domain: general_manufacturing
subdomain: maintenance
difficulty: 3
estimated_time_min: 30

title: ...
scenario: ...
question: ...

expected_skills: [...]
primary_skill: cost_benefit_analysis
secondary_skills: [...]

reference_answer: ...

evaluation_rubric:
  must_have:         [...]
  nice_to_have:      [...]
  critical_failures: [...]

# v1.1 後方互換拡張 (任意)
score_cap_rules: [...]
numeric_checks: [...]
generic_answer_penalty: { enabled: true, conditions: [...] }
structured_output_requirements: { required: true, format: json, required_fields: [...] }
disallowed_answers: [...]
```

詳細は [`docs/benchmark_spec.md`](docs/benchmark_spec.md) を参照。

---

## 10. 評価方法 (要約)

| 評価軸 | 概要 |
|---|---|
| `critical_failure_triggered` | 致命的誤りがあれば即 `final_score = 1` |
| `disallowed_answers` | 明示的禁止回答への該当判定 |
| `must_have` | 必須要件充足率 (欠落数で `max_score` を制御) |
| `score_cap_rules` | シナリオ固有制約の欠落で `max_score` を制御 |
| `numeric_checks` | 必須数値の `expected_value` / `tolerance` / `unit` を検証 |
| `structured_output_requirements` | 必須フィールドと形式を検証 |
| `generic_answer_penalty` | 一般論回答を減点 |
| `nice_to_have` | 発展要件 (加点) |
| `reasoning_quality` | 推論の論理性・製造業実務妥当性 |

Judge v2 の詳細は [`judge_template_v2.md`](judge_template_v2.md) と [`docs/evaluation_methodology.md`](docs/evaluation_methodology.md) を参照。

---

## 11. ライセンス・引用

本プロジェクトは Apache License 2.0 の下で公開する。

利用時は、本リポジトリ名、バージョン (例: `v1.1.0-pre`)、利用した問題 ID または範囲を明記することを推奨する。

---

## 12. バージョン履歴

- **v1.0 (2026-06)** — 初版凍結。90 問・スキーマ・評価方法を完成。
- **v1.1.0-pre (2026-06)** — 140 問へ拡張。Judge v2、`evaluation_set_v2`、識別力検証結果を追加。既存資産は未変更。
