# 運用ルール

このリポジトリの運用ルールのマスタ。スキル（`.agents/skills/`）はここに書いたルールを手早く実行するための手順で、ルールそのものはここに書く。

## 実行環境

- 作業はすべて Docker コンテナの中で行う。エージェントもコンテナ内で起動する（入り方は `README.md` の「セットアップ」）
- コンテナの外から実行するときは `docker compose exec dev ...`
- 依存は uv で管理する。追加は `uv add`、Python の実行は `uv run ...`。`pip` を直接使わない
- Notebook 提出の場合は Kaggle 上で動くので、ライブラリ・実行時間・GPU・インターネットの条件をコンペに合わせる

## Kaggle API

- kaggle CLI は `uv run kaggle`、nvidia-kaggle プラグインのスクリプトは `tools/nvkg` で実行する
- 認証は `.env` の `KAGGLE_API_TOKEN` だけを使う（`~/.kaggle/kaggle.json` は作らない）

## 実験

- 1 実験 = 1 ディレクトリ（`exp/<ID>/`。命名は `exp/README.md`）。既存ディレクトリの流用は、パラメータを 1 つ変えるだけの再測定に限る
- `exp/<ID>/README.md` に狙い・仕様・再現手順・結果・考察を書く
- 再現可能なスクリプトで実装する。パラメータはコード内の CONFIG に書く（CLI 引数だけだと git に残らない）
- 予測結果・モデル重み・ログなどの出力は `exp/<ID>/output/`（git 管理外）に置く

## ファイルの置き場

生成物は種類で置き場を分ける。どれも git 管理外。

| 置き場 | 置くもの |
| --- | --- |
| `input/` | コンペの提供データだけ |
| `exp/<ID>/output/` | その実験の出力（予測結果・モデル重み・ログ・特徴量など） |
| `data/` | 上のどちらにも当てはまらない生成物（プラグインの DB、複数の実験で共有する前処理済みデータなど） |

## 知見の記録

記録先は役割ごとに分かれている。1 つのファイルに書き連ねない。失敗した実験も記録する。

| 記録先 | 何を書くか | 更新のしかた |
| --- | --- | --- |
| `exp/<ID>/README.md` | 実験 1 件の記録 | 「結果」「考察」を追記。過去の内容は書き換えず、訂正は追記で示す |
| `exp/README.md` | 実験の一覧と提出履歴 | 表に 1 行追記・更新。結論は「何をして何が分かったか」を数値込みで書く |
| `exp/cv_lb.csv` | 提出ごとの CV と LB（可視化用） | 提出ごとに 1 行追記。列は `date,id,cv,lb,note`（`date` は JST の `YYYY-MM-DD HH:MM`） |
| `exp/findings.md` | 実験をまたいで使う知見と現状のまとめ | 該当する節を最新の内容に更新 |
| `reference/` | 公開ノートブック・Discussion の要約 | 「公開情報の活用」を参照 |

実験の記録には最低限次を残す。

- 結果（数値）と、それをどう判断したか
- なぜその結果になったか（結果だけだと同じ提案を繰り返す）
- 再現手順（コマンド・CONFIG・使用データ）

書き方の注意:

- 仮説は仮説と明記し、確認済みの事実と区別する
- 「そのアイデアがだめ」なのか「その実装がだめ」なのかを区別する
- 事前に立てた仮説の検証と、結果を見てから立てた仮説の探索を区別する
- エージェントのメモリに知見を書かない。マスタはリポジトリ内のファイル

## 公開情報の活用

- 公開ノートブック・Discussion は nvidia-kaggle プラグインの DB（`data/`、git 管理外）に取り込み、要約だけを `reference/` に置く
  - Discussion は本文とコメントまで DB に入る
  - ノートブックは DB にメタ情報（タイトル・著者・票数など）だけが入り、コードは読むときにダウンロードされる（`data/notebooks/`）
