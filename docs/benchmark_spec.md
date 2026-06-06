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
`manufacturing_execution` / `quality` / `shipping` / `improvement`

Layer 2 (industrial_reasoning):
`fta` / `5why` / `fmea` / `capa` / `quality_improvement` / `abnormality_analysis`

Layer 3 (industrial_agent):
`workflow_design` / `agent_design` / `mcp` / `tool_selection` /
`human_in_the_loop` / `multi_agent_coordination`

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
| fta | FTA |
| 5why | 5WHY |
| fmea | FMEA |
| capa | CAPA |
| quality_improvement | QI |
| abnormality_analysis | AA |
| workflow_design | WD |
| agent_design | AD |
| mcp | MCP |
| tool_selection | TS |
| human_in_the_loop | HIL |
| multi_agent_coordination | MAC |

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
