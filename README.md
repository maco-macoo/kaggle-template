# kaggle-competition-template

[Kaggle] <コンペ名を記入>

このリポジトリは Kaggle コンペ用のセットアップテンプレート。新しいコンペを始めるときにこのリポジトリを
複製し、`<...>` で示した箇所（コンペ名・スラッグ・チーム情報・リポジトリ名等）を埋めてから使う。

## 初回セットアップチェックリスト

- [ ] `docker-compose.yml` の `name` / `container_name` を `sato-dev1` から一意な名前に変更
- [ ] `pyproject.toml` の `name` / `description` を記入
- [ ] `.env.example` → `.env` にコピーし、`KAGGLE_API_TOKEN` / `KAGGLE_COMPETITION` 等を記入
- [ ] `docs/competition/overview.md` にコンペ概要・評価指標・提出形式を記入（`docs/rules/submission.md` の分岐もコンペ種別に合わせて選ぶ）
- [ ] `docs/rules/issues.md` の GitHub リポジトリ名を記入し、`gh label create` でラベルを作成
- [ ] `docs/README.md` の日付・注記を更新
- [ ] GPU 不要なコンペなら `docker-compose.yml` の `runtime: nvidia` 等 GPU 関連設定を削除

## セットアップ

### 1. Docker 環境（Linux サーバー。Windows ローカルは uv 直でこの節は不要）

構成は `docker-compose.yml` 1 ファイル（uv 公式イメージを `sato-dev:latest` としてほぼ素のまま使う）。
マシン差分（`HOST_UID` / `HOST_GID`）は `.env`（git 管理外）に寄せる。

```bash
cp .env.example .env    # KAGGLE_API_TOKEN 等と HOST_UID/HOST_GID を記入（雛形にコメントで例あり）

docker compose up -d --build     # --build は初回と compose の FROM/RUN 変更時のみ
docker exec -it sato-dev1 bash # コンテナに入る場合。ホストから docker exec sato-dev1 <cmd> でも可
```

- 2 回目以降は `docker compose up -d` だけで OK。停止は `docker compose down`。
- `.venv` とキャッシュは bind mount 上にあり、コンテナを再作成しても消えない。
- 編集・git・Claude Code はホスト側、実行はコンテナ側。

### 2. Python 環境（コンテナ内）

```bash
uv sync
```

### 3. nvidia-kaggle プラグイン（Kaggle Discussion・公開ノートブックの調査に使用）

`kaggle-discussion-pull` / `kaggle-notebook-pull` skill は nvidia-kaggle プラグインの索引・検索スクリプトに
委譲する。プラグインが未導入ならインストールしておく（詳細は `docs/rules/kaggle-api.md`）。

## ドキュメント

- 運用ルール: `docs/rules/`（実行環境の詳細は `docs/rules/environment.md`）
- ドキュメント索引: `docs/README.md`
