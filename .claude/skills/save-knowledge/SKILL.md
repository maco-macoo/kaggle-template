---
name: save-knowledge
description: 実験・調査で得た知見を所定の場所（docs/experiments/ + INDEX + FINDINGS §0-8 + SCORES）に記録する。実験の結果（GO/NO-GO/RED いずれも）が出たとき、または再利用価値のある知見が会話・調査から出たときに使う。
---

# 知見の保存

知見の置き場は役割で分かれている。**1つの巨大ファイルに書き連ねない**。

| 置き場 | 役割 | 更新方法 |
|---|---|---|
| `docs/experiments/expNNN_<slug>.md` | 実験の詳細ログ（1実験1ファイル） | 新規作成。過去ファイルは書き換えない（訂正は新知見として追記） |
| `docs/experiments/INDEX.md` | 実験の索引テーブル | 1行追記（Exp/日付/1行結論/結果/リンク） |
| `docs/knowledge/findings.md` §0〜§8 | 恒久サマリ（毎セッション読む） | 常に最新化。現状サマリ・What works・負の結果表・教訓 |
| `docs/knowledge/scores.md` | スコア時系列 | 提出・評価の結果が出たら追記 |

## 手順

### Step 1: 実験ログの作成（実験の場合）

`docs/experiments/expNNN_<slug>.md` を作成。含めるべき内容:
- **結果**（数値表）と **判定**（GO / NO-GO / RED / 調査）
- **原因・機構**（なぜその結果になったか — 結果だけ書かない。同じ提案のループを防ぐのは原因の記録）
- **教訓**（方法論として一般化できるもの）
- **再現手順**（コマンド・CONFIG・使用データ）
- 事前登録ゲートと実測の対比（ゲートを事後に動かした場合はその旨を明記）

### Step 2: INDEX.md へ1行追記

`docs/experiments/INDEX.md` のテーブル末尾に追加。1行結論は「何をして何が分かったか」を数値込みで。
リンク列には docs ファイルに加えて Issue へのリンク（`#N`）も併記。

### Step 3: FINDINGS.md 恒久サマリの更新（該当する場合のみ）

- ベスト更新・方針転換 → §0 現状サマリ
- 再挑戦しない負の結果 → §7 の表に追加
- 一般化できる方法論 → §5/§4 教訓
- レバーの開閉 → §6 未着手の有望方向

### Step 4: Issue の close（実験の場合）

`docs/rules/issues.md` に従い、実験の Issue を閉じる:

```bash
gh issue comment N --body "判定・主要数値・原因の要約（詳細: docs/experiments/expNNN_<slug>.md）"
gh issue edit N --add-label "GO|NO-GO|RED|調査"   # INDEX.md の判定と同一のものを1つ
gh issue close N
```

RED/NO-GO でも必ず close する（open 放置しない）。Issue コメントは生ログであり、
docs への整理（Step 1〜3）が完了して初めて知見の記録完了。

### Step 5: その他

- 提出・評価のスコアが出た → `docs/knowledge/scores.md`
- エージェント固有メモリには知見を書かない（docs が正本。メモリは docs への薄いポインタのみ）
- コミット: `[expNNN] 概要（数値）` 形式。docs のみなら `[docs]`。**失敗・退行もコミット**する。

## 注意

- 仮説は仮説と明記する（確定した機構と区別する）
- 「そのアイデアの RED」か「その手法の RED」かを区別して書く
  （あるアイデアが特定の実装で失敗しても、別の実装では有効なことがある。棄却の範囲を明確に）
- **検証（事前登録した仮説の確認）と探索（結果を見てから立てた仮説）を区別して書く**
  （探索から得た所見を検証済みの結論として書かない — HARKing の防止）
