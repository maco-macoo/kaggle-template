# tools/ — 収集・分析・評価スクリプト

すべて `uv run python tools/<script>.py` で実行。出力データは `data/`（git 管理外）。

`kag_common.py` はどのコンペでも使う共通基盤（kaggle CLI subprocess ラッパー・チーム識別）を用意した雛形。
それ以外はコンペ種別に応じて実装する。以下は典型的な構成の例（不要なものは作らない）:

| スクリプト（例） | 役割 |
|---|---|
| `kag_common.py` | kaggle CLI subprocess ラッパー・パス定数・自チーム識別（テンプレートに雛形あり） |
| `verify_submission.py` | 提出前のフォーマット検証（CSV の列名・行数・欠損など） |
| `lb_snapshot.py` | LB のスナップショット保存 + `data/lb_history.csv` 追記 |
| `score_trajectory.py` | LB 履歴からスコア推移・{上昇/安定/下降} 判定レポート |
| `eval.py` | ローカル評価ハーネス（固定 seed・固定分割。事前登録ゲートの判定機構） |

大量取得系のスクリプトは礼儀正しく（スリープ・上限つき）実装し、レートリミットを守る。
