# evaluation_v2 Results Report

## 1. 概要

P4-2 / P5 として、`evaluation_set_v2.yaml` と `judge_template_v2.md` を用い、4つの匿名化モデル (`model_a`〜`model_d`) × 30問 = 120件の Judge v2 全件採点を実行した。

本検証の目的は、Industrial Agent Benchmark v1.1 が v1.0 で課題だった「スコアが4〜5点に集中し、モデル差が出にくい」状態を改善できたかを確認することである。

v1.1では、以下の評価要素を強化した。

- `score_cap_rules`
- `numeric_checks`
- `generic_answer_penalty`
- `structured_output_requirements`
- `disallowed_answers`
- `critical_failures`
- evidence requirement

採点結果は `results_v2/<model_id>/judgements/` に JSON として保存し、集計用に `results_v2/leaderboard_v2.csv` を作成した。

---

## 2. 品質確認

| 確認項目 | 結果 |
|---|---:|
| judgement JSON件数 | 120 |
| JSON parse | 120/120 PASS |
| leaderboard_v2.csv データ行 | 120 |
| final_score範囲 | 1〜5内 |
| UTF-8 / 文字化け | PASS |
| model_id混同 | なし |
| judge_inputs / raw answers | 未変更 |

---

## 3. model別平均 final_score

| model_id | avg_final_score | score_cap発動率 | numeric_check_failed_ratio平均 | generic_penalty発動率 | critical_failure件数 |
|---|---:|---:|---:|---:|---:|
| model_a | 3.93 | 46.7% | 0.115 | 0.0% | 0 |
| model_b | 3.93 | 46.7% | 0.115 | 0.0% | 0 |
| model_c | 3.33 | 66.7% | 0.171 | 10.0% | 0 |
| model_d | 1.27 | 100.0% | 0.933 | 93.3% | 6 |

最高平均と最低平均の差は **2.67点** であり、v1.0で見られた高得点集中よりも明確な差分が出た。

---

## 4. layer別平均 final_score

| layer | avg_final_score |
|---|---:|
| industrial_knowledge | 3.53 |
| industrial_reasoning | 3.20 |
| industrial_agent | 2.63 |

Agent層が最も難しく、特にHIL Boundary、Tool Trajectory、Agent Safetyが差分検出に効いた。

---

## 5. category別平均 final_score

| category | avg_final_score |
|---|---:|
| agent_safety | 2.63 |
| data_integrity | 2.70 |
| hil_boundary | 2.00 |
| maintenance_engineering | 3.34 |
| order | 4.25 |
| risk_tradeoff | 3.70 |
| shipping | 4.25 |
| structured_decision | 3.25 |
| tool_trajectory | 2.63 |

HIL Boundary は平均 2.00 と最も低く、承認者特定、SLA、承認前禁止操作、監査ログ項目の不足を強く検出した。Tool Trajectory と Agent Safety も平均 2.63 であり、危険なtool順序、approval gate不足、権限境界の曖昧さを検出しやすかった。

---

## 6. difficulty別平均 final_score

| difficulty | avg_final_score |
|---|---:|
| 3 | 3.20 |
| 4 | 3.07 |
| 5 | 3.18 |

Difficultyだけではなく、カテゴリ固有の制約密度、数値要求、HIL/監査要件がスコア差に大きく影響した。

---

## 7. スコア分布

| final_score | count | ratio |
|---:|---:|---:|
| 1 | 22 | 18.3% |
| 2 | 29 | 24.2% |
| 3 | 24 | 20.0% |
| 4 | 3 | 2.5% |
| 5 | 42 | 35.0% |

v1.0ではスコアが4〜5点に集中していたが、v1.1では **1〜5点の全範囲に分布**した。これにより、高得点・中間点・低得点の区別が可能になった。

---

## 8. v1.1評価機能の発動状況

| metric | value |
|---|---:|
| score_cap発動率 | 65.0% |
| numeric_check_failed_ratio平均 | 0.333 |
| generic_penalty発動率 | 25.8% |
| critical_failure発動件数 | 6 |

`score_cap_rules`、`numeric_checks`、`generic_answer_penalty`、`critical_failures` は実際に機能し、以下のような回答を低スコア側へ制限した。

- シナリオ固有数値を使わない回答
- 必須承認者を特定しない回答
- go / hold条件を分けない回答
- QMS / MES / ERP等の矛盾を無視する回答
- HIL境界やapproval gateを曖昧にする回答
- 監査ログやrollback/fallbackを定義しない回答

---

## 9. v1.0との比較

v1.0の初回評価では、回答が一般論として自然であれば4〜5点に寄りやすく、上位モデル間の差が出にくかった。

v1.1では以下の改善により、スコア分布が広がった。

1. **score cap rules** により、重大な欠落がある回答の上限を制御した。
2. **numeric checks** により、数値を明示的に利用しない回答を減点・cap対象にした。
3. **generic answer penalty** により、一般論やチェックリスト型回答を高得点化しにくくした。
4. **critical failures** により、安全・品質・規制・顧客承認に反する回答を最低点側へ制限した。
5. **Agent評価項目** により、HIL、tool sequence、approval gate、監査ログ、fallback、権限境界を評価可能にした。

---

## 10. 識別力判定

**判定: Industrial Agent Benchmark v1.1 は、v1.0よりもモデル差を検出できる。**

根拠:

- v1.0では4〜5点集中が課題だったが、v1.1では1〜5点に分布した。
- model間平均差が **2.67点** 出た。
- score_cap / numeric_check / generic_penalty / critical_failure が実際に発動した。
- Agent層が最も難しく、HIL Boundary / Tool Trajectory / Agent Safety が差分検出に効いた。
- 単なる安全側の一般論では高得点にならず、シナリオ固有の数値・承認者・tool順序・監査要件・条件分岐が必要になった。

---

## 11. 公開・非公開の扱い

公開版では、匿名化モデルID、スコア分布、評価設計上の改善、評価機能の発動状況、benchmark designとしての示唆のみを扱う。

非公開版では、モデルID対応表は記載せず、再評価時の分析観点、改善候補、運用TODOのみを扱う。
