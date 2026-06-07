# Industrial Agent Benchmark v1.0 — Benchmark Specification

本ドキュメントは Industrial Agent Benchmark v1.0 における問題データの **正式スキーマ** を定義する。
本仕様は v1.0 として凍結され、以降のスキーマ変更はマイナー / メジャーバージョンとして管理する。

---

## 1. データ形式

- 1問 = 1 YAML ファイル
- 文字コード: UTF-8 (BOM 無し)
- 改行コード: LF
- ファイル名: `{id}.yaml` （例: `IK-ORDER-001.yaml`）
- 配置先: `benchmark_data/{layer}/{category}/{id}.yaml`

---

## 2. 正式スキーマ

```yaml
id: string                      # 問題ID。グローバル一意。例: IK-ORDER-001
layer: enum                     # industrial_knowledge | industrial_reasoning | industrial_agent
category: string                # レイヤ内カテゴリ。ディレクトリ名と一致
domain: enum                    # 産業ドメイン (下記参照)
subdomain: enum                 # サブドメイン (下記参照)
difficulty: integer             # 1〜5 (difficulty_definition.md 参照)
estimated_time_min: integer     # 専門家が解く場合の推定所要時間(分)

title: string                   # 問題タイトル (1行)
scenario: string                # 実務シナリオ (条件・制約・数値を含む)
question: string                # エージェントへの問い

expected_skills: list[string]   # 評価対象スキル一式 (標準スキル語彙より)
primary_skill: string           # 主要評価スキル (expected_skills の中から1つ)
secondary_skills: list[string]  # 補助評価スキル (expected_skills のうち主要以外)

reference_answer: string        # 模範解答 / 推奨思考プロセス

evaluation_rubric:
  must_have: list[string]       # 必須要件。欠落時は final_score <= 2 に制限
  nice_to_have: list[string]    # 発展要件。加点要素
  critical_failures: list[string] # 致命的エラー条件。該当時は final_score = 1

reasoning_trace_required: bool  # trueの場合、エージェントは推論過程の明示が必須
```

---

## 3. enum 定義

### 3.1 layer

| value | 説明 |
|---|---|
| industrial_knowledge | Layer 1: 実務知識・状況判断 |
| industrial_reasoning | Layer 2: 推論手法 (FTA/5Why/FMEA/CAPA等) |
| industrial_agent | Layer 3: エージェント設計能力 |

### 3.2 category

Layer 1 (industrial_knowledge):
`order` / `production_planning` / `procurement` / `manufacturing_preparation` /
`manufacturing_execution` / `quality` / `shipping` / `improvement` /
`maintenance_engineering`

Layer 2 (industrial_reasoning):
`fta` / `5why` / `fmea` / `capa` / `quality_improvement` / `abnormality_analysis` / `risk_tradeoff` / `data_integrity`

Layer 3 (industrial_agent):
`workflow_design` / `agent_design` / `mcp` / `tool_selection` /
`human_in_the_loop` / `multi_agent_coordination` / `agent_safety` / `structured_decision` / `tool_trajectory` / `hil_boundary`

### 3.3 domain

| value | 説明 |
|---|---|
| automotive | 自動車・自動車部品 |
| electronics | 電子機器・電子部品 |
| medical_device | 医療機器 |
| heavy_machinery | 産業機械・建機 |
| general_manufacturing | 業種非依存の一般製造 |

### 3.4 subdomain

| value | 説明 |
|---|---|
| assembly | 組立 |
| smt | 表面実装 |
| molding | 樹脂成形 |
| machining | 切削加工 |
| welding | 溶接 |
| coating | 塗装 |
| inspection | 検査 |
| logistics | 物流・梱包・出荷 |
| procurement | 調達・購買 |
| production_control | 生産管理・計画 |
| quality_assurance | 品質保証 |
| maintenance | 保全 (v1.0 では限定使用) |
| supply_chain_management | サプライチェーン |
| process_engineering | 工程設計 |

---

## 4. 標準スキル語彙 (primary_skill / secondary_skills)

```
requirement_analysis, normalization, capacity_planning, production_planning,
procurement_planning, inventory_planning, supplier_quality_management,
change_control, process_validation, measurement_system_analysis,
work_standardization, shopfloor_control, traceability_analysis,
containment_planning, shipment_control, statistical_quality_control,
process_capability_analysis, root_cause_analysis, fta_structuring,
five_why_analysis, fmea_analysis, capa_planning, quality_improvement,
abnormality_analysis, human_factors, cost_benefit_analysis,
logistics_planning, product_lifecycle_management, launch_readiness,
workflow_design, agent_design, tool_selection, mcp_design,
data_integration, human_in_the_loop, multi_agent_coordination,
evidence_management, guardrail_design, simulation_reasoning,
risk_assessment, structured_output_design, knowledge_extraction,
sustainability_reporting, compliance_management
```

