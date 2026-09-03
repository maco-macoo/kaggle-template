# 外部資産（公開ノートブック・公開コード）の扱い

- **調査は積極的に行う**: 公開ノートブック・Discussion・（あれば）他チームのリプレイ等は
  `/kaggle-notebook-pull`・`/kaggle-discussion-pull` で収集し、raw を `reference/{notebooks,discussions}/raw/`、
  要約を `summary/` に置く（索引 `reference/INDEX.md`）。
- **公開コードのそのまま提出は NG**（コンペ規約以前に学びがない）。
  アイデア・パラメータ・手法は分析して自前実装に取り込む（出典を findings.md に記録）。
- 外部データ・事前学習済みモデルを使う場合は、コンペルール上許可されているか
  （External Data ルール・ライセンス）を確認してから使う。
- 大物（重み・リプレイ等）は `data/` に置き git にコミットしない。
