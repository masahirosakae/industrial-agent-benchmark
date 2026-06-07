# evaluation_set_v2 Design — Industrial Agent Benchmark v1.1

本ドキュメントは `evaluation_set_v2.yaml` の30問選定方針と、各問題の選定理由を説明する。v2評価セットは、v1.0で課題となった「上位モデル間のスコア差が出にくい」「generic answer が高得点になる」「numeric reasoning が十分評価されない」問題を検証するため、v1.1追加カテゴリを中心に構成する。

## 1. 選定方針

- 合計30問: Knowledge 10 / Reasoning 10 / Agent 10。
- v1.1追加カテゴリを重点採用: Maintenance & Engineering、Risk Tradeoff、Data Integrity、Agent Safety、Tool Trajectory、HIL Boundary、Structured Decision。
- difficulty 3〜5のみで構成し、分布は difficulty 3=5問、4=18問、5=7問。
- domain は electronics / automotive / general_manufacturing を中心に、heavy_machinery / medical_device も含める。
- v1.1拡張スキーマ (score_cap_rules, numeric_checks, generic_answer_penalty, structured_output_requirements, disallowed_answers) を含む問題を優先。
- v1.0との比較基準として、Knowledgeに `IK-SHIP-005` と `IK-ORDER-004` を含め、Data Integrity / HIL / 品質規制系問題との比較基準にする。

## 2. バランス

### Layer distribution
| Layer | Count |
|---|---:|
| industrial_knowledge | 10 |
| industrial_reasoning | 10 |
| industrial_agent | 10 |

### Difficulty distribution
| Difficulty | Count |
|---|---:|
| 3 | 5 |
| 4 | 18 |
| 5 | 7 |

### Domain distribution
| Domain | Count |
|---|---:|
| automotive | 7 |
| electronics | 9 |
| general_manufacturing | 8 |
| heavy_machinery | 4 |
| medical_device | 2 |

### Category distribution
| Category | Count |
|---|---:|
| agent_safety | 2 |
| data_integrity | 5 |
| hil_boundary | 3 |
| maintenance_engineering | 8 |
| order | 1 |
| risk_tradeoff | 5 |
| shipping | 1 |
| structured_decision | 3 |
| tool_trajectory | 2 |

## 3. 選定問題一覧と理由

