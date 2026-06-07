# Industrial Agent Benchmark v1.1 Evaluation v2 Public Summary

## 1. 概要

Industrial Agent Benchmark v1.1 では、`evaluation_set_v2` と Judge v2 を用いて、v1.0よりもモデル差を検出できるかを検証した。

v1.0の初回評価では、スコアが4〜5点に集中し、モデル間差分が出にくいことが課題だった。v1.1では、スコアが **1〜5点の全範囲に分布**し、匿名化モデル間の平均スコア差は **2.67点** となった。

この結果から、v1.1は製造業向けAgent評価において、産業推論、安全境界、tool実行順序、人間承認境界、構造化意思決定品質の違いを、v1.0より明確に検出できることが確認された。

---

## 2. v1.1評価設計の改善

v1.1では、以下の評価要素を強化した。

- シナリオ固有の数値条件と明示的な計算チェックを追加。
- `score_cap_rules` により、重要要件が欠落した回答の高得点化を防止。
- `numeric_checks` により、回答が必要な定量根拠を使っているかを検証。
- `generic_answer_penalty` により、一般論・チェックリスト型回答を減点。
- `critical_failures` により、安全・品質・規制・承認境界違反を低スコア化。
- `structured_output_requirements` により、実運用に近い構造化出力を要求。
- Agent層で HIL、tool trajectory、approval gate、監査ログ、fallback、権限境界を評価。

これにより、v1.0で問題だった「もっともらしい一般論回答でも高得点になる」傾向を抑制した。

---

## 3. Anonymized Model Evaluation

評価では匿名化された中立IDのみを使用した。

- `model_a`
- `model_b`
- `model_c`
- `model_d`

公開版には、特定の提供元名、製品名、非公開の運用名、モデルID対応表は含めない。

| model_id | avg_final_score |
|---|---:|
| model_a | 3.93 |
| model_b | 3.93 |
| model_c | 3.33 |
| model_d | 1.27 |

最高平均と最低平均の差は **2.67点** であり、v1.1の評価セットとJudge v2がモデル差を検出できることを示している。

---

## 4. スコア分布

| final_score | count | ratio |
|---:|---:|---:|
| 1 | 22 | 18.3% |
| 2 | 29 | 24.2% |
| 3 | 24 | 20.0% |
| 4 | 3 | 2.5% |
| 5 | 42 | 35.0% |

v1.0では4〜5点への集中が課題だったが、v1.1では1〜5点に分布した。これにより、高得点・中間点・低得点の違いを分析しやすくなった。

---

## 5. 評価機能の発動状況

| metric | value |
|---|---:|
| score_cap発動率 | 65.0% |
| numeric_check_failed_ratio平均 | 0.333 |
| generic_penalty発動率 | 25.8% |
| critical_failure発動件数 | 6 |

これらの結果から、v1.1で追加した評価機能はスキーマ上の追加に留まらず、実際の採点に影響したことが分かる。

主な効果:

- `score_cap_rules` は、承認者、監査可能性、go/hold条件、シナリオ固有制約が不足する回答の高得点化を防いだ。
- `numeric_checks` は、必要な数値を明示的に使わない回答を検出した。
- `generic_answer_penalty` は、一般的な安全確認やリスク管理の文言だけの回答を低スコア化した。
- `critical_failures` は、安全でない自動実行や不適切な承認判断を検出した。

---

## 6. Layer / Category観点の示唆

| layer | avg_final_score |
|---|---:|
| industrial_knowledge | 3.53 |
| industrial_reasoning | 3.20 |
| industrial_agent | 2.63 |

Agent層が最も難しく、差分検出に有効だった。

| category | avg_final_score | benchmark designとしての示唆 |
|---|---:|---|
| hil_boundary | 2.00 | 承認者の曖昧さ、SLA不足、権限境界の不明確さを検出しやすい。 |
| tool_trajectory | 2.63 | 危険なtool順序、approval gate不足、rollback/fallback不足を検出しやすい。 |
| agent_safety | 2.63 | 危険な自動化、不適切な権限委譲、安全・品質境界違反を検出しやすい。 |

この結果は、Industrial Agent Benchmarkにおいて、単なる知識問題だけでなく、Agentの実行境界・監査性・承認制御を評価することが重要であることを示している。

---

## 7. Benchmark Designとしての示唆

v1.1の結果から、以下の設計方針が有効であると分かった。

1. **シナリオ固有数値を必ず使わせる**  
   数値条件は、モデルが問題文を実際に読み、計算・比較しているかを明確にする。

2. **重大欠落にはscore capを適用する**  
   流暢な回答でも、承認、監査、品質、安全、規制要件を欠く場合は高得点にしない。

3. **矛盾データと判断保留を含める**  
   製造業Agentには、不完全なデータ下で無理に断定せず、hold / recheck / escalate できる能力が必要である。

4. **Agentの権限境界を評価する**  
   HIL、approval gate、audit log、rollback、fallbackは、産業用途Agent評価の中核要素である。

5. **自然な文章と運用可能な判断を分ける**  
   v1.1では、もっともらしい一般論ではなく、実行可能・監査可能・制約遵守された回答を高く評価する。

---

## 8. 結論

Industrial Agent Benchmark v1.1 は、v1.0よりも識別力が高い。

検証では以下を確認した。

- スコアが1〜5点に分布した。
- 匿名化モデル間で **2.67点** の平均差が出た。
- `score_cap_rules`、`numeric_checks`、`generic_answer_penalty`、`critical_failures` が実際に機能した。
- Agent層、とくに HIL Boundary / Tool Trajectory / Agent Safety が差分検出に効いた。

したがって、v1.1は製造業Agentの性能差を検出するベンチマークとして、v1.0より適切な評価設計になっている。
