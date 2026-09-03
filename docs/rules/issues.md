# Issue 運用（実験トラッキング）

実験の進行管理・結果閲覧を GitHub Issues で行う。
**知見の正本は本リポジトリの docs/**。Issue はリアルタイムの作業ログ・閲覧ビューであり、
docs/experiments/ 以下は整理済みの最終記録として役割が分かれる — 同じ内容を2か所に清書する二重管理はしない。

- リポジトリ: `<owner>/<repo>`（テンプレート複製時に記入）
- **1実験 = 1 Issue**。タイトルは `[expNNN] <タイトル>`（コミット prefix と同一形式）
- 操作は `gh` CLI（認証済み）

## 役割分担（責務境界）

| 場所 | 役割 | 内容 |
|---|---|---|
| GitHub Issue | 進行管理・閲覧ビュー | 仮説・事前登録ゲート（body）／中間結果・図（コメント）／最終結果コメント／判定ラベル |
| `docs/experiments/` + findings/scores/INDEX | **知見の正本**（毎セッション読む） | `/save-knowledge` で整理して記録 |
| `exp/expNNN/NOTES.md` | コード隣の再現記録（オフラインでも読める） | 仕様・パラメータ所在・uv run コマンド列のみ（最小化） |

## ライフサイクル

1. **開始**（`/new-exp` の一部）: Issue を作成。body に仮説・**事前登録ゲート**・仕様骨子を書く。
   ```bash
   gh issue create --title "[expNNN] <タイトル>" --body-file <(cat <<'EOF'
   ## 仮説・狙い
   （何を検証するか。関連過去実験: docs/experiments/expXXX_*.md）

   ## 事前登録ゲート
   （GO/NO-GO の数値基準。**body に書いた時点が正** — 事後変更は body を黙って書き換えず、理由をコメントに明記する。編集履歴で検証可能）

   ## 仕様
   （データ・手法・パラメータ骨子）
   EOF
   )
   ```
2. **進行中**: 中間結果を `gh issue comment N --body "..."` で追記。図は git 管理内の小さい PNG（`exp/expNNN/figs/`）をコミットし blob URL をコメントに貼る（gh CLI からの画像直接アップロードは不可。ブラウザからのドラッグ&ドロップは可）。
3. **コミット連携**: コミットメッセージに `(#N)` を含める（例: `[expNNN] 概要（数値） (#N)`）→ Issue のタイムラインに自動リンク。
4. **終了**（`/save-knowledge` の一部）: 最終結果コメント（判定・主要数値・原因の要約 + `docs/experiments/expNNN_*.md` へのリンク）→ 判定ラベルを付けて close。RED/NO-GO でも必ず close まで行う（open のまま放置しない）。

## ラベル（判定 — INDEX.md の語彙と同一）

| ラベル | 色 | 意味 |
|---|---|---|
| `GO` | 緑 `0e8a16` | 採用・改善・整備完了 |
| `NO-GO` | 橙 `d93f0b` | 事前登録ゲート不通過（原因記録済み） |
| `RED` | 赤 `b60205` | 手法/アイデアの棄却（再挑戦条件は docs 側に記録） |
| `調査` | 黄 `fbca04` | 実験でない調査・計測 |

close 時に必ず1つ付ける。

## 初回セットアップ（認証後に1回）

```bash
gh auth login   # ユーザー操作（ブラウザ or トークン）
gh label create GO --color 0e8a16 --description "採用・改善"
gh label create NO-GO --color d93f0b --description "事前登録ゲート不通過"
gh label create RED --color b60205 --description "手法/アイデアの棄却"
gh label create 調査 --color fbca04 --description "実験でない調査・計測"
```

## 注意

- Issue のコメントは生ログであり知見の記録完了ではない。**docs（experiments/ + INDEX + findings/scores）へ整理して初めて記録完了**（`/save-knowledge`）。エージェントの過去知見の読み込みも docs 側から行う（Issue の全読みはしない）。
- GitHub にアクセスできない環境でも、再現手順（NOTES.md）と知見（docs/）だけで実験を継承できる状態を保つ。
