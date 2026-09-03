---
name: summarize-discussion
description: 取得済み（reference/discussions/raw/ にある）Kaggle Discussion を精読し、要約を reference/discussions/summary/ に作成して INDEX を更新する。/kaggle-discussion-pull の後続、または既に raw があるトピックを後から要約するときに使う。
---

# Discussion の要約

対象の raw（`reference/discussions/raw/<topic-id>.md`）を精読し、知見をコミット対象の要約に落とす。

## Step 1: 精読の観点

1. **検証可能な主張か、憶測か**を区別する（主張の根拠: LB実測 / ローカル実測 / コード公開の有無）
2. `docs/experiments/INDEX.md`・`docs/knowledge/findings.md` §7（負の結果）と照合:
   - 我々の実測と一致する外部報告 → 信頼度の裏付けとして記録
   - 我々の RED と矛盾する報告 → 手法差を特定してから判断（「手法の RED」vs「アイデアの RED」）
3. リーク・public LB 専用テクの匂いは明示的にフラグする

## Step 2: 要約の作成

`reference/discussions/summary/<topic-id>_<slug>.md` に作成:

```markdown
# #<topic-id> <タイトル>（<著者>, 取得日 YYYY-MM-DD）

## 主張の要点
## 根拠の強さ（LB実測 / ローカル実測 / コード有無）
## 我々への含意（既検証との照合・新規レバーか）
## raw の場所
reference/discussions/raw/<topic-id>.md
```

## Step 3: INDEX 更新

`reference/INDEX.md` の Discussion 表に1行追記（**我々への含意を必ず書く**）。
