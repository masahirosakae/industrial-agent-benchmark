# Industrial Agent Benchmark v1.0

> Manufacturing 版 Humanity's Last Exam を目指す、製造業エージェント評価ベンチマーク

本リポジトリは、製造業ドメインにおけるAIエージェントの能力を、
**専門知識 / 推論 / 問題解決 / Agent設計** の4観点から総合評価するための
ベンチマークデータセットおよび評価方法を提供する。

---

## 1. 目的

単純な定義・暗記問題ではなく、以下の能力を評価する:

1. **製造業専門知識** — 受注、生産計画、調達、品質、出荷など実務知識の状況判断
2. **製造業推論能力** — FTA / 5Why / FMEA / CAPA などフレームワーク適用と因果推論
3. **製造業問題解決能力** — トレードオフを含む実環境での意思決定
4. **Industrial Agent能力** — ワークフロー設計、MCP連携、Human-in-the-loop、マルチエージェント協調

---

## 2. 3 Layer アーキテクチャ

| Layer | 名称 | 問題数 | カテゴリ |
|---|---|---|---|
| Layer 1 | Industrial Knowledge | 40 | Order / Production Planning / Procurement / Manufacturing Preparation / Manufacturing Execution / Quality / Shipping / Improvement (各5問) |
| Layer 2 | Industrial Reasoning | 30 | FTA / 5Why / FMEA / CAPA / Quality Improvement / Abnormality Analysis (各5問) |
| Layer 3 | Industrial Agent | 20 | Workflow Design / Agent Design / MCP / Tool Selection / Human in the Loop / Multi-Agent Coordination |
| **合計** | | **90** | |

---

## 3. v1.0 スコープ

本リリースで **凍結** される項目:

- 90問のシナリオ・問題本文・模範解答
- v1.0 正式スキーマ (`docs/benchmark_spec.md`)
- 難易度1〜5の定義 (`docs/difficulty_definition.md`)
- LLM-as-a-Judge 評価方法 (`docs/evaluation_methodology.md`)

v1.0 では、Benchmark Dataset と Evaluation Methodology の完成度を最優先する。

---

## 4. データセット統計 (v1.0)

### 難易度分布
| Difficulty | 件数 |
|---|---|
| 3 (Mid-level) | 34 |
| 4 (Senior Expert) | 44 |
| 5 (Factory Director) | 12 |

### ドメイン分布
| Domain | 件数 |
|---|---|
| general_manufacturing | 52 |
| electronics | 19 |
| automotive | 15 |
| medical_device | 2 |
| heavy_machinery | 2 |

### 想定総解答時間
合計 約 **3,690 分 (61.5 時間)** ＝ 専門家1名による全問解答工数。

---

## 5. 将来計画

### v1.1 以降で追加予定
新たに以下カテゴリを追加し、最終的に **2,500問規模** を目指す:

- **Maintenance** — 予知保全、CBM、MTBF/MTTR、保全計画
- **Compliance** — ISO/IATF、RoHS/REACH、下請法、輸出管理
- **Factory Management** — ROI、投資判断、内製外注、組織設計
- **Robotics & Automation** — Sim2Real、PLC制御、ロボット動作計画

### Agent Evaluation Platform (後続フェーズ)
本リポジトリとは別フェーズで以下を実装予定:

- `agent_harness/` — エージェント実行ランナー
- `mcp_mock_servers/` — 評価用ダミーERP/MES/APSの提供
- `sandbox_env/` — Docker等で隔離された安全実行環境

v1.0 ではこれらは含まない（Dataset と Methodology の完成を優先する方針）。

---

## 6. ディレクトリ構成

```
industrial-agent-benchmark/
├── README.md
├── docs/
│   ├── benchmark_spec.md          # 正式スキーマ定義 (v1.0凍結)
│   ├── difficulty_definition.md   # 難易度1〜5の定義
│   ├── evaluation_methodology.md  # LLM-as-a-Judge 評価方法
│   ├── benchmark_card.md          # ベンチマークカード
│   └── benchmark_release_notes_v1.0.md
│
├── benchmark_data/
│   ├── index.yaml                 # 全問題インデックス (YAML)
│   ├── index.csv                  # 全問題インデックス (CSV)
│   ├── knowledge/                 # Layer 1 (40問)
│   │   ├── order/                 (5)
│   │   ├── production_planning/   (5)
│   │   ├── procurement/           (5)
│   │   ├── manufacturing_preparation/   (5)
│   │   ├── manufacturing_execution/     (5)
│   │   ├── quality/               (5)
│   │   ├── shipping/              (5)
│   │   └── improvement/           (5)
│   ├── reasoning/                 # Layer 2 (30問)
│   │   ├── fta/                   (5)
│   │   ├── 5why/                  (5)
│   │   ├── fmea/                  (5)
│   │   ├── capa/                  (5)
│   │   ├── quality_improvement/   (5)
│   │   └── abnormality_analysis/  (5)
│   └── agent/                     # Layer 3 (20問)
│       ├── workflow_design/       (4)
│       ├── agent_design/          (4)
│       ├── mcp/                   (3)
│       ├── tool_selection/        (3)
│       ├── human_in_the_loop/     (3)
│       └── multi_agent_coordination/    (3)
│
└── scripts/
    ├── generate_dataset.py        # 90問データから個別YAMLを生成
    └── validate_dataset.py        # データセット整合性検証
```

---

## 7. クイックスタート

### 必要環境
- Python 3.10 以上
- PyYAML (`pip install pyyaml`)

### データセット再生成
```bash
python scripts/generate_dataset.py
```

### バリデーション
```bash
python scripts/validate_dataset.py
```

成功時の出力例:
```
Checked: 90 problem files
Errors:  0
Warnings:0
```

### 個別問題の参照
```bash
cat benchmark_data/knowledge/order/IK-ORDER-001.yaml
```

---

## 8. スキーマ概要

各問題は以下の構造を持つ:

```yaml
id: IK-ORDER-001
layer: industrial_knowledge       # 3 layers
category: order                   # 20 categories
domain: automotive                # 5 domains
subdomain: molding                # 14 subdomains
difficulty: 3                     # 1..5
estimated_time_min: 30

title: ...
scenario: ...                     # 実務シナリオ
question: ...                     # 問い

expected_skills: [...]
primary_skill: requirement_analysis
secondary_skills: [...]

reference_answer: ...

evaluation_rubric:
  must_have:         [...]        # 必須要件（欠落で max final_score=2）
  nice_to_have:      [...]        # 発展要件（加点）
  critical_failures: [...]        # 致命的エラー（該当時 final_score=1）

reasoning_trace_required: true
```

詳細は `docs/benchmark_spec.md` を参照。

---

## 9. 評価方法（要約）

評価者LLMまたは専門家レビューを用いた4要素採点:

| 要素 | 内容 |
|---|---|
| `critical_failure_triggered` | 致命的誤りがあれば即 `final_score = 1` |
| `must_have_ratio` | 必須要件充足率（不足時はスコア上限を制限） |
| `nice_to_have_ratio` | 発展要件充足率 |
| `reasoning_quality` | 推論の論理性・製造業実務妥当性 (1-5) |

詳細プロンプトとスコア決定ルールは `docs/evaluation_methodology.md` 参照。

---

## 10. ライセンス・引用

本プロジェクトは Apache License 2.0 の下で公開される。

利用時は、本リポジトリ名、バージョン、利用した問題IDまたはデータセット範囲を明記することを推奨する。

---

## 11. バージョン履歴

- **v1.0 (2026-06)** — 初版凍結。90問・スキーマ・評価方法を完成。
