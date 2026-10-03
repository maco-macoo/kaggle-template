---
name: public-insights
description: Kaggle の公開ノートブックと Discussion を扱う。DB の更新・検索・本文の読み取り・要約の作成のどれにでも使う。
---

# 公開ノートブックと Discussion

ルール（どこに何を置くか、読むときの観点）は `docs/workflow.md` の「公開情報の活用」。
ここには使える機能を記載する。希望に合うものを選んで使い、順番に全部やる必要はない。
コマンドはコンテナ内のリポジトリ直下で実行する。

## DB を更新する

一覧を Kaggle API から取り、差分を DB（`data/kernels.db`、`data/discussions.db`）に upsert する。
検索・読み取りの前に DB が古そうなら先に実行する。

```bash
tools/nvkg kernel_ingest "$KAGGLE_COMPETITION" --sort-by voteCount
tools/nvkg discussion_ingest "$KAGGLE_COMPETITION" --sort-by updated   # 既定は 5 ページまで。全部なら --max-pages を増やす
```

## DB の状態を見る

```bash
tools/nvkg kernel_db_info "$KAGGLE_COMPETITION"
tools/nvkg discussion_db_info "$KAGGLE_COMPETITION"
```

## 探す

DB は SQLite なので、目的に合わせて自由に問い合わせてよい。

- 簡単な検索・並べ替えは、プラグインの `kernel_query` / `discussion_query` が近道になる（オプションは `tools/nvkg kernel_query -h` で確かめる）
- 集計や複雑な条件は SQL で書く。`sqlite3` コマンドは入っていないので Python から実行する

```bash
uv run python - <<'PY'
import sqlite3
for row in sqlite3.connect("data/discussions.db").execute("SELECT ..."):
    print(row)
PY
```

| DB | テーブル | 主な列 |
| --- | --- | --- |
| `data/kernels.db` | `kernels` | `competition_id` `kernel_ref` `title` `author` `total_votes` `last_run_time` |
| `data/discussions.db` | `discussions` | `competition_id` `discussion_id` `title` `author` `votes` `comment_count` `body_markdown` `tags` `created_at` `updated_at` |
| `data/discussions.db` | `discussion_comments` | `discussion_id` `author` `votes` `body_markdown` `created_at` |

DB に無いもの:

- ノートブックのコード：「読む」で取ってくる
- ノートブックの public LB スコア：`tools/nvkg fetch_top_kernel_scores "$KAGGLE_COMPETITION" --sort descending` で API から取る
- 要約済みかどうか：`reference/INDEX.md` で確かめる

## 読む

```bash
# 初回はダウンロードし data/notebooks/ にキャッシュ。最新版は --force
tools/nvkg kernel_read <owner/slug> --competition-id "$KAGGLE_COMPETITION"

# DB から本文とコメントを表示
tools/nvkg discussion_read <topic-id> --competition-id "$KAGGLE_COMPETITION"
```

## 要約を書く

ノートブックは `reference/notebooks/<owner>_<slug>.md`、Discussion は `reference/discussions/<topic-id>_<slug>.md` に書き、`reference/INDEX.md` の該当する表に 1 行追記する。
すでに要約があるものは、内容が更新されたときだけ追記する。

```markdown
# <タイトル>

- ID: <owner/slug または topic-id>
- 著者 / 票 / スコア: <...>
- 読んだ日: YYYY-MM-DD

## 要点
（何をしている / 何を主張しているか）

## 根拠と外部依存

## こちらへの含意
（新しい点 / 試したことがある点 / 追う価値があるか）
```

追う価値があると判断したらユーザーに提案する（実験にするなら `/new-exp`）。
