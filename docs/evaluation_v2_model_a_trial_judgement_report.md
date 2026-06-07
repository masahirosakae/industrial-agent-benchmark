# evaluation_v2 model_a Trial Judgement Report

## 1. 目的

P4-2 として、4モデル全件評価へ進む前に `judge_template_v2.md` が以下を期待どおり適用できるかを確認するため、`model_a` の judge input から6問を選定して試験採点した。

- `score_cap_rules`
- `numeric_checks`
- `generic_answer_penalty`
- evidence requirement
- critical_failure / disallowed_answers の優先適用
- JSON出力のparse可能性

採点は `results_v2/model_a/judge_inputs/` の6件を読み、結果を `results_v2/model_a/trial_judgements/` に JSON として保存した。raw answers と judge_inputs は変更していない。

---

## 2. 対象6問

| Layer | Category | Question ID | Difficulty | Domain | 選定理由 |
|---|---|---:|---:|---|---|
| Knowledge | maintenance_engineering | IK-MAINT-001 | 3 | general_manufacturing | v1.1 Maintenance代表。ROI・回収期間・段階導入・品質確認を含み、numeric_checksの正常通過を確認できる。 |
| Knowledge | order | IK-ORDER-004 | 3 | medical_device | v1.0既存カテゴリ。後方互換的にv1.1拡張フィールドなしでもJudge v2が採点できるか確認する。 |
| Reasoning | risk_tradeoff | IR-RT-001 | 4 | electronics | 品質 vs 納期・費用の代表問題。tradeoff_matrix、go/hold、顧客SQE承認を評価できる。 |
| Reasoning | data_integrity | IR-DI-001 | 4 | electronics | 欠損・データソース信頼度・Safe Deferralの代表問題。must_have capの挙動も確認できる。 |
| Agent | tool_trajectory | IA-TT-001 | 4 | electronics | tool順序・approval gate・rollback/fallback・監査ログを評価。numeric_checksとscore_cap_rulesの発動を確認できる。 |
| Agent | hil_boundary | IA-HILB-001 | 4 | electronics | HIL境界・承認者・SLA・承認前禁止操作を評価。derived numeric不足によるcap発動を確認できる。 |

---

## 3. 出力ファイル

### JSON judgement

```text
results_v2/model_a/trial_judgements/IK-MAINT-001_judgement.json
results_v2/model_a/trial_judgements/IK-ORDER-004_judgement.json
results_v2/model_a/trial_judgements/IR-RT-001_judgement.json
results_v2/model_a/trial_judgements/IR-DI-001_judgement.json
results_v2/model_a/trial_judgements/IA-TT-001_judgement.json
results_v2/model_a/trial_judgements/IA-HILB-001_judgement.json
```

### Trial leaderboard

```text
results_v2/model_a/leaderboard_trial_v2.csv
```

---

## 4. 採点結果サマリ

| question_id | final_score | must_have_missing_count | numeric_check_failed_ratio | generic_penalty_triggered | critical_failure_triggered | cap発動状況 |
|---|---:|---:|---:|---|---|---|
| IK-MAINT-001 | 5 | 0 | 0.0000 | false | false | なし |
| IK-ORDER-004 | 5 | 0 | 0.0000 | false | false | なし |
| IR-RT-001 | 5 | 0 | 0.0000 | false | false | なし |
| IR-DI-001 | 4 | 1 | 0.0000 | false | false | must_have_missing max 4 |
| IA-TT-001 | 3 | 1 | 0.3333 | false | false | must_have_missing max 4 / numeric_checks max 3 / score_cap_rules max 3 |
| IA-HILB-001 | 2 | 2 | 0.2500 | false | false | must_have_missing max 3 / numeric_checks max 3 / score_cap_rules max 2 |

### スコア分布

| final_score | 件数 |
|---:|---:|
| 5 | 3 |
| 4 | 1 |
| 3 | 1 |
| 2 | 1 |
| 1 | 0 |

**確認結果:** 6問の試験採点では `4〜5点のみ` には集中せず、2〜5点に分布した。特にAgent層の2問では、回答全体は良好でも、scenario-specific numericや監査ログ項目の不足がcapで反映された。

---

## 5. 各問の採点コメント

