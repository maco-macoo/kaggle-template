---
name: new-exp
description: 新しい実験ディレクトリ exp/expNNN/ を docs/rules/ 準拠で作成する。新しい構造・新しい狙いの実験を始めるときに使う（既存ディレクトリの流用は「同一レシピの単一ノブ違い」のみ可）。
---

# 新規実験の開始

`docs/rules/experiment.md` に従い、1実験=1ディレクトリで実験を開始する。

## 手順

### Step 1: 事前読み込み（必須）

1. `docs/knowledge/findings.md` §0（現状サマリ）— 現ベスト・枯渇済みレバー・残レバーを確認
2. `docs/experiments/INDEX.md` — 同系統の過去実験があれば該当ファイルを読む（**同じ提案のループ防止**。
   RED/NO-GO 済みのアイデアは、過去の原因を踏まえた新規性がない限り再挑戦しない）
3. `docs/rules/README.md`（索引）と関連ルール（experiment / submission / knowledge）

### Step 2: 番号採番と Issue 作成

- `exp/` 配下の最大 expNNN + 1 を採番
- **GitHub Issue を作成する**（`docs/rules/issues.md`。1実験=1Issue）:

```bash
gh issue create --title "[expNNN] <タイトル>" --body "$(cat <<'EOF'
## 仮説・狙い
（何を検証するか。関連する過去実験: docs/experiments/expXXX_*.md）

## 事前登録ゲート
（GO/NO-GO の判定基準を実験前に数値で決める。
 事後の基準変更は禁止 — 小標本の好結果は full 母集団で霧散する前例多数。
 変更せざるを得ない場合は body を黙って書き換えず、コメントで理由を明記）

## 仕様
（データ・手法・パラメータ骨子。パラメータはコード内 CONFIG に記録 — CLI 引数だけだと再現不能）
EOF
)"
```

### Step 3: ディレクトリ作成

`exp/expNNN/` を作成し、`NOTES.md` を以下の**最小骨子**で作る
（仮説・ゲート・進行・結果は Issue と docs/experiments/ 側 — NOTES.md には書かない）:

```markdown
# expNNN: <タイトル>（Issue #N）

## 仕様
（データ・手法・パラメータの所在）

## 再現手順
（uv run コマンド列）
```

### Step 4: 実装時の注意

- コンペデータは `data/` または `input/` に置く（`docs/competition/overview.md` のパス規約に従う）。
  ローカルと Kaggle 環境でパスが異なる場合は両対応で書く:
  ```python
  from pathlib import Path
  INPUT_DIR = Path(f"/kaggle/input/<comp-slug>") if Path("/kaggle").exists() else Path("data")
  ```
- 中間チェックポイントは残さない（docs/rules/experiment.md）。大物バイナリは git にコミットしない。
- 検証は leak-free を原則とし、評価プロトコル（分割・評価指標など）を CONFIG に固定して比較可能にする。
- 中間結果・図は `gh issue comment N` で Issue に追記（進行ログ。`docs/rules/issues.md`）。
  コミットメッセージには `(#N)` を含める。

### Step 5: 実験終了時

`/save-knowledge` を実行して知見を記録する（結果が RED/NO-GO でも必ず記録）。
Issue の結果コメント・判定ラベル・close も `/save-knowledge` の手順に含まれる。
