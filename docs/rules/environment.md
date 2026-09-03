# 実行環境

- 実行環境は 2 系統。**どちらも環境の正本は `uv.lock`**:
  - **Windows ローカル**: PowerShell + uv 直（Docker 不使用）。CPU のみを想定。
  - **研究室共有 Linux サーバー**: Docker（`docker compose up -d --build` → `docker exec -it kaggle-dev1 bash`）。
    `HOST_UID` / `HOST_GID` は `.env` に置く（`.env.example` 参照）。
- **イメージとコンテナの命名**: イメージ `kaggle-dev:latest` は uv 公式イメージをそのまま落とし込んだもので、
  リポジトリ横断で共用してよい（compose の `dockerfile_inline` が FROM のみ。ツール追加が要るときだけ RUN を足す）。
  コンテナはリポジトリごとに1つ、`kaggle-dev1`, `kaggle-dev2`, ... と番号を振る。
- **開発フロー（サーバー）**: 編集・git・Claude Code は**ホスト側**で行い、Python / uv / kaggle CLI の実行は
  `docker exec kaggle-dev1 ...` でコンテナに送る（リポジトリは bind mount なので編集は即反映される）。
  長時間学習は**ホストの tmux** 内で `docker exec -it kaggle-dev1 bash` して手動実行 + tee
  （エージェント起動プロセスは環境により ~600秒で kill されることがある）。
- **GPU 学習（torch 等）が必要なら**サーバーの Docker コンテナ内で行う（nvidia ランタイム有効時）。
  torch は CUDA 同梱 wheel でそのまま GPU が効き、リビルド不要（ベースイメージに CUDA toolkit は不要。
  lock 外ビルドが要る特殊ケースは避ける）。GPU 不要なコンペでは `docker-compose.yml` の
  `runtime: nvidia` / `NVIDIA_*` を削除してよい。
  Windows ローカルは CPU のみ想定（軽い開発・分析用）。
- **Docker は Linux 前提・named volume は使わない**。`.venv` もキャッシュ（`XDG_CACHE_HOME=/workspace/.cache`）も
  bind mount（`.:/workspace`）上に置く。compose の `user: HOST_UID:HOST_GID` により生成物の所有権はホストと一致し、
  venv と cache が同一マウントなので uv のハードリンク展開も効く。
  - **Windows ホストでは Docker を使わない**（uv 直）。Linux と Windows で `.venv` を共有すると
    `uv sync` が壊れる。クローンがマシンごとに別なら問題にならない。
- **環境の再現手順は常に `docker compose up` → `uv sync` だけ**で済む状態を維持する。
  lock 外の手作りインストールはしない。
- 依存: `kaggle`（CLI）、`pandas`、`jupyterlab` が既定。追加はコンペの必要に応じて `uv add` で行い lock をコミットする
  （例: 学習系なら `torch` / `lightgbm`、シミュレーションコンペなら `kaggle-environments` 等）。
- コードコンペ（推論ノートブック提出）の場合、提出コードは Kaggle サンドボックスで実行される点に注意
  （使えるライブラリ・実行時間・GPU 有無の制約を Kaggle の Notebook 設定と一致させる）。