### IK-MAINT-001 — final_score 5

- 年間故障費 `13,104,000円/年`、年間削減額 `5,176,800円`、回収期間 `0.7年` を回答内で明示。
- `4台先行`、`30ショット外観確認`、品質責任者を含む承認者を記載。
- `numeric_checks` は 3/3 pass。
- score cap / generic penalty / critical failure は未発動。

### IK-ORDER-004 — final_score 5

- v1.0既存カテゴリで、v1.1拡張フィールドは空。
- 試作の手組・全数検査と量産前提のギャップを指摘し、検査水準・変更管理・顧客承認範囲を合意事項として記載。
- v1.1専用フィールドなしでもJudge v2の後方互換的採点が可能であることを確認。

### IR-RT-001 — final_score 5

- 不良率 `4/200=2.0%`、顧客基準 `0.5%`、全数選別 `600,000円`、遅延ペナルティ `1,800,000円/日` を使用。
- `tradeoff_matrix`、`conditions_for_go`、`conditions_for_hold`、`required_approvals` を満たす。
- `numeric_checks` は 4/4 pass。
- 監査ログ詳細はnice_to_haveとして弱いが、必須要件とcap条件は満たした。

### IR-DI-001 — final_score 4

- 欠損 `7ロット`、欠損率 `7.0%`、保留 `3,360個`、出荷候補 `44,640個` は正しく使用。
- QMS / MES / ERP / 自動外観検査ログの trust level を分離。
- `required_rechecks` に再検査・検査員ヒアリング・QMS監査証跡はあるが、must_haveに含まれる `欠損原因の分類` が明示されていない。
- そのため `must_have_missing_count=1`、`must_have_score_cap=4` を適用。

### IA-TT-001 — final_score 3

- ERP → MES → QMS → SOP → QA通知 → hold draft の tool sequence は適切。
- QA approval gate を `release_hold_commit` 前に配置し、rollback/fallback も記載。
- ただし `QMS検査完了率 82.5%` が回答本文に明示されず、`numeric_check_failed_ratio=0.3333`。
- `numeric_checks` 失敗率が20%以上のため `numeric_score_cap=3`。
- さらに監査ログが `tool / input / output / approver / timestamp` を完全には分離しておらず、score_cap_rules max 3 も発動。

### IA-HILB-001 — final_score 2

- QA責任者(高橋)、誤承認者、SLA、承認前禁止操作は適切に設計。
- `missing_count=8`、`ng_suspect_count=2`、`shipment_deadline=360分` は記載。
- ただし `8/80=10.0%` の欠損率計算が回答本文に明示されず、numeric_checkが1/4 fail。
- `numeric_check_failed_ratio=0.25` のため numeric cap max 3。
- `欠損8件または欠損率10.0%を計算せず判断` の score_cap_rules が発動し、max 2。
- 最終スコアは `min(raw_final_score=4, cap=2)` により 2。

---

## 6. Judge v2 機能確認

### 6.1 final_score が4〜5に集中していないか

**PASS。**

結果は `5, 5, 5, 4, 3, 2` となり、2〜5点に分布した。v1.0で問題になった「全体的に4〜5点へ寄る」傾向は、少なくともこの6問では緩和されている。

### 6.2 score_cap_rules が必要時に発動しているか

**PASS。**

- `IA-TT-001`: 監査ログ項目が `tool / input / output / approver / timestamp` を完全に含まないため max 3。
- `IA-HILB-001`: 欠損率 `10.0%` を計算せず判断しているため max 2。
- `IR-DI-001`: 明示的score_cap_rulesではなく、must_have欠落cap max 4 が発動。

score cap は、回答が全体として自然・安全でも、scenario-specificな欠落がある場合に最終点を制限できている。

### 6.3 numeric_checks が実際に判定されているか

**PASS。**

- `IK-MAINT-001`: 3/3 pass
- `IR-RT-001`: 4/4 pass
- `IR-DI-001`: 4/4 pass
- `IA-TT-001`: 2/3 pass、82.5%未記載でfail
- `IA-HILB-001`: 3/4 pass、10.0%未記載でfail

数値が「暗黙に計算可能」でも、回答本文に明示されていない場合はfailとして扱われ、evidence requirementと整合している。

