# 提出（Kaggle）の規約

提出前に必ず `/submit-check`（`.claude/skills/submit-check/SKILL.md`）のチェックリストを全通過させる。

## 提出前（共通）

- **提出はユーザーの承認を得てから**（何をいつ出すか）。承認後の提出オペはエージェントが完結してよい。
- 提出制限（回数/日・締切）は `docs/competition/overview.md` を正本とする。
  細かい版を乱発せず、ローカルゲートを通した版だけを出す。
- パラメータは**コード内 CONFIG に記録**する（CLI 引数だけだと git に残らず再現不能）。
- 複数エージェント並走時の二重提出防止: `mkdir <exp>/SUBMIT_LOCK` の成功者だけが提出する。
- 提出前に nvidia-kaggle プラグインの `submission_quota.py` で残りクォータを確認する
  （枠が尽きていれば提出しない。`docs/rules/kaggle-api.md` 参照）。

## 提出形式ごとの手順

コンペの提出形式は `docs/competition/overview.md` で選んだものに従う。

### A. CSV 直接提出（テーブル/画像/NLP 系の多く）

```bash
set -a; source .env; set +a
kaggle competitions submit -c "$KAGGLE_COMPETITION" -f <path>/submission.csv -m "[expNNN] <説明>"
kaggle competitions submissions "$KAGGLE_COMPETITION"   # 受理確認（submit は成功しても無出力）
```

- `tools/verify_submission.py`（要実装）で提出前にフォーマット検証する（列名・行数・欠損など）。

### B. コードコンペ（Notebook をコンペに紐付けて自動実行・採点）

nvidia-kaggle プラグインの `submit_kernel.py` を使う（push → 実行ポーリング → 提出 → 評価ポーリングまで一貫）。
`kernel-metadata.json` の整備、既存提出履歴の確認手順はプラグインの `submission.md`
（`~/.claude/plugins/cache/nvidia-kaggle/.../skills/nvidia-kaggle-skill/submission.md`）を参照。
**このリポジトリ固有のゲート判定**（ローカル CV が基準を満たすか等）は `/submit-check` 側の責務、
push・提出・ポーリングという機械的操作はプラグイン側の責務、と役割を分けて重複させない。

### C. シミュレーション/エージェント提出（kaggle-environments 系）

```bash
kaggle competitions submit -c "$KAGGLE_COMPETITION" -f <path>/main.py -m "[expNNN] <説明>"
```

- 提出物が**公式ランナー**（`kaggle_environments` の該当環境）で最低1試合エラーなく完走するかを、
  ライブラリの `get_last_callable` の仕様（「名前が `agent`」ではなく「最後に定義された callable」を選ぶ実装がある）
  を踏まえて確認する。ファイル結合・層を重ねる構成では末尾に新名のエントリポイント関数を置く。

## 提出後 — スコアは「推移」で判断する

- LB スコアがレーティング制・収束に時間がかかる形式の場合、**一時点のスコアで GO/NO-GO を判断しない**。
  上昇中/下降中の情報が本体（`tools/` に LB スナップショット・推移判定スクリプトを実装して定期実行する）。
- 結果は `docs/knowledge/scores.md` に整理する。
