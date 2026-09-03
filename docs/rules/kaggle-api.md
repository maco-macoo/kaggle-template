# Kaggle API の運用

- 実行は **Windows PowerShell + `uv run kaggle`** または **コンテナ内 bash + `kaggle`**。
  認証はコンテナ内 bash の場合、リポジトリ直下の **`.env`**（git 管理外・`.gitignore` 済み）に
  `KAGGLE_API_TOKEN=...` を定義し（雛形: `.env.example`）、`set -a; source .env; set +a` を前置してから `kaggle` を叩く。
  トークンを個別ファイル（`~/.kaggle/kaggle.json` 等）に分散させない — 環境変数は `.env` に一括で集約する。
- **`$env:PYTHONUTF8 = "1"` が必須**（PowerShell で cp932 になり日本語が壊れる）。
- **CLI の stdout をパイプしない**（PowerShell で `kaggle ... | Select-Object` 等は broken pipe で exit 255 になりうる）。
  JSON が要るときは `--format json` を Python の subprocess で捕捉するか、ファイルに書く
  （`>` リダイレクトは UTF-16 になるため `| Out-File -Encoding utf8` を使う）。
- 大量取得は `tools/` のスクリプト経由で行う（リトライ・スリープ・増分管理込み。手打ちで連打しない）。

## nvidia-kaggle プラグインとの役割分担

Discussion・公開ノートブックの**索引・検索**（一覧性のある調査）は nvidia-kaggle プラグインの
SQLite DB（`data/*.db`、git 管理外）に委譲する（`/kaggle-discussion-pull`・`/kaggle-notebook-pull` が呼ぶ）。
精読対象だけ raw を `reference/*/raw/`（git管理）に保存し、要約（我々への含意まで書いたもの）だけを
`reference/*/summary/` に残す。**DB の中身をまるごと docs 化しない** — 探索段階のノイズまで
git 管理下に置くと知見の正本が肥大化する。

提出まわりも同様に、機械的な操作（提出クォータ確認・提出履歴ログ）はプラグインの
`submission_quota.py` / `submission_history.py`（コードコンペのカーネル提出は `submit_kernel.py`）に
委譲し、`/submit-check`（本リポジトリ固有）はゲート判定・チェックリストという解釈作業に専念する
（`docs/rules/submission.md` 参照）。

## コマンド集（例。実行前に `kaggle --version` で動作確認しておく）

```powershell
# LB
uv run kaggle competitions leaderboard <slug> -s --format json --page-size 200

# 自分の提出・ログ
uv run kaggle competitions submissions <slug>

# 提出（CSV 直接提出の場合）
uv run kaggle competitions submit <slug> -f submission.csv -m "..."

# 公開カーネル / Discussion（一覧性のある調査は nvidia-kaggle プラグインの DB 経由を推奨。
# raw の直接取得はプラグイン導入前や単発取得のときに使う）
uv run kaggle kernels list --competition <slug> --sort-by voteCount --page-size 20
uv run kaggle kernels pull <owner>/<slug> -p reference/notebooks/raw/ -m
uv run kaggle competitions topics -c <slug>
uv run kaggle competitions topic <topic-id>
```

シミュレーション/エージェント提出コンペのみで使うコマンド（テーブル/画像/NLP系コンペでは不要）:

```powershell
# 他チームの提出一覧・エピソード・リプレイ（kaggle-environments 系コンペのみ存在するエンドポイント）
uv run kaggle competitions team-submissions <teamId>
uv run kaggle competitions episodes <submissionId>
uv run kaggle competitions replay <episodeId> -p <dir>
```

## 既知の罠

- **`kaggle competitions submit` は成功しても無出力**なことがある。提出直後は必ず `submissions` で受理確認。
  無出力・exit≠0 に見えても**再実行しない**（二重提出により枠を失うリスクがある）。
- コードコンペではノートブックの実行ログ（他ユーザー分）は取得不可。分析は自分のログ・公開情報に依存する。
