---
name: kaggle-notebook-pull
description: Kaggle 公開ノートブックを nvidia-kaggle プラグインの DB でインデックス・検索し、精読対象の raw を reference/notebooks/raw/ に取得する。取得後は指定がなければ /summarize-notebook まで続けて実行する。公開ノートブックの調査・新着フロンティアの確認をするときに使う。
---

# 公開ノートブックの取得

一覧・検索・スコア調査は nvidia-kaggle プラグイン（DB は `data/`、git 管理外）で行い、
精読対象だけ raw を `reference/notebooks/raw/`（git 管理）に保存する。要約は後続の `/summarize-notebook` が担当。

## Step 1: インデックス・検索・スコア調査（プラグイン）

```bash
# コンテナ内 bash・リポジトリ直下で実行（DB が data/ に落ち、.env も自動ロードされる）
# .venv には必要パッケージが揃っているので .venv/bin/python で実行する（pip install 不要）
NVKG=$(ls -d ~/.claude/plugins/cache/nvidia-kaggle/nvidia-kaggle/*/skills/nvidia-kaggle-skill/scripts | head -1)
COMP=$KAGGLE_COMPETITION   # .env に定義（source 済みでなければ `set -a; source .env; set +a`）

# 公開カーネルを DB に取り込む（新着フロンティア確認は再実行するだけ）
.venv/bin/python "$NVKG/kernel_ingest.py" "$COMP" --sort-by voteCount

# 検索・絞り込み（キーワード・票数・投稿者。--as-json も可）
.venv/bin/python "$NVKG/kernel_query.py" "$COMP" --sort-by total_votes --limit 20
.venv/bin/python "$NVKG/kernel_query.py" "$COMP" --search <TERM>

# スコア付き上位一覧（スコアの向きは評価指標に合わせて --sort を選ぶ）
.venv/bin/python "$NVKG/fetch_top_kernel_scores.py" "$COMP" --sort descending
```

## Step 2: 精読対象の raw 取得（従来どおり kaggle CLI）

```bash
# 取得（メタデータ込み。-m が重要 — dataset_sources の確認に使う）
# 必ず <slug> ごとのサブディレクトリを指定する — フラットな reference/notebooks/raw/ 直下に
# 複数ノートブックを続けて pull すると、同名ファイル（kernel-metadata.json 等）が上書きされて
# 前のノートブックの取得結果が消える。
kaggle kernels pull <owner>/<slug> -p reference/notebooks/raw/<slug>/ -m
```

## Step 3: 要約へ引き継ぎ

取得できたら、ユーザーから別の指示がない限り **`/summarize-notebook` を続けて実行**する
（精読観点・要約フォーマット・INDEX 更新はそちらに定義）。
