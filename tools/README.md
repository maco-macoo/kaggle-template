# tools/ — 補助スクリプト

コンテナの中のリポジトリ直下で実行する。

| ファイル | 役割 |
| --- | --- |
| `nvkg` | nvidia-kaggle プラグインのスクリプトを実行する（`tools/nvkg <スクリプト名> [引数...]`）。プラグインの場所をここで解決するので、スキルはプラグインのパスを知らなくてよい |
| `fetch_competition_pages.py` | Kaggle のコンペページを `docs/overview.md` と `docs/data.md` に書き出す（`tools/nvkg tools/fetch_competition_pages.py`） |

- コンペごとに必要になったスクリプトはここに追加し、この表に 1 行書く
- 出力するデータは `data/`（git 管理外）に置く
- 大量に取得するスクリプトには待ち時間と上限を付け、レート制限を守る
