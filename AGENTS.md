# AGENTS.md — エージェント共通の作業指針

このファイルが Claude Code と Codex の両方が読むマスタ。`CLAUDE.md` はここを `@AGENTS.md` で取り込むだけ。

## まず読むもの

- `docs/workflow.md` — 運用ルール（実行環境・uv の使い方もここ）。
- `exp/findings.md` — 実験をまたいで使う知見。作業前に最初に読む。

## 言語・記法

- ドキュメント、コード内のコメントと docstring、コミットメッセージ、提出メッセージはすべて日本語で書く（技術用語の英語はそのままでよい）。
- 日時はすべて日本時間（JST）で書く。Kaggle など UTC で示された時刻は JST に直して記載する。
- ファイル名は小文字にし、日付を入れない（履歴は git で追う）。`README.md`、`INDEX.md`、`AGENTS.md`、`CLAUDE.md`、`SKILL.md` は固定名として例外。

## スキル（定型作業の手順）

`.agents/skills/<name>/SKILL.md` が実体。`.claude/skills` はそこへのシンボリックリンク。

| スキル | 使うとき |
|---|---|
| new-exp | 新しい実験ディレクトリ `exp/<ID>/` を作る |
| save-knowledge | 実験・調査の結果と知見を `exp/` に記録する（失敗でも必ず） |
| submit-check | Kaggle 提出前のチェック。提出前に必ず実行 |
| public-insights | 公開ノートブックと Discussion の DB 更新・検索・読み取り・要約 |

スキル本文中の `/skill-name` は Claude Code の呼び出し記法。Codex ではそのスキルを使う指示として読む。

nvidia-kaggle プラグイン（Kaggle API 操作のスクリプト群）は Claude Code と Codex のそれぞれに公式の方法でインストールする（手順は `README.md` の「3. エージェント」）。
プラグインの SKILL.md は「スキルのディレクトリで `python scripts/<name>.py` を実行する」と書いているが、このリポジトリでは従わず、必ず `tools/nvkg <name>` で実行する（依存は uv で固定し、出力はリポジトリ直下に置き、提出の確認ルールにかけるため）。

## 安全上の決まり

- `.env` の中身を表示しない。
- `kaggle competitions submit`（`uv run kaggle competitions submit` を含む）と `tools/nvkg submit_kernel` は必ずユーザーの確認を取ってから実行する。
    - submit-check スキルの手順を先に通す。
    - ユーザーに事前に承認を得たならば、提出時に再度承認を取らなくてよい。
- `data/` `input/` は git 管理外。
- 過去の実験の `exp/<ID>/README.md` は書き換えず追記する。

提出の確認と `.env` の読み取り禁止は、`.claude/settings.json`（`ask` / `deny`）と `.codex/rules/default.rules`（「安全上の決まり」の節）の両方で設定している。変えるときは両方を直す。それ以外の許可（`allow`）は各ツールで揃えなくてよい。