新規スキルを追加する場合は本リストへの登録を必須とする。

---

## 5. id 命名規則

`{LAYER_PREFIX}-{CATEGORY_PREFIX}-{SEQ:03d}`

| Layer | Prefix |
|---|---|
| industrial_knowledge | IK |
| industrial_reasoning | IR |
| industrial_agent | IA |

カテゴリ Prefix:

| Category | Prefix |
|---|---|
| order | ORDER |
| production_planning | PP |
| procurement | PROC |
| manufacturing_preparation | MPREP |
| manufacturing_execution | MEXEC |
| quality | QUAL |
| shipping | SHIP |
| improvement | IMPR |
| maintenance_engineering | MAINT |
| fta | FTA |
| 5why | 5WHY |
| fmea | FMEA |
| capa | CAPA |
| quality_improvement | QI |
| abnormality_analysis | AA |
| risk_tradeoff | RT |
| data_integrity | DI |
| workflow_design | WD |
| agent_design | AD |
| mcp | MCP |
| tool_selection | TS |
| human_in_the_loop | HIL |
| multi_agent_coordination | MAC |
| agent_safety | AS |
| structured_decision | SD |
| tool_trajectory | TT |
| hil_boundary | HILB |

---

## 6. reasoning_trace_required

- `true`: エージェントは最終結論に加え、明示的な推論過程（仮説、根拠、トレードオフ、結論）を出力すること。
- `false`: 推論過程の明示は任意。最終結論の妥当性で評価する。

Layer 2 / Layer 3 は原則として `true`。
Layer 1 は問題ごとに難易度に応じて設定する (難易度 3 以上は原則 `true`)。

---

## 7. バリデーション

`scripts/validate_dataset.py` により以下を機械的に検証する:

- 必須フィールド欠落の検出
- id のグローバル一意性
- difficulty が 1〜5 整数
- evaluation_rubric.must_have / nice_to_have / critical_failures の存在
- file_path と id の整合
- enum 値の妥当性
- expected_skills と primary_skill / secondary_skills の整合

---

## 8. バージョニング

本仕様は **v1.0** として凍結する。
v1.1 以降での予定:

- 新カテゴリ追加 (Maintenance / Compliance / Robotics)
- 問題数 2,500 規模への拡張
- assets フィールド導入 (図面/ログ/CSV添付)
- allowed_tools フィールド導入 (Agent Harness 連携用)


---

## 9. v1.1 拡張スキーマ (Additive, Backward Compatible)

v1.1 では、上位モデル間の識別力を高めるために以下フィールドを **追加** する。
すべて **任意 (optional)** であり、未指定の問題は v1.0 互換として扱われる。
ファイル先頭に `schema_version: "1.1"` を持つ問題のみ、これら追加フィールドの
構造検証 (存在時) の対象となる。`schema_version` 未指定 / `"1.0"` の問題は
v1.0 検証規則のみ適用される。

### 9.1 追加フィールド一覧

```yaml
schema_version: string        # 任意。"1.1" を指定すると v1.1 拡張が有効化される

score_cap_rules:              # 任意。発火時に final_score を max_score に制限する
  - condition: string         # 必須。Judge が判定可能な自然言語条件
    max_score: integer        # 必須。1〜5
    reason: string            # 任意。発火理由 (Judge / レビュー向けの説明)

numeric_checks:               # 任意。機械的に検査可能な数値要件のリスト
  - name: string              # 必須。何の数値か (例: "必要追加設備台数")
    expected_value: scalar    # 必須。number / "[min, max]" レンジ文字列 / 関数式文字列
    tolerance: string         # 必須。"±5%", "±0.1", "exact", "<=", ">=" 等
    unit: string              # 必須。例: "台", "%", "JPY/個"
    required: bool            # 任意 (既定 false)。true の場合、失敗は critical_failure 昇格

generic_answer_penalty:       # 任意。汎用論回答を減点する
  enabled: bool               # 必須
  conditions: list[string]    # 必須。下記の標準条件名から選ぶ
    # 標準条件:
    # - scenario_specific_numbers_not_used
    # - no_priority_order
    # - no_tradeoff_analysis
    # - generic_framework_only
    # - no_named_stakeholder

structured_output_requirements:  # 任意。構造化出力の必須要件
  required: bool                 # 必須
  format: enum                   # 必須。json | yaml | markdown_table | none
  required_fields: list[string]  # 必須。必須キー名のリスト

disallowed_answers:           # 任意。禁則回答パターン
  - string                    # 自然言語の禁則条件。Judge が一致を検出すると critical_failure 相当
```

### 9.2 後方互換ルール

- v1.0 問題 (90 問) は `schema_version` を **明示しない**。validator はこれらを
  v1.0 規則のみで検証する。
