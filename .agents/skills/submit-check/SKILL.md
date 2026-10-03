---
name: submit-check
description: Kaggle 提出前のチェックリスト。提出する前に必ず使う。
---

# 提出前チェック

ルールは `docs/workflow.md` の「提出」。ここではそれを上から順に確かめる。1 つでも満たさない項目があれば提出せずユーザーに報告する。

## Step 1: 承認

- [ ] 何を、どの提出枠で出すかについてユーザーの承認を得ているか

## Step 2: 残り回数

```bash
tools/nvkg submission_quota "$KAGGLE_COMPETITION"
```

- [ ] `Status: EXHAUSTED` でないか。`Status: UNKNOWN` なら Kaggle の提出ページで残り回数を確認する

## Step 3: ローカル検証

- [ ] 提出物がローカルでエラーなく最後まで実行でき、出力がコンペの提出形式に合っているか
- [ ] CV またはローカル評価が、実験開始時に決めた基準を満たしているか

## Step 4: 二重提出の確認

```bash
uv run kaggle competitions submissions "$KAGGLE_COMPETITION"
```

- [ ] 同じ実験・同じメッセージの提出がまだ無いか（他のエージェントや前回の実行が先に出していれば提出しない）

## Step 5: 提出形式固有の確認

- [ ] Notebook 提出の場合、`exp/<ID>/kernel-metadata.json` が `docs/workflow.md` の「提出前に確かめること」のとおりか（`id`・`is_private`・`enable_internet`・`competition_sources`）

- [ ] ファイル提出の場合、列・行数・欠損・エントリポイントなど、`README.md` の「コンペ概要」の「提出」に定めた形式を満たしているか

## Step 6: 提出

`docs/workflow.md` の「提出のしかた」のコマンドを順に実行する。採点結果は待たない。

- [ ] `uv run kaggle competitions submissions "$KAGGLE_COMPETITION"` で受理されたことを確認したか（出力がなくても submit を再実行しない）

結果が出たら `/save-knowledge` で記録する。
