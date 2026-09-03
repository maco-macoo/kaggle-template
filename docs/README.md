# docs/ — ドキュメント索引

> 本リポジトリのドキュメントはすべて**日本語**で書く（技術用語の英語はそのままでよい）。
> 新しい知見が出たら `/save-knowledge` の手順で記録する（規約: `rules/knowledge.md`）。
> このテンプレートを複製したら、この行をコンペ名・開始日で書き換える
> （例:「2026-XX-XX に <コンペ名> 用に初期化した」）。

| ディレクトリ | 役割 | 更新タイミング |
|---|---|---|
| [competition/](competition/overview.md) | **コンペ仕様**（overview.md=競技概要・評価方式・提出形式。ルール正典は Kaggle 公式ページ／同梱の README・AGENTS.md 等） | 基本固定 |
| [rules/](rules/README.md) | **運用ルール**（カテゴリ別: 実験・知見・提出・環境・外部資産・Kaggle API・git） | ルール追加時 |
| [knowledge/](knowledge/findings.md) | **恒久ナレッジ**（findings.md=知見・原因・教訓の恒久サマリ §0〜・**最初に読む** / scores.md=LB スコア推移） | 知見・提出のたび |
| [experiments/](experiments/INDEX.md) | **実験ごとの詳細ログ**（1実験1ファイル。索引は INDEX.md。過去ファイルは書き換えず追記） | 実験のたび |

## ファイル命名規約

- docs/ 配下は**カテゴリ別サブディレクトリ + 小文字ファイル名**（`rules/submission.md` 等）。
  索引ファイルのみ大文字固定名（`README.md` / `INDEX.md`）。
- **日付をファイル名に入れない**。ファイルは常に「最新の内容」を保持し、履歴は git で追う。日付は本文の見出しに書く。
- リポジトリ直下の `README.md`、実験ディレクトリの `NOTES.md` はツール・慣習上の固定名。
- コードファイルは小文字 snake_case（`lb_snapshot.py` 等）。

## エージェントメモリについて

Claude Code の自動メモリ（`~/.claude/projects/<slug>/memory/`）は環境ローカルの補助であり、
**知見・ルールの正本は常に本リポジトリの docs/**。
メモリには docs への薄いポインタ以上の知見を溜めない（`rules/knowledge.md`）。

## 関連（docs 外）

- Kaggle 公式のコンペページ・（配布があれば）同梱のルール/データ説明ファイルが**競技ルールの正典**。
- `.claude/skills/` — 定型作業の実行手順（new-exp / submit-check / save-knowledge / kaggle-notebook-pull / summarize-notebook / kaggle-discussion-pull / summarize-discussion）。
- `reference/` — 公開ノートブック・Discussion の要約と raw（索引 `reference/INDEX.md`）
- `tools/` — LB追跡・提出検証・ローカル評価などのスクリプト群（コンペごとに実装）
- `data/`（git 管理外） — 収集した LB 履歴・特徴量・nvidia-kaggle プラグインの DB（`data/*.db`）
- 各 `exp/expNNN/NOTES.md` — 実験ごとの仕様・再現手順