### 6.4 generic_answer_penalty が機能しているか

**限定的に確認。**

今回の `model_a` 回答は6問すべてでシナリオ固有の数値・ロール・条件を使っており、`scenario_specific_numbers_not_used` は発動しなかった。そのため、generic answer penaltyの発動例はこの6問では得られていない。

ただし、各judgement JSONでは `generic_answer_penalty_results` に条件別の判定と根拠を記録しており、generic answerが出た場合にmax 2 capを適用できる構造になっている。

### 6.5 evidence requirement により根拠なし加点が抑制されているか

**PASS。**

全judgement JSONで、以下に対して回答本文からの引用または要約を記録した。

- must_have_results
- nice_to_have_results
- numeric_check_results
- score_cap_rule_results
- generic_answer_penalty_results
- structured_output_results

引用・要約できない項目は `該当記述なし` または「明示なし」として未達扱いにした。特に `82.5%`、`10.0%`、`欠損原因の分類` は、推測補完せず減点した。

### 6.6 JSONがすべてparse可能か

**PASS。**

`results_v2/model_a/trial_judgements/*_judgement.json` の6ファイルはすべてJSONとしてparse可能であることを確認した。

---

## 7. v1.0 Judgeと比べた識別力改善

v1.0 Judgeでは、回答が安全側・一般論として自然であれば4〜5点に寄りやすかった。今回のJudge v2試験では、以下により識別力が改善している。

1. **must_have欠落数による上限**
   - `IR-DI-001` は大部分が良好でも、`欠損原因の分類` が未明示のため4点に制限された。

2. **numeric_checksの明示判定**
   - `IA-TT-001` の `82.5%`、`IA-HILB-001` の `10.0%` は暗算可能だが回答本文に明示されていないためfail。
   - これにより、数値を正しく使うモデルと、数値を一部省略するモデルの差が出る。

3. **score_cap_rulesによる危険・監査不能回答の上限制御**
   - `IA-TT-001` は監査ログ項目不足で max 3。
   - `IA-HILB-001` は欠損率計算不足で max 2。

4. **evidence requirementによる推測加点防止**
   - Judgeが回答本文にない内容を補完せず、証拠がない項目を未達扱いにできた。

このため、v1.1 Judge v2 は v1.0 よりも「自然だが不十分な回答」を低〜中スコアへ落とし、モデル差分を検出しやすい設計になっている。

---

## 8. 4モデル全件評価へ進んでよいか

**判定: 進んでよい。**

理由:

- 6件すべてで judgement JSON がparse可能。
- `leaderboard_trial_v2.csv` を生成できた。
- v1.0既存カテゴリも後方互換的に採点可能。
- v1.1問題では score_cap_rules / numeric_checks / structured_output_requirements が実際に機能した。
- final_score は2〜5に分布し、4〜5偏重を一定程度抑制できている。
- evidence requirementにより、根拠なし加点が抑えられている。

### 推奨事項

全件評価前に、Judge運用メモとして以下を明確化するとさらに安定する。

1. **暗算可能だが未記載の派生値をfailとする方針を維持する**
   - v1.1はscenario-specific numericを明示的に使えるかを評価するため、`66/80` があっても `82.5%` が required numeric_check なら fail とする。

2. **generic_answer_penaltyは複数モデル評価で再確認する**
   - 今回の6問ではgeneric回答がなかったため、4モデル全件評価で発動例を確認する。

3. **cap発動理由はleaderboardに短く残す**
   - モデル差分析時に、単なる点数差ではなく「numeric不足」「HIL境界不足」「監査ログ不足」などに分解できる。

---

## 9. 結論

P4-2 model_a 試験採点は完了した。Judge v2は、少なくとも今回の6問において、以下を満たしている。

- 高品質回答を5点として評価できる。
- 一部必須項目欠落を4点に制限できる。
- numeric_checks失敗率20%以上を3点以下へ制限できる。
- score_cap_rulesにより、HIL境界や監査ログ不足を2〜3点へ制限できる。
- evidence requirementにより、回答本文にない内容を補完せず採点できる。

したがって、次フェーズとして `model_b` / `model_c` / `model_d` の回答生成、または4モデル分のJudge v2全件評価へ進める状態である。
