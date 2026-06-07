# evaluation_v2 model_c Generation Report

## 1. 目的

P4-1 継続作業として、`evaluation_set_v2.yaml` 対象30問について `model_c` の回答を作成し、Judge v2 用の `judge_inputs` を生成した。

この段階では **採点は実行していない**。作業対象は `results_v2/` 配下と本レポートのみであり、`benchmark_data/`、`README.md`、`evaluation_set_v1.yaml`、`results/` は変更していない。

---

## 2. 入力と出力

### 入力

```text
results_v2/prompts/base/<question_id>.txt
```

### 回答保存先

```text
results_v2/model_c/answers/<question_id>.txt
```

### Judge input 保存先

```text
results_v2/model_c/judge_inputs/<question_id>_judge.md
```

### Judge input 生成コマンド

```bash
python scripts/prepare_judge_inputs_v2.py model_c
```

---

## 3. 対象30問

```text
IA-AS-001
IA-AS-003
IA-HILB-001
IA-HILB-003
IA-HILB-005
IA-SD-001
IA-SD-003
IA-SD-005
IA-TT-001
IA-TT-004
IK-MAINT-001
IK-MAINT-002
IK-MAINT-003
IK-MAINT-004
IK-MAINT-005
IK-MAINT-006
IK-MAINT-007
IK-MAINT-009
IK-ORDER-004
IK-SHIP-005
IR-DI-001
IR-DI-002
IR-DI-005
IR-DI-008
IR-DI-010
IR-RT-001
IR-RT-003
IR-RT-004
IR-RT-007
IR-RT-009
```

---

## 4. 生成結果

| 確認項目 | 結果 |
|---|---:|
| prompts 件数 | 30 |
| answers 保存数 | 30 |
| judge_inputs 生成数 | 30 |
| answer leakage hits | 0 |
| prompt leakage hits | 0 |
| UTF-8 decode errors | 0 |
| BOM / replacement char 検出 | 0 |
| JSON parse errors | 0 |
| 空または極端に短い回答 | 0 |
| judge input anchor 欠落 | 0 |

---

## 5. leakage check

以下の評価用・採点用語が、回答ファイルおよび base prompt に混入していないことを確認した。

```text
reference_answer
evaluation_rubric
must_have
nice_to_have
critical_failures
score_cap_rules
numeric_checks
disallowed_answers
expected_value
```

検出結果: **0件**

---

## 6. UTF-8 / 文字化け確認

`results_v2/model_c/answers/*.txt` について、以下を確認した。

- UTF-8 としてdecode可能
- BOMなし
- 置換文字 `U+FFFD` なし
- 空ファイルなし

結果: **PASS**

---

## 7. JSON parse確認

`results_v2/model_c/answers/*.txt` の30件について、すべて JSON としてparse可能であることを確認した。

結果: **30 / 30 PASS**

---

## 8. judge_inputs 生成確認

`python scripts/prepare_judge_inputs_v2.py model_c` を実行し、30件の Judge v2 入力を生成した。

生成件数: **30 / 30**

各 judge input には `### Model Answer` セクションが存在することを確認した。採点は未実行。

---

## 9. 判定

`model_c` のP4-1回答生成は完了。回答数、judge_inputs数、leakage、UTF-8、JSON parse の全確認項目が PASS である。

次工程では、`model_a`〜`model_d` の全回答が揃った状態で、Judge v2 による全件採点へ進める。