| ID | Layer | Category | Domain | Difficulty | Title | 選定理由 |
|---|---|---|---|---:|---|---|
| IK-MAINT-001 | industrial_knowledge | maintenance_engineering | general_manufacturing | 3 | 射出成形機 12 台の CBM 切替 ROI 算定と段階導入計画 | v1.1 Knowledge追加カテゴリの代表。保全判断で数値条件を使えるかを評価し、v1.0の用語説明型回答との差分を見る。 |
| IK-MAINT-002 | industrial_knowledge | maintenance_engineering | electronics | 4 | MTBF 480h / MTTR 6h 設備で Availability 99.5% を満たす冗長台数 | 電子機器領域の保全・品質・停止制約を扱い、genericな予防保全論ではなくscenario-specificな判断を要求する。 |
| IK-MAINT-003 | industrial_knowledge | maintenance_engineering | general_manufacturing | 3 | 潤滑油劣化トレンドからの次回 OH 時期と判断保留条件 | MTBF/MTTRやチョコ停などの定量保全知識を使う基礎〜中難度問題として含める。 |
| IK-MAINT-004 | industrial_knowledge | maintenance_engineering | automotive | 4 | 安全 PLC のテスト周期と SIL レベル整合判定 | 自動車ドメインで設備停止・品質保証・納期制約を統合する知識を評価できる。 |
| IK-MAINT-005 | industrial_knowledge | maintenance_engineering | general_manufacturing | 4 | スペア在庫の臨界部品分類 (ABC) と発注 LT 設計 | 予備品・停止損失・保全計画のトレードオフを含み、数値根拠の有無で差が出る。 |
| IK-MAINT-006 | industrial_knowledge | maintenance_engineering | heavy_machinery | 3 | 突発故障 vs 計画停止の機会損失と部品費の期待値比較 | 重機械設備の異常兆候に対する基本的な保全判断と安全制約を評価する。 |
| IK-MAINT-007 | industrial_knowledge | maintenance_engineering | automotive | 4 | 振動値とトルク値が矛盾する設備の故障モード推定 | 自動車領域で復旧後品質確認と生産再開判断を扱い、安易な再開判断を検出できる。 |
| IK-SHIP-005 | industrial_knowledge | shipping | automotive | 4 | リコール対象ロットの出荷停止範囲 | v1.0からの橋渡し問題。安全部品の記録欠落と出荷停止範囲を扱い、v1.1のData Integrity / HIL評価との比較基準になる。 |
| IK-MAINT-009 | industrial_knowledge | maintenance_engineering | general_manufacturing | 5 | 老朽化ライン更新 vs OH 延命 5 年の NPV / IRR 比較と撤退条件 | 高難度の保全・品質・安全・コスト統合判断で上位モデル差分を検出する。 |
| IK-ORDER-004 | industrial_knowledge | order | medical_device | 3 | 試作要求から量産条件への移管判断 | v1.0からの橋渡し問題。医療機器ドメインの試作から量産移管・品質保証制約を含み、v1.1の規制/品質系問題との比較基準になる. |
| IR-RT-001 | industrial_reasoning | risk_tradeoff | electronics | 4 | 品質 vs 納期: 検査未完了ロットの出荷判断 | 品質 vs 納期の代表問題。tradeoff_matrix、numeric_basis、go/hold条件を検証できる。 |
| IR-RT-003 | industrial_reasoning | risk_tradeoff | heavy_machinery | 4 | 安全 vs 生産継続: 設備異常時の継続運転判断 | 安全 vs 生産継続を扱い、安全停止をコスト理由で否定するモデルを低スコア化できる。 |
| IR-RT-004 | industrial_reasoning | risk_tradeoff | automotive | 5 | 顧客要求 vs 工程能力: Cpk 1.67 要求での短納期量産開始判断 | 顧客要求Cpkと工程能力不足の高難度判断で、顧客承認と数値推論の両方を評価する。 |
| IR-RT-007 | industrial_reasoning | risk_tradeoff | electronics | 4 | 環境規制 vs 生産継続: RoHS/REACH 証明書欠落時の判断 | 環境規制 vs 生産継続を扱い、規制証跡欠落を納期で覆す回答を検出する。 |
| IR-RT-009 | industrial_reasoning | risk_tradeoff | general_manufacturing | 3 | リワーク vs 廃棄: 品質ばらつきと再検査工数を含む判断 | コスト削減案の品質・納期・安全影響を比較する中難度Risk Tradeoff問題。difficulty 3の推論アンカーとして、上位/中位モデルの基本的なKPI比較力を測る。 |
| IR-DI-001 | industrial_reasoning | data_integrity | electronics | 4 | 検査データ欠損: 100ロット中7ロット最終検査未実施での出荷可否判断 | 検査データ欠損と出荷判断の代表問題。欠損を無視した出荷可判断をcriticalに検出する。 |
| IR-DI-002 | industrial_reasoning | data_integrity | general_manufacturing | 4 | MES / QMS / ERP 不整合: 工程完了・未検査・出荷指示済みの矛盾解消 | MES/QMS/ERP不整合を扱い、システム間矛盾へのSafe Deferral能力を評価する。 |
| IR-DI-005 | industrial_reasoning | data_integrity | medical_device | 4 | 単位不一致: 温度 °C/°F と圧力 MPa/kPa 混在時の工程判定 | 単位不一致の検出と変換を要求し、単位変換ミスや単一ソース過信を検出できる。 |
| IR-DI-008 | industrial_reasoning | data_integrity | electronics | 4 | データ鮮度不足: 最新需要予測と48時間前在庫・2週間前工程能力の混在判断 | データ鮮度不足と需給判断を扱い、古い在庫/能力データへの過信を減点できる。 |
| IR-DI-010 | industrial_reasoning | data_integrity | automotive | 5 | 統計判断サンプル不足: n=8 の検査結果で工程安定を断定できるか | n=8のサンプル不足で工程安定を断定する誤りを検出する高難度Safe Deferral問題。 |
| IA-AS-001 | industrial_agent | agent_safety | electronics | 4 | 出荷判定 Agent の欠損データ時自動 OK 防止ガードレール設計 | 欠損データ時の自動OK防止を評価し、危険な自動承認をcritical_failureとして検出できる。 |
| IA-AS-003 | industrial_agent | agent_safety | general_manufacturing | 5 | LLM 信頼度 < 0.85 で HIL に強制エスカレーションする条件設計 | 保全・安全系のAgent判断境界を評価し、HILなしの危険実行を低スコア化する。 |
| IA-TT-001 | industrial_agent | tool_trajectory | electronics | 4 | 品質異常検知 Agent の tool 呼び出し順序設計 | ERP/MES/QMS/SOPをまたぐtool順序とapproval gateを評価し、順序誤りを検出する。 |
| IA-TT-004 | industrial_agent | tool_trajectory | general_manufacturing | 5 | 出荷判定 Agent の tool sequence と部分失敗時の意思決定 | 部分失敗時のtool trajectory、rollback/fallback、停止条件を評価する高難度問題。 |
| IA-HILB-001 | industrial_agent | hil_boundary | electronics | 4 | 検査欠損と納期遅延が同時発生した出荷判定 Agent の HIL 境界設計 | 出荷判定におけるQA/営業/生産管理のHIL境界とSLAを評価できる。 |
| IA-HILB-003 | industrial_agent | hil_boundary | heavy_machinery | 4 | 設備復旧後の品質確認不完全状態における生産再開 HIL 境界設計 | 設備復旧後の品質確認不完全状態で、誰にいつ承認を求めるかを評価する。 |
| IA-HILB-005 | industrial_agent | hil_boundary | automotive | 5 | 市場不具合初報段階における封じ込め・顧客報告・経営エスカレーション HIL 境界設計 | 市場不具合初報時の品質・法務・顧客SQE・経営エスカレーションを評価する高難度問題。 |
| IA-SD-001 | industrial_agent | structured_decision | electronics | 4 | 品質リスク・納期・顧客影響を統合する出荷可否 Structured Decision | 出荷可否判断をdecision/confidence/tradeoff/approvals付きJSONで構造化できるかを評価する。 |
| IA-SD-003 | industrial_agent | structured_decision | heavy_machinery | 4 | 故障リスク・生産影響・安全影響を統合する設備停止 Structured Decision | 設備停止判断で故障・生産・安全KPIを統合したStructured Decisionを評価する。 |
| IA-SD-005 | industrial_agent | structured_decision | automotive | 5 | 不具合率・顧客影響・法規制を統合する市場不具合封じ込め Structured Decision | 市場不具合封じ込め判断で不具合率・顧客影響・法規制を統合する高難度問題。 |

## 4. v1.1識別力を検証できる理由

1. **score cap rules の発火頻度を測れる**: Reasoning/Agentの20問は v1.1拡張スキーマを持ち、must_have欠落・数値未使用・HIL欠落・危険な自動実行で上限スコアが下がる。
2. **numeric_checks の合否を比較できる**: Risk Tradeoff / Data Integrity / Structured Decision / HIL Boundary は数値条件を含むため、計算・単位変換・Cpk差分・ppm・欠損率などでモデル差を検出できる。
3. **generic answer を抑制できる**: `scenario_specific_numbers_not_used` や `no_priority_order` を含む問題を多く含み、一般論の回答は max_score=2〜3 に抑えられる。
4. **Safe Deferral を評価できる**: Data Integrity / HIL Boundary / Agent Safety では、出荷可・自動実行ではなく hold / defer / escalate を選べるかを評価する。
5. **Agent実運用出力を評価できる**: Tool Trajectory と Structured Decision で tool_sequence、approval gate、rollback、JSON structured fields を要求し、実運用に近い差分を測る。
6. **domain汎化を測れる**: electronics / automotive / heavy_machinery / medical_device / general_manufacturing を含め、特定ドメインだけに最適化された回答を防ぐ。
