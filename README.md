# kaggle-competition-template

Kaggle コンペの実験・調査・提出を管理するテンプレート。複製後、以下のチェックリストと「コンペ概要」をコンペごとに記入する。

## 初回セットアップチェックリスト

- [ ] この README のタイトル・コンペ名・公式 URL を記入する
- [ ] `pyproject.toml` の `name` / `description` を変更する
- [ ] `.env.example` を `.env` にコピーし、`KAGGLE_API_TOKEN` / `KAGGLE_COMPETITION` を設定する
- [ ] CPU / GPU と起動方法を選び、コンテナ内で `uv sync` を実行する
- [ ] 必要な依存を `uv add` で追加し、生成した `uv.lock` をコミットする
- [ ] Kaggle のルールに同意し、提供データを `input/` にダウンロードする
- [ ] `docs/overview.md` / `docs/data.md` に公式ページを記録し、下のコンペ概要を埋める
- [ ] `exp/README.md` に担当者と実験 ID の接頭辞を設定する（初期値は `eNNN`）
- [ ] `exp/findings.md` の現状サマリ・評価方針を記入する
- [ ] 使用するエージェントと nvidia-kaggle プラグインをコンテナ内に導入する

## コンペ概要

この節はコンペごとに記入する。参加ルールの正本は Kaggle の公式ページ。

### 基本情報

- コンペ名: （記入）
- 公式 URL: （記入）
- スラッグ: （`.env` の `KAGGLE_COMPETITION` と揃える）
- 日程（すべて日本時間 JST）
  - 開始: （記入）
  - ルール同意・チームマージ期限: （記入）
  - 最終提出期限: （記入）
- 公式ページの原文: [Overview](docs/overview.md)、[Data](docs/data.md)

### タスク・評価

- タスク・予測単位: （記入）
- 評価指標・計算方法・スコアの向き: （記入）
- CV 方針・リーク防止の注意点: （記入。検証後の知見は `exp/findings.md` に記録）

### データ

| ファイル | 内容・主要な列 | サイズ・件数 |
| --- | --- | --- |

提供データは `input/`、共有する前処理済みデータは `data/` に置く。

### 提出

- 提出方式: （Notebook / CSV 等のファイル / エージェントから選び、詳細を記入）
- 提出ファイル名・列・行数・欠損や重複の扱い: （記入）
- 実行制約: （実行時間・CPU/GPU・メモリ・インターネット等を記入）
- 提出回数・リセット時刻（JST）: （記入）
- 最終提出の選択数: （記入）
- LB の性質・採点完了の判断: （記入）

提出前には `submit-check` スキルを使う。操作手順は [運用ルール](docs/workflow.md) の「提出」。

### ルール

- 公式 Rules の URL: （記入）
- 外部データ・事前学習済みモデルの可否と条件: （記入）
- データの利用条件・ライセンス・公開義務: （記入）

## ディレクトリ構成

```text
.
├── exp/                  # 実験
│   ├── README.md         # 実験一覧と提出履歴
│   ├── cv_lb.csv         # 提出ごとの CV と LB
│   ├── findings.md       # 実験をまたぐ知見（作業前に読む）
│   └── <ID>/
│       ├── README.md     # 狙い・仕様・再現手順・結果・考察
│       └── output/       # 実験の出力（git 管理外）
├── docs/
│   ├── workflow.md       # 運用ルールのマスタ
│   ├── overview.md       # Kaggle の Overview 原文
│   └── data.md           # Kaggle の Data 原文
├── reference/            # 公開情報の要約と INDEX.md
├── tools/                # プラグイン実行ラッパー・補助スクリプト
├── input/                # コンペ提供データ（git 管理外）
├── data/                 # DB・共有する生成物（git 管理外）
├── .agents/skills/       # エージェント共通のスキル
├── .claude/skills        # .agents/skills へのシンボリックリンク
├── .codex/               # Codex の設定・実行ルール
├── .devcontainer/        # CPU / GPU の Dev Containers 設定
├── compose.yaml          # CPU の基本設定
├── compose.gpu.yaml      # GPU 用の追加設定
├── .home/                # コンテナのホーム（git 管理外）
├── .env.example          # 環境変数の雛形
├── pyproject.toml        # 共通依存（uv で管理）
├── AGENTS.md             # エージェント共通の指針
└── CLAUDE.md             # AGENTS.md を取り込む
```

