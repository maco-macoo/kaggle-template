---
name: summarize-notebook
description: 取得済み（reference/notebooks/raw/ にある）Kaggle 公開ノートブックを精読し、要約を reference/notebooks/summary/ に作成して INDEX を更新する。/kaggle-notebook-pull の後続、または既に raw がある NB を後から要約するときに使う。
---

# 公開ノートブックの要約

対象の raw（`reference/notebooks/raw/<slug>/` または exp ローカルコピー）を精読し、知見をコミット対象の要約に落とす。

## Step 1: 精読の観点

1. **外部 artifact 依存の判定（`docs/rules/external-data.md`）**: `kernel-metadata.json` の `dataset_sources` と
   コード内の pretrained モデル・外部ファイルのロードを確認。
   - コンペルール上問題ない依存か？由来を説明できるか？
   - 「スコアされた実体」が見えているコードか、外部ロード物かを区別する
     （visible コードと採点された実体が別物のことがある）
2. **スコア上乗せの成分分解**（public LB 専用のリーク・ハック成分がないか分離してから追う）
3. 新規アルゴリズムか、我々の実装済み手法の別名か（「公開の目玉」が実装済みのことは多い）
4. `docs/experiments/INDEX.md` と照合し、既に RED/NO-GO 済みの構想でないか

## Step 2: 要約の作成

`reference/notebooks/summary/<owner>_<slug>.md` に作成:

```markdown
# <owner>/<slug>（スコア x.xxx, 取得日 YYYY-MM-DD）

## 概要（何をしているか）
## 外部 artifact 依存（判定と根拠）
## 我々への含意（新規性 / 既検証との照合 / 追うべきか）
## raw の場所
reference/notebooks/raw/<slug>/（git 管理・再取得も可能）
```

## Step 3: INDEX 更新

`reference/INDEX.md` のノートブック表に1行追記（**我々への含意を必ず書く**）。
追う価値ありと判断した場合はユーザーに提案（実験化は `/new-exp`）。
