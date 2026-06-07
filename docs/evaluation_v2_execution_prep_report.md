# Evaluation v2 Execution Preparation Report

Industrial Agent Benchmark v1.1 の識別力検証に向け、`evaluation_set_v2.yaml` と `judge_template_v2.md` を用いた評価実行準備を完了した。本段階では、モデル回答生成および採点は実行していない。

## 1. evaluation_set_v2 の30問確認結果

`evaluation_set_v2.yaml` を読み込み、`benchmark_data/index.yaml` と照合した。30問すべてについて `question_id / layer / category / difficulty / domain / file_path` を確認済み。

| question_id | layer | category | difficulty | domain | file_path |
| --- | --- | --- | ---: | --- | --- |
| IK-MAINT-001 | industrial_knowledge | maintenance_engineering | 3 | general_manufacturing | benchmark_data/knowledge/maintenance_engineering/IK-MAINT-001.yaml |
| IK-MAINT-002 | industrial_knowledge | maintenance_engineering | 4 | electronics | benchmark_data/knowledge/maintenance_engineering/IK-MAINT-002.yaml |
| IK-MAINT-003 | industrial_knowledge | maintenance_engineering | 3 | general_manufacturing | benchmark_data/knowledge/maintenance_engineering/IK-MAINT-003.yaml |
| IK-MAINT-004 | industrial_knowledge | maintenance_engineering | 4 | automotive | benchmark_data/knowledge/maintenance_engineering/IK-MAINT-004.yaml |
| IK-MAINT-005 | industrial_knowledge | maintenance_engineering | 4 | general_manufacturing | benchmark_data/knowledge/maintenance_engineering/IK-MAINT-005.yaml |
| IK-MAINT-006 | industrial_knowledge | maintenance_engineering | 3 | heavy_machinery | benchmark_data/knowledge/maintenance_engineering/IK-MAINT-006.yaml |
| IK-MAINT-007 | industrial_knowledge | maintenance_engineering | 4 | automotive | benchmark_data/knowledge/maintenance_engineering/IK-MAINT-007.yaml |
| IK-SHIP-005 | industrial_knowledge | shipping | 4 | automotive | benchmark_data/knowledge/shipping/IK-SHIP-005.yaml |
| IK-MAINT-009 | industrial_knowledge | maintenance_engineering | 5 | general_manufacturing | benchmark_data/knowledge/maintenance_engineering/IK-MAINT-009.yaml |
| IK-ORDER-004 | industrial_knowledge | order | 3 | medical_device | benchmark_data/knowledge/order/IK-ORDER-004.yaml |
| IR-RT-001 | industrial_reasoning | risk_tradeoff | 4 | electronics | benchmark_data/reasoning/risk_tradeoff/IR-RT-001.yaml |
| IR-RT-003 | industrial_reasoning | risk_tradeoff | 4 | heavy_machinery | benchmark_data/reasoning/risk_tradeoff/IR-RT-003.yaml |
| IR-RT-004 | industrial_reasoning | risk_tradeoff | 5 | automotive | benchmark_data/reasoning/risk_tradeoff/IR-RT-004.yaml |
| IR-RT-007 | industrial_reasoning | risk_tradeoff | 4 | electronics | benchmark_data/reasoning/risk_tradeoff/IR-RT-007.yaml |
| IR-RT-009 | industrial_reasoning | risk_tradeoff | 3 | general_manufacturing | benchmark_data/reasoning/risk_tradeoff/IR-RT-009.yaml |
| IR-DI-001 | industrial_reasoning | data_integrity | 4 | electronics | benchmark_data/reasoning/data_integrity/IR-DI-001.yaml |
| IR-DI-002 | industrial_reasoning | data_integrity | 4 | general_manufacturing | benchmark_data/reasoning/data_integrity/IR-DI-002.yaml |
| IR-DI-005 | industrial_reasoning | data_integrity | 4 | medical_device | benchmark_data/reasoning/data_integrity/IR-DI-005.yaml |
| IR-DI-008 | industrial_reasoning | data_integrity | 4 | electronics | benchmark_data/reasoning/data_integrity/IR-DI-008.yaml |
| IR-DI-010 | industrial_reasoning | data_integrity | 5 | automotive | benchmark_data/reasoning/data_integrity/IR-DI-010.yaml |
| IA-AS-001 | industrial_agent | agent_safety | 4 | electronics | benchmark_data/agent/agent_safety/IA-AS-001.yaml |
| IA-AS-003 | industrial_agent | agent_safety | 5 | general_manufacturing | benchmark_data/agent/agent_safety/IA-AS-003.yaml |
| IA-TT-001 | industrial_agent | tool_trajectory | 4 | electronics | benchmark_data/agent/tool_trajectory/IA-TT-001.yaml |
| IA-TT-004 | industrial_agent | tool_trajectory | 5 | general_manufacturing | benchmark_data/agent/tool_trajectory/IA-TT-004.yaml |
| IA-HILB-001 | industrial_agent | hil_boundary | 4 | electronics | benchmark_data/agent/hil_boundary/IA-HILB-001.yaml |
| IA-HILB-003 | industrial_agent | hil_boundary | 4 | heavy_machinery | benchmark_data/agent/hil_boundary/IA-HILB-003.yaml |
| IA-HILB-005 | industrial_agent | hil_boundary | 5 | automotive | benchmark_data/agent/hil_boundary/IA-HILB-005.yaml |
| IA-SD-001 | industrial_agent | structured_decision | 4 | electronics | benchmark_data/agent/structured_decision/IA-SD-001.yaml |
| IA-SD-003 | industrial_agent | structured_decision | 4 | heavy_machinery | benchmark_data/agent/structured_decision/IA-SD-003.yaml |
| IA-SD-005 | industrial_agent | structured_decision | 5 | automotive | benchmark_data/agent/structured_decision/IA-SD-005.yaml |

