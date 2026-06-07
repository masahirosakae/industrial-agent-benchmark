# Industrial Agent Benchmark v1.1-pre Public Evaluation Summary

本書は、Industrial Agent Benchmark v1.1-pre の **公開可能な範囲のみ** をまとめた識別力サマリである。  
モデル ID 対応表、提供元名、製品名、運用名、非公開メモは含まない。

---

## 1. 検証目的

Industrial Agent Benchmark v1.0 では「上位モデル間でスコアが 4〜5 点に集中し、モデル差が出にくい」ことが課題だった。  
v1.1 では、シナリオ固有数値、`score_cap_rules`、`numeric_checks`、`generic_answer_penalty`、強化された `critical_failures`、Agent 層の権限境界評価 (HIL Boundary / Tool Trajectory / Agent Safety / Structured Decision) を導入し、識別力を改善できたかを検証した。

評価には次を用いた。

- 評価サブセット: `evaluation_set_v2.yaml` (30 問)
- Judge: `judge_template_v2.md`
- 対象: 匿名化モデル 4 つ (`model_a` / `model_b` / `model_c` / `model_d`)
- 採点件数: 4 モデル × 30 問 = 120 件

---

## 2. v1.1 評価設計の主な改善

- シナリオ固有の数値条件と明示的な計算チェックを追加
- `score_cap_rules` により、重要要件欠落時の最終スコア上限を機械的に制御
- `numeric_checks` により、必要な数値を回答本文で使っているかを検証
- `generic_answer_penalty` により、一般論・チェックリスト型回答を減点
- `structured_output_requirements` により、実運用に近い構造化出力を要求
- `disallowed_answers` により、明示的に禁止すべき回答パターンを定義
- 強化された `critical_failures` により、安全・品質・規制・承認境界違反を最低スコアへ制限
- Agent 層で HIL、tool sequence、approval gate、audit log、rollback、fallback、権限境界を評価
- Judge v2 に **evidence requirement** を導入し、加点根拠を回答本文からの引用または要約に限定

---

## 3. Anonymized Model Evaluation Results

中立 ID のみを用いた集計結果である。

| model_id | avg_final_score | score_cap 発動率 | numeric_check 失敗率平均 | generic_penalty 発動率 | critical_failure 件数 |
|---|---:|---:|---:|---:|---:|
| model_a | 3.93 | 46.7% | 0.115 | 0.0% | 0 |
| model_b | 3.93 | 46.7% | 0.115 | 0.0% | 0 |
| model_c | 3.33 | 66.7% | 0.171 | 10.0% | 0 |
| model_d | 1.27 | 100.0% | 0.933 | 93.3% | 6 |

最高平均と最低平均の差は **2.67 点**。v1.0 の高得点集中傾向は再現していない。

---

## 4. スコア分布

| final_score | 件数 | 比率 |
|---:|---:|---:|
| 1 | 22 | 18.3% |
| 2 | 29 | 24.2% |
| 3 | 24 | 20.0% |
| 4 | 3 | 2.5% |
| 5 | 42 | 35.0% |

スコアは 1〜5 の全範囲に分布した。

---

## 5. Layer 別平均

| layer | avg_final_score |
|---|---:|
| industrial_knowledge | 3.53 |
| industrial_reasoning | 3.20 |
| industrial_agent | 2.63 |

Agent 層が最も難しく、差分検出に有効だった。

---

## 6. Category 別平均と識別力観点

| category | avg_final_score | 識別力に関する観点 |
|---|---:|---|
| hil_boundary | 2.00 | 承認者の曖昧さ、SLA 不足、権限境界の不明確さを強く検出 |
| agent_safety | 2.63 | 危険な自動化、不適切な権限委譲、安全/品質境界違反を検出 |
| tool_trajectory | 2.63 | 危険な tool 順序、approval gate 不足、rollback/fallback 不足を検出 |
| data_integrity | 2.70 | 欠損・矛盾・データ鮮度不足下での Safe Deferral を評価 |
| structured_decision | 3.25 | KPI 衝突下の構造化最終判断を評価 |
| maintenance_engineering | 3.34 | 数値計算と段階導入・品質確認制約を統合した判断を評価 |
| risk_tradeoff | 3.70 | 品質・納期・コスト・安全のトレードオフ意思決定を評価 |
| order | 4.25 | v1.0 既存カテゴリ。後方互換採点を確認 |
| shipping | 4.25 | v1.0 既存カテゴリ。後方互換採点を確認 |

---

## 7. v1.1 評価機能の発動状況

| metric | value |
|---|---:|
| score_cap 発動率 | 65.0% |
| numeric_check 失敗率平均 | 0.333 |
| generic_penalty 発動率 | 25.8% |
| critical_failure 発動件数 | 6 |

これらは v1.1 で追加された評価機能が、スキーマ上の追加にとどまらず、実際の採点へ寄与したことを示す。

---

## 8. Benchmark Design としての示唆

1. **シナリオ固有数値を使わせる**  
   定量条件は、モデルが問題文を読み計算・比較しているかを区別する強力な指標である。

2. **重大欠落には score cap を適用する**  
   流暢な回答でも、承認、監査、品質、安全、規制要件を欠く場合は高得点にしない設計が有効だった。

3. **矛盾データと判断保留を含める**  
   製造業 Agent には、不完全なデータ下で無理に断定せず hold / recheck / escalate できる能力が必要である。

4. **Agent の権限境界を評価する**  
   HIL、approval gate、audit log、rollback、fallback は、産業用 Agent 評価の中核要素である。

5. **自然な文章と運用可能な判断を分ける**  
   v1.1 は、もっともらしい一般論ではなく、実行可能・監査可能・制約遵守された回答を高く評価する。

---

## 9. 結論

Industrial Agent Benchmark v1.1-pre は、v1.0 よりもモデル差を検出できる評価設計となっている。

- スコアが 1〜5 点に分布した
- 匿名化モデル間で **2.67 点** の平均差が出た
- score_cap / numeric_check / generic_penalty / critical_failure が実際に機能した
- Agent 層、とくに HIL Boundary / Tool Trajectory / Agent Safety が差分検出に効いた

公開対象には特定モデル名、提供元名、運用名、モデル ID 対応表、API キー、非公開メモ、raw answers、judge inputs、judgements を一切含めていない。
