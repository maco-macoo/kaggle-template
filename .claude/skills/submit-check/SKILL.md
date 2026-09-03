---
name: submit-check
description: Kaggle 提出前のゲートチェックリストを実行する。提出（kaggle competitions submit 等）を行う前に必ず使う。docs/rules/submission.md・kaggle-api.md の規約を実行可能な手順として固定したもの。
---

# 提出前ゲート

提出枠は**貴重資源**（回数・リセット時刻は `docs/competition/overview.md`）。以下を上から順に全て確認し、
1つでも NO なら提出せずユーザーに報告する。

このスキルは**ゲート判定・チェックリストという解釈作業**を担当する。機械的な操作
（クォータ確認・提出履歴の照会・コードコンペのカーネル push/poll）は nvidia-kaggle プラグインの
スクリプトに委譲し、ここで再実装しない（重複させない — `docs/rules/kaggle-api.md`）。

## Step 1: 提出の正当性

- [ ] **ユーザーの承認済みか**（何をどの枠で出すか。承認後のオペはエージェント完結でよい）
- [ ] 較正目的なら**1ノブだけ**変えているか
  （結果の解釈時の注意: 単発のスコア差がノイズ床未満なら改善の証拠にならない — ノイズ床の実測値は findings.md）
- [ ] 提出物が**意図した版か**を識別できるか（ログ内マーカー・バージョン表記・md5 等で前版と区別する）
- [ ] 単発の極端な好値を確定扱いしていないか（追試で検証する計画か）

## Step 2: 提出クォータの確認（機械的操作 → プラグインに委譲）

```bash
NVKG=$(ls -d ~/.claude/plugins/cache/nvidia-kaggle/nvidia-kaggle/*/skills/nvidia-kaggle-skill/scripts | head -1)
.venv/bin/python "$NVKG/submission_quota.py" "$KAGGLE_COMPETITION"
```

- `exhausted: true` なら提出しない。
- 過去の提出試行・評価結果はローカルログで確認できる（提出方法によらず有効。詳細は `docs/rules/kaggle-api.md`）:
  ```bash
  .venv/bin/python "$NVKG/submission_history.py" "$KAGGLE_COMPETITION"
  ```
  「前回の実行が成功したか不明」な状態で再実行しない — ログを読んでから判断する。

## Step 3: ローカル検証（提出物の健全性）

提出形式ごとの検証項目は `docs/competition/overview.md` を正本とする。共通の最低ライン:

- [ ] 提出物がローカルで**エラーなく最後まで実行できる**ことを確認したか
- [ ] CV / ローカル評価が事前登録したゲート基準を満たしているか（`docs/rules/experiment.md`）
- [ ] **CSV 提出**: `tools/verify_submission.py` で形式検証したか（列名・行数・欠損など）
- [ ] **コードコンペ**: Notebook が Kaggle の実行制約（時間・GPU・インターネット無効化）内で完走するか。
      push・提出・評価ポーリングはプラグインの `submit_kernel.py` を使う（`docs/rules/submission.md` B）
- [ ] **シミュレーション/エージェント提出**: 公式ランナーで最低1試合エラーなく完走するか。
      エントリポイント解決の仕様（例: 「名前が特定でなく最後に定義された callable を拾う」実装）を
      踏まえ、複数関数を定義する構成ではファイル末尾に新名ラッパを置いているか

## Step 4: 排他制御

- [ ] `mkdir <exp>/SUBMIT_LOCK` に成功したか（複数エージェント並走時の二重提出防止。
  提出完了ごとに `SUBMIT_LOCK/done_*` を touch）

## Step 5: 提出コマンド

`docs/rules/submission.md` の該当する提出形式（A: CSV / B: コードコンペ / C: シミュレーション）に従う。

- [ ] 認証前置をしているか（`docs/rules/kaggle-api.md`）:
  ```bash
  set -a; source .env; set +a   # KAGGLE_API_TOKEN・KAGGLE_COMPETITION は .env に定義
  ```
- [ ] 提出直後に `kaggle competitions submissions "$KAGGLE_COMPETITION"` で**受理を確認**したか
  （成功時に無出力の罠 — 無出力でも再実行しない）

## Step 6: 提出後

- 結果判明後、`docs/knowledge/scores.md` と該当 exp の NOTES.md に結果を記録し、`/save-knowledge` で知見を残す。
- 結果が退行でも**必ずコミット**する（docs/rules/git.md）。