## 2. prompt 作成件数

- 出力先: `results_v2/prompts/base/`
- 作成件数: 30件
- ファイル形式: `<question_id>.txt`
- 含めた内容: question metadata / scenario / question
- 除外した内容: reference answer、rubric、score cap、numeric check、disallowed answer など採点用情報

## 3. prompt leakage check 結果

以下の禁止語を全30 promptに対して検索した。

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
結果: **leakage_hits = NONE**。採点用情報の prompt 混入は検出されなかった。

## 4. results_v2 構成

`results_v2/` は `.gitignore` に追加済み。公開対象には含めず、ローカル評価作業用ディレクトリとして扱う。

```text
results_v2/
  prompts/
    base/
      <question_id>.txt  # 30 files
  model_a/
    answers/
    judge_inputs/
  model_b/
    answers/
    judge_inputs/
  model_c/
    answers/
    judge_inputs/
  model_d/
    answers/
    judge_inputs/
  leaderboard_v2_template.csv
  evaluation_set_v2_questions.csv
```

モデル識別子は中立的な `model_a`〜`model_d` のみを使用し、公開ドキュメントに固有のモデル名は記載しない。

## 5. leaderboard_v2_template.csv 仕様

作成ファイル: `results_v2/leaderboard_v2_template.csv`

| column | description |
| --- | --- |
| model_id | 中立的なモデルID |
| question_id | 評価対象問題ID |
| layer | industrial_knowledge / industrial_reasoning / industrial_agent |
| category | 問題カテゴリ |
| difficulty | 難易度 |
| domain | ドメイン |
| final_score | Judge v2 最終スコア |
| must_have_missing_count | must_have 欠落数 |
| numeric_check_failed_ratio | numeric_checks 失敗率 |
| generic_penalty_triggered | generic answer penalty 発火有無 |
| critical_failure_triggered | critical_failure 発火有無 |
| score_cap_applied | 適用された score cap |
| judge_summary | Judge コメント要約 |

## 6. prepare_judge_inputs_v2.py 仕様

作成ファイル: `scripts/prepare_judge_inputs_v2.py`

主な機能:
- 指定した `results_v2/<model_id>/answers/` から `<question_id>.txt` を読み込む。
- `evaluation_set_v2.yaml` と `benchmark_data/index.yaml` を用いて対象問題YAMLを特定する。
- `judge_template_v2.md` に以下を埋め込む。
  - scenario
  - question
  - reference_answer
  - evaluation_rubric
  - score_cap_rules
  - numeric_checks
  - generic_answer_penalty
  - structured_output_requirements
  - disallowed_answers
  - model_answer
- `results_v2/<model_id>/judge_inputs/<question_id>_judge.md` を出力する。

使用例:
```bash
python scripts/prepare_judge_inputs_v2.py model_a
python scripts/prepare_judge_inputs_v2.py model_a --allow-missing
```
確認結果: `python -m py_compile scripts/prepare_judge_inputs_v2.py` は成功。`--allow-missing` 付きのドライ実行では、回答未生成のため0件作成・30件skipとなることを確認済み。