## セットアップ

### 1. コンテナ

起動方法は A か B を選び、同じマシンでは混ぜない。切り替えるとコンテナが作り直され、中のユーザーが変わる。

まず `.env` を作り、トークンとコンペのスラッグを記入する。

```bash
cp .env.example .env
```

#### A. Dev Containers

1. VS Code に Dev Containers 拡張機能を入れる。
2. 「Dev Containers: Reopen in Container」で `CPU` か `GPU` を選ぶ。
3. コンテナ内で `uv sync` を実行する。

Notebook のカーネルは `/workspace/.venv/bin/python` を選ぶ。

#### B. docker compose

Linux では `.env` の `UID` / `GID` に `id -u` / `id -g` の値を記入する（Mac・rootless Docker では不要）。GPU を使う場合は `COMPOSE_FILE=compose.yaml:compose.gpu.yaml` のコメントを外す。GPU 利用にはホスト側の NVIDIA ドライバと NVIDIA Container Toolkit が必要。

```bash
docker compose up -d
docker compose exec dev bash
uv sync
```

停止は `docker compose down`。コンテナ外から実行する場合は `docker compose exec dev ...` を使う。VS Code で Notebook を動かす場合は A を使う。

### 2. データと公式ページ

Kaggle のコンペページでルールに同意してから、コンテナ内で実行する。

```bash
uv run kaggle competitions files -c "$KAGGLE_COMPETITION"
uv run kaggle competitions download -c "$KAGGLE_COMPETITION" -p input/
```

ダウンロードした ZIP を `input/` に展開する。nvidia-kaggle プラグイン導入後、公式ページを取得する。

```bash
tools/nvkg tools/fetch_competition_pages.py
```

ページ取得は `docs/overview.md` / `docs/data.md` を置き換える。公式 Rules も別途確認し、この README に日本語の概要を記入する。

### 3. エージェント

使用するエージェントはコンテナ内でインストールし、ログインする。ログイン情報・キャッシュは `.home/` に保持する。

Claude Code の場合:

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude plugin marketplace add https://github.com/NVIDIA/nvidia-kaggle.git
claude plugin install nvidia-kaggle@nvidia-kaggle --scope project
claude
```

`claude` が見つからない場合はコンテナの `~/.local/bin` を PATH に追加する。

Codex は [公式セットアップ手順](https://learn.chatgpt.com/docs/quickstart) に従ってコンテナ内へ導入し、nvidia-kaggle は [プラグインの公式手順](https://github.com/NVIDIA/nvidia-kaggle) に従って導入する。起動は `codex`。

- 共通指針は `AGENTS.md`。Claude Code は `CLAUDE.md` から取り込む。
- スキルの実体は `.agents/skills/`。`.claude/skills` はそこへのリンク。
- プラグインのスクリプトは両エージェントから `tools/nvkg <名前> [引数...]` で実行する。Claude Code 側のプラグインを優先し、なければ Codex 側を使う。
- `.codex/config.toml` はコンテナを隔離の境界としてサンドボックスを外す設定。Codex はこのリポジトリのコンテナ内で起動する。設定項目は [公式の構成リファレンス](https://learn.chatgpt.com/docs/config-file/config-reference) を参照。
- 提出の確認と `.env` の閲覧禁止は `.claude/settings.json` / `.codex/rules/default.rules` の両方で管理する。Codex のコマンド規則は先頭一致であり、すべての閲覧方法を禁止する仕組みではないため、`AGENTS.md` の指針も守る。

## 日常の作業

作業前に `docs/workflow.md` と `exp/findings.md` を読む。新しい実験は `new-exp`、結果の記録は `save-knowledge`、公開情報の調査は `public-insights`、提出前は `submit-check` を使う。失敗した実験も結果と原因を記録する。
