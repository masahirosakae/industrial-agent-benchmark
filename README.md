# Industrial Agent Benchmark

Industrial Agent Benchmark は、製造業における AI エージェントの実務能力を評価するための公開ベンチマークです。

v2.0.0 は Industrial Agent Benchmark の初の Stable Public Release です。現在のデータセットには英語タスクと日本語タスクが混在しており、v2.1.0 で multilingual architecture を整理する予定です。この日本語 README では、日本の製造業でこのベンチマークが必要になる背景と使い方を説明します。

English README: [README_EN.md](README_EN.md)

## 現在のリリース

| Version | Status | Summary |
|---|---|---|
| v1.0 | Public baseline | 初期 90 問のベンチマークと judge 方法論。 |
| v1.1.0 | Frozen pre-release snapshot | 140 問の pre-release snapshot。互換性確認用に保持。 |
| v2.0.0 | Stable Public Release | 180 問の公開データセット、HF-compatible JSONL、公開検証 workflow。英語と日本語のタスクが混在。 |

v2.0.0 は、HLE-like な公開モデルを意識して設計しています。

- 問題データは公開リポジトリで管理
- Hugging Face Datasets で読み込みやすい JSONL を提供
- 評価スクリプトとドキュメントを GitHub で公開
- 生成回答、モデル別結果、非公開評価ログは commit しない
- leaderboard は将来の安定した judge 互換性ルールの後に検討

Language note:

- v2.0.0 の実データは English / Japanese / Mixed を含みます。
- v2.0.1 は、この実態に合わせるための Documentation & Metadata Correction Release です。
- v2.1.0 では、言語別 metadata、multilingual 評価方針、English/Japanese task design を整理する予定です。

## Why Industrial Agent Benchmark?

製造業で AI エージェントを使う場合、一般的な会話能力だけでは十分ではありません。現場では、受注、計画、購買、製造、検査、出荷、保全、変更管理などがつながっており、ひとつの判断が品質、納期、安全、トレーサビリティに影響します。

特に日本の製造業では、以下のような実務上の論点があります。

- 熟練者の暗黙知を、どこまで標準化された判断として扱えるか
- 不具合、手戻り、特採、変更管理を、証跡付きで説明できるか
- 自動化してよい作業と、人の承認が必要な作業を区別できるか
- 現場データ、帳票、指示書、検査記録をまたいで矛盾を見つけられるか
- 改善提案だけでなく、実行前にリスクと制約を確認できるか

Industrial Agent Benchmark は、こうした製造業固有の能力を、知識・推論・エージェント行動の 3 層で評価するための土台です。

## v2.0.0 データセット構成

v2.0.0 Stable Release は 180 問です。

| Layer | Count | 評価対象 |
|---|---:|---|
| Industrial Knowledge | 60 | 製造業務、品質、保全、変更管理などの知識 |
| Industrial Reasoning | 60 | 根本原因分析、FMEA、CAPA、能力計画、リスク判断 |
| Industrial Agent | 60 | tool selection、workflow design、human-in-the-loop、安全な実行境界 |
| Total | 180 |  |

ローカルの Hugging Face-compatible JSONL は以下です。

```text
data/v2/test.jsonl
```

Dataset card: [dataset_card.md](dataset_card.md)

## Quick Start

### Requirements

- Python 3.10+
- PyYAML

```bash
pip install pyyaml
```

### データセット検証

```bash
python scripts/validate_dataset.py
```

Expected output:

```text
Checked: 180 problem files
Errors: 0
Warnings:0
```

### JSONL export

```bash
python scripts/export_hf_dataset_v2.py
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

### Hugging Face Datasets 形式で読み込む

```bash
python examples/load_dataset_v2.py
```

Hugging Face Hub で公開する場合も、この `data/v2/test.jsonl` と [dataset_card.md](dataset_card.md) を中心に利用します。

## リポジトリ構成

```text
industrial-agent-benchmark/
  README.md
  README_EN.md
  dataset_card.md
  data/
    v2/
      test.jsonl
  benchmark_data/
    index.yaml
    index.csv
    knowledge/
    reasoning/
    agent/
  docs/
  examples/
  eval/
  scripts/
```

## 評価アーキテクチャ

v2.0.0 は、次の judge 方向を想定しています。

| Layer | Judge direction |
|---|---|
| Industrial Knowledge | Deterministic Judge |
| Industrial Reasoning | Rubric Judge plus numeric checks |
| Industrial Agent | Executable Judge |

現時点の公開リポジトリは、データセット検証、JSONL export、簡易評価のための基盤を提供します。モデル回答や評価結果は含めません。

## Public Artifact Policy

このリポジトリは fresh clone で検証できる公開成果物だけを含めます。

commit しないもの:

- raw model answers
- `results_v2/`
- `results/`
- judge inputs / judge outputs
- model-specific evaluation results
- unpublished reports
- provider/model-name mappings
- API keys, `.env`, tokens, credentials

## ライセンス

Code: Apache License 2.0. See [LICENSE](LICENSE).

Dataset: see [LICENSE_DATASET.md](LICENSE_DATASET.md).
