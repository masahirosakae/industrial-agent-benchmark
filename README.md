# Industrial Agent Benchmark

Industrial Agent Benchmark は、製造業向け AI、Manufacturing AI Assistant、Industrial Agent を評価するための公開ベンチマークです。

日本語を canonical language とし、製造現場で重要になる知識、推論、エージェント動作を 3 層で評価します。英語版は今後、日本語 canonical dataset から派生する translated distribution として扱います。

English overview: [README_EN.md](README_EN.md)

## 現在のリリース

**v2.2.0: Japanese Canonical Normalization**

v2.2.0 では、v2.0.x で残っていた English-only tasks を日本語 canonical form へ移行しました。

- Total: 180 tasks
- Knowledge: 60
- Reasoning: 60
- Agent: 60
- English-only tasks: 45 -> 0
- Validation/export pipeline: preserved
- Primary dataset file: `data/v2/test.jsonl`

注意: `data/v2/test.jsonl` の一部 schema/version fields は互換性維持のため historical field values を保持しています。リリース状態としては v2.2.0 が現在の公開版です。

## Why Industrial Agent Benchmark?

製造業で AI エージェントを使う場合、一般的な会話能力だけでは不十分です。現場では、品質保留、出荷判定、CAPA、FMEA、工程変更、設備制約、要員制約、承認境界、監査証跡が実務判断に直結します。

Industrial Agent Benchmark は、次の観点を評価するために設計されています。

- 製造業の基本知識を正しく扱えるか
- 数値制約、能力、歩留まり、リスクを踏まえて推論できるか
- 人による承認が必要な行動を自律実行しないか
- 推奨、ドラフト、実行、リリース、出荷を区別できるか
- 監査可能な証拠、判断、エスカレーションを残せるか

## Dataset Overview

| Layer | Count | Focus |
|---|---:|---|
| Industrial Knowledge | 60 | 製造知識、手順、品質、保全、変更管理 |
| Industrial Reasoning | 60 | 根本原因分析、FMEA、CAPA、リスク判断、数値能力計画 |
| Industrial Agent | 60 | workflow design、tool selection、human-in-the-loop、承認境界、監査性 |
| Total | 180 |  |

Primary JSONL artifact:

```text
data/v2/test.jsonl
```

Dataset card:

```text
dataset_card.md
```

Hugging Face Dataset:

```text
https://huggingface.co/datasets/MSakae/industrial-agent-benchmark
```

## Quick Start

### Requirements

- Python 3.10+
- PyYAML

```bash
pip install pyyaml
```

### Validate benchmark YAML

```bash
python scripts/validate_dataset.py
```

Expected output:

```text
Checked: 180 problem files
Errors: 0
Warnings:0
```

### Export and validate HF-compatible JSONL

```bash
python scripts/export_hf_dataset_v2.py
python scripts/validate_hf_dataset_v2.py data/v2/test.jsonl
```

### Load locally

```bash
python examples/load_dataset_v2.py
```

## Evaluation Architecture

| Layer | Judge direction |
|---|---|
| Industrial Knowledge | Deterministic Judge |
| Industrial Reasoning | Rubric Judge plus numeric checks |
| Industrial Agent | Executable Judge |

The repository includes validation, export, schema documentation, and local evaluation utilities. It does not include generated model answers, private judge outputs, provider-specific results, or leaderboard data.

## Public Artifact Policy

Do not commit:

- raw model answers
- `results/`
- `results_v2/`
- judge inputs or judge outputs
- provider-specific evaluation results
- private reports
- API keys, `.env`, tokens, credentials

## License

Code: Apache License 2.0. See [LICENSE](LICENSE).

Dataset: see [LICENSE_DATASET.md](LICENSE_DATASET.md).