- v1.1 問題は `schema_version: "1.1"` を必須とする。これにより validator は
  Section 9 のフィールドが存在する場合の構造検証を有効化する。
- 採点パイプラインは `schema_version` を読み取り、v1.1 ロジック
  (`evaluation_methodology.md` v1.1 章参照) を適用するか判断する。
- 既存 v1.0 採点ロジックは変更しない。

### 9.3 numeric_checks 詳細

- `expected_value`:
  - 数値 (`int` / `float`)
  - レンジを表す文字列 `"[a, b]"` (両端含む)
  - 評価時に Judge が計算可能な式文字列 (例: `"ceil(12000*38/27000)"`)
- `tolerance`:
  - 相対許容 `"±5%"`
  - 絶対許容 `"±0.1"`
  - 厳密一致 `"exact"`
  - 比較演算 `"<="`, `">="`, `"<"`, `">"`
- `required: true` のチェックが 1 つでも失敗した場合、final_score = 1 (critical_failure 同等)。

### 9.4 structured_output_requirements 詳細

- `format`:
  - `json`: 厳密に有効な JSON で出力
  - `yaml`: 厳密に有効な YAML で出力
  - `markdown_table`: Markdown テーブル形式
  - `none`: 形式不問 (将来拡張用)
- `required_fields` に列挙されたキーは全て出現必須。
- 標準推奨キーセット: `decision`, `rationale`, `risks`, `required_approvals`, `next_actions`
  (問題ごとに増減可)。

### 9.5 generic_answer_penalty 詳細

- `conditions` のいずれか 1 つ以上が Judge により発火と判定された場合、
  最終スコアから減点する (既定 -1, 下限 1)。詳細は `evaluation_methodology.md` v1.1 章を参照。

### 9.6 disallowed_answers 詳細

- 各エントリは自然言語の禁則条件文字列。
- Judge が回答中に該当パターンを検出した場合、`critical_failures` と同等扱いで
  final_score = 1 とする (`evaluation_methodology.md` v1.1 章 採点優先順位 §2 参照)。

### 9.7 適用範囲 (v1.1 リリース時点)

- v1.1 で新規追加する 90 問のみが本拡張を使用する。
- 既存 v1.0 90 問は本拡張の対象外であり、`schema_version` フィールドを持たない。
- カテゴリ別の活用方針は `docs/v1.1_category_plan.md` および
  `docs/v1.1_rubric_design.md` を参照。

### 9.8 enum / 標準スキル語彙の v1.1 追加 (検討中)

P2 以降で新規 90 問の生成に伴い、必要なカテゴリ・prefix・subdomain・primary_skill を段階的に正式追記する。
P2 第1バッチでは `maintenance_engineering` カテゴリと `MAINT` prefix を Section 3.2 / Section 5 に正式追記した。
P2 第2バッチでは `agent_safety` カテゴリと `AS` prefix を Section 3.2 / Section 5 に正式追記した。
P2 第3バッチでは `tool_trajectory` カテゴリと `TT` prefix を Section 3.2 / Section 5 に正式追記した。
P2 第4バッチでは `hil_boundary` カテゴリと `HILB` prefix を Section 3.2 / Section 5 に正式追記した。
P2 第5バッチでは `structured_decision` カテゴリと `SD` prefix を Section 3.2 / Section 5 に正式追記した。
P2 第6バッチでは `risk_tradeoff` カテゴリと `RT` prefix を Section 3.2 / Section 5 に正式追記した。
P2 第7バッチでは `data_integrity` カテゴリと `DI` prefix を Section 3.2 / Section 5 に正式追記した。

- 追加 subdomain 候補: `maintenance_engineering`, `change_control`, `compliance`,
  `factory_management`, `data_governance`, `agent_safety`, `tool_orchestration`
- 追加 primary_skill 候補: `predictive_maintenance`, `reliability_engineering`,
  `change_management`, `regulatory_compliance`, `factory_economics`,
  `numeric_reasoning`, `tradeoff_analysis`, `data_integrity_assessment`,
  `agent_safety_engineering`, `tool_trajectory_design`, `hil_boundary_design`,
  `audit_log_design`, `fallback_design`

---

## 10. バージョニング (v1.1 更新)

- 本仕様は **v1.0** で凍結された Section 1〜8 を維持しつつ、
  Section 9 を **v1.1 拡張 (additive)** として追記したものである。
- v1.0 互換性: `schema_version` 未指定 / `"1.0"` の問題は Section 1〜8 のみで検証される。
- v1.1 識別: `schema_version: "1.1"` の問題は Section 1〜8 に加え、
  Section 9 で定義された任意フィールドの構造検証を受ける。
- 破壊的変更は v2.0 で別途扱う。