- 何を読んだか・どう判断したかは `reference/INDEX.md` で管理する（DB は知らない）
- 読むときは次を確かめ、要約に書く
  - 主張の根拠は何か（LB の実測 / ローカルの実測 / コード公開の有無）。憶測と区別する
  - 外部データや事前学習済みモデルに依存していないか。依存しているならコンペのルール上問題ないか
  - 見えているコードと、実際にスコアを出した実体が同じか（外部からロードしたものが本体のことがある）
  - public LB にしか効かないリークやハックが混ざっていないか
  - こちらで試したことがあるか（`exp/findings.md`）
- 公開コードをそのまま提出しない。アイデアは自分で実装し、出典を `exp/findings.md` に書く

## git

- 実験単位でコミットする。
- コミットメッセージは `<接頭辞>: 概要` の形式にし、`[]` で囲まない。接頭辞は実験なら `<ID>`（例: `e001: 学習率を下げる`）、docs だけの変更は `docs`、環境の変更は `env`
- 大きなファイル（モデル重み・データ・特徴量）はコミットしない。置き場は「ファイルの置き場」に従う

## 提出

提出回数には上限がある（回数とリセット時刻は `README.md` の「コンペ概要」の「提出」）。

### 提出前に確かめること

- ユーザーの承認を得ている（何を、どの提出枠で出すか）。承認後の操作はエージェントが行ってよい
- 残り回数がある（`tools/nvkg submission_quota "$KAGGLE_COMPETITION"`）
- 提出物がローカルでエラーなく最後まで動き、出力がコンペの提出形式に合っている
- CV またはローカル評価が、実験開始時に決めた基準を満たしている
- 同じ実験・同じメッセージの提出がまだ無い（`uv run kaggle competitions submissions "$KAGGLE_COMPETITION"`）
- Notebook 提出の場合は `exp/<ID>/kernel-metadata.json` が次のとおりになっている
  - `id` が自分のアカウントの `<user>/<slug>`（公開ノートブックを取り込んだままだと他人の ID になっている）
  - `is_private` が `true`（`false` だとコードが公開される）
  - `enable_internet`・GPU 等がコンペの実行条件に合い、`competition_sources` にコンペのスラッグがある

### 提出のしかた

提出形式・ファイル名・実行制約は `README.md` の「コンペ概要」の「提出」でコンペごとに定める。下のコマンドの `<...>` を実際の値に置き換える。

#### Notebook 提出

kaggle CLI で打つ。結果が出るまで待つ必要はなく、採点結果は Kaggle のサイトで確認する（プラグインの `submit_kernel` は結果が出るまで待ち続けるので使わない）。

```bash
uv run kaggle kernels push -p exp/<ID>                  # 新しい版を作り、Kaggle 上で実行する
uv run kaggle kernels status <user>/<slug>              # 実行が終わったか確認する（サイトで見てもよい）
uv run kaggle competitions submit "$KAGGLE_COMPETITION" -k <user>/<slug> -v <版番号> -f <提出ファイル名> -m "<ID>: <説明>"
uv run kaggle competitions submissions "$KAGGLE_COMPETITION"   # 受理されたか確認する
```

#### ファイル提出（CSV・エージェント等）

提出ファイルをローカルで検証してから実行する。エージェント提出では公式ランナーによる動作確認も行う。

```bash
uv run kaggle competitions submit "$KAGGLE_COMPETITION" -f exp/<ID>/output/<提出ファイル> -m "<ID>: <説明>"
uv run kaggle competitions submissions "$KAGGLE_COMPETITION"
```

#### 提出後

- 提出メッセージは `<ID>: <説明>` の形式にし、説明は日本語で端的に書く
- `competitions submit` は成功しても何も出力しない。出力がなくても再実行せず、`competitions submissions` で受理を確かめる
- 結果が出たら「知見の記録」の表に従って記録する（`exp/README.md` の提出履歴、`exp/cv_lb.csv`、`exp/<ID>/README.md`）
