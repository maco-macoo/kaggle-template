# 知見の記録ルール

実験の**結果・原因・教訓**が出たら `/save-knowledge`（`.claude/skills/save-knowledge/SKILL.md`）の手順で記録する。

## 置き場の役割分担

| 置き場 | 役割 |
|---|---|
| `docs/experiments/expNNN_<slug>.md` + `INDEX.md` | 実験の詳細ログ（1実験1ファイル・新規作成、INDEX に1行追記）。過去ファイルは書き換えない（訂正は新知見として追記） |
| `docs/knowledge/findings.md` §0〜§8 | 恒久的な教訓・機構・現状サマリ（常に最新化） |
| `docs/knowledge/scores.md` | LB / CV スコアの時系列 |
| `reference/{notebooks,discussions}/summary/` + `reference/INDEX.md` | 公開ノートブック・Discussion の要約 |

## 原則

- **エージェント固有メモリに知見を残さない**（どのエージェント・どの環境からでも継承できるように、正本は必ず上記の docs/ 側へ書く）。
  メモリは docs への薄いポインタとセッション間の作業状態のみ。
- 結果だけでなく**原因・機構**を書く（同じ提案のループを防ぐのは原因の記録）。
- 仮説は仮説と明記する。「アイデアの RED」と「手法の RED」を区別する。
- **検証（事前登録した仮説の確認）と探索（結果を見てから仮説を立てる調査）を区別して書く**。
  探索から得た所見を検証済みの結論として書かない（HARKing の防止）。
