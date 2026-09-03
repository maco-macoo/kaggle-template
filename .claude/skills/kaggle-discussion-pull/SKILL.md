---
name: kaggle-discussion-pull
description: Kaggle Discussion を nvidia-kaggle プラグインの DB に一括インデックスして検索し、精読対象の raw を reference/discussions/raw/ に保存する。取得後は指定がなければ /summarize-discussion まで続けて実行する。Discussion の調査・定点観測をするときに使う。
---

# Discussion の取得

一覧・検索は nvidia-kaggle プラグインの SQLite DB（`data/discussions.db`、git 管理外）で行い、
精読対象だけ raw を `reference/discussions/raw/`（git 管理）に保存する。要約は後続の `/summarize-discussion` が担当。

## Step 1: インデックスと検索（プラグイン DB）

```bash
# コンテナ内 bash・リポジトリ直下で実行（DB が data/ に落ち、.env も自動ロードされる）
# .venv には必要パッケージが揃っているので .venv/bin/python で実行する（pip install 不要）
NVKG=$(ls -d ~/.claude/plugins/cache/nvidia-kaggle/nvidia-kaggle/*/skills/nvidia-kaggle-skill/scripts | head -1)
COMP=$KAGGLE_COMPETITION   # .env に定義（source 済みでなければ `set -a; source .env; set +a`）

# 全トピックを DB に取り込む（定点観測は再実行するだけで差分更新）
.venv/bin/python "$NVKG/discussion_ingest.py" "$COMP" --sort-by updated

# 検索・絞り込み（キーワード・票数・投稿者。--as-json も可）
.venv/bin/python "$NVKG/discussion_query.py" "$COMP" --sort-by votes --limit 20
.venv/bin/python "$NVKG/discussion_query.py" "$COMP" --search <TERM> --min-votes 5

# 中身をその場で流し読み（保存はしない）
.venv/bin/python "$NVKG/discussion_read.py" <topic-id> --competition-id "$COMP"
```

## Step 2: 精読対象の raw 保存（従来どおり kaggle CLI）

```bash
# 本文は Markdown なので .md で保存する
# （ホスト PowerShell で打つ場合の注意は docs/rules/kaggle-api.md — 特に `>` が UTF-16 保存になり raw を汚す）
kaggle competitions topics show "$COMP" <topic-id> > reference/discussions/raw/<topic-id>.md
```

## Step 3: 要約へ引き継ぎ

取得できたら、ユーザーから別の指示がない限り **`/summarize-discussion` を続けて実行**する
（精読観点・要約フォーマット・INDEX 更新はそちらに定義）。