## 7. 次に人間が実施すべき回答生成手順

1. `results_v2/prompts/base/<question_id>.txt` を対象モデルへ入力する。
2. 各回答を `results_v2/<model_id>/answers/<question_id>.txt` として保存する。
3. 30問すべての回答が揃ったら、以下を実行する。
```bash
python scripts/prepare_judge_inputs_v2.py model_a
python scripts/prepare_judge_inputs_v2.py model_b
python scripts/prepare_judge_inputs_v2.py model_c
python scripts/prepare_judge_inputs_v2.py model_d
```
4. 生成された `judge_inputs/` 内の `<question_id>_judge.md` を Judge v2 に入力する。
5. Judge JSON 出力を収集し、`leaderboard_v2_template.csv` の列構造に従って集計する。
6. `final_score` だけでなく、must_have欠落数、numeric_check失敗率、generic penalty、critical failure、score cap発火率を比較する。

## 8. 制約遵守

- `benchmark_data/` は変更していない。
- `README.md` は変更していない。
- `evaluation_set_v1.yaml` は変更していない。
- `results/` は変更していない。
- `results_v2/` は `.gitignore` 対象。
- 公開対象ドキュメントに固有のモデル名や非公開運用情報は記載していない。


## 9. レビュー監査結果 (Critical Review)

P4 成果物に対して、独立に以下の追加監査を実施した。

### 9.1 ユーザー指定 leakage トークン (binding requirement)

以下のトークン名が prompt に含まれていないかを 30 件全件について再検証した。

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

結果: **NONE** (PASS)

### 9.2 深層オーバーラップ監査 (informational)

トークン名一致だけでなく、rubric の `must_have` / `disallowed_answers` 本文と prompt 本文の文字列一致を 25/20 字単位で網羅検査した。検出された 21 件のオーバーラップはすべて以下のいずれかに該当し、Judge 情報の漏えいではないことを確認した。

- `disallowed_answers` オーバーラップ (11 件): scenario が「誤った近道」を意図的に narrative として明示しており、rubric の disallowed_answers がその文言を引用しているため。モデルが見る prompt には scenario の narrative のみが含まれ、rubric は提示されない。これは Batch 5/6/7 の意図的な trap 設計である。
- `must_have` オーバーラップ (10 件): rubric の must_have が `structured_output_requirements.required_fields` (例: `trust_level_by_source / detected_issues / conditions_for_go`) に anchor しており、question が同じフィールド名を出力指示として明示しているため。必須出力フォーマットの伝達は仕様上必要であり、Judge 情報の漏えいではない。

全 21 件について scenario または question への trace を確認済み。真の漏えい (neither scenario nor question) はゼロ件。

### 9.3 prepare_judge_inputs_v2.py end-to-end smoke test

ダミー回答を 1 件投入し、Judge input が正しく生成されることを実機検証した。

確認項目:

- Created judge input files: 1 / Skipped: 29 (期待通り)
- 生成された judge md 内に以下のアンカーがすべて存在
  - question_id, Scenario, Question, Reference Answer
  - Must Have, Nice to Have, Critical Failures
  - score_cap_rules, numeric_checks, generic_answer_penalty
  - structured_output_requirements, disallowed_answers
  - Model Answer (ダミー回答本文)
- 未解決テンプレートトークン: NONE
- judge input サイズ: 約 8.3 KB

結果: PASS。スクリプトは設計通り動作し、Judge v2 に投入可能な形で v1.1 拡張フィールドをすべて埋め込む。

### 9.4 BOM・公開ドキュメント禁止語

- 公開対象成果物 (`.gitignore` / `scripts/prepare_judge_inputs_v2.py` / `docs/evaluation_v2_execution_prep_report.md`) と `results_v2/` 配下生成物: いずれも BOM なし。
- 公開対象成果物: 特定モデル名・特定ベンダー名・テスト運用情報の禁止語ゼロ。

### 9.5 制約遵守

- `benchmark_data/` は本フェーズで変更なし (索引のみ過去バッチで更新済み)。
- `README.md` 変更なし。
- `evaluation_set_v1.yaml` 変更なし。
- `results/` 変更なし。
- `results_v2/` は `.gitignore` 対象として正しく除外され、`git check-ignore` で確認済み。

### 9.6 監査結論

P4 評価実行準備の全成果物 (prompts 30 件、results_v2 構成、leaderboard テンプレート、Judge input 生成スクリプト、レポート) は仕様を満たし、人間による回答生成フェーズへの移行準備が完了している。
