"""コンペ横断で使う共通基盤: kaggle CLI サブプロセスラッパー・パス定数・自チーム識別。

使い方の例:
    from kag_common import run_kaggle, OUR_TEAM_ID, OUR_TEAM_NAME

    result = run_kaggle(["competitions", "submissions", COMPETITION], as_json=True)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

COMPETITION = os.environ.get("KAGGLE_COMPETITION", "")
# 自チーム識別子。文字列一致（チーム名）だけで別チームを誤認するリスクがあるため、
# 使う前に `kaggle competitions team-submissions <OUR_TEAM_ID>` の結果に自分の
# submissionId が含まれることを一度検証してから運用する。
OUR_TEAM_ID = os.environ.get("KAGGLE_TEAM_ID", "")
OUR_TEAM_NAME = os.environ.get("KAGGLE_TEAM_NAME", "")


def run_kaggle(args: list[str], as_json: bool = False) -> str | dict | list:
    """kaggle CLI をサブプロセスで実行する。

    stdout をシェルのパイプに直結しない（PowerShell 環境で broken pipe になりうるため、
    このラッパーで subprocess.run 経由の捕捉に統一する）。
    """
    cmd = ["kaggle", *args]
    if as_json and "--format" not in args:
        cmd += ["--format", "json"]
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", env=env, check=False
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"kaggle CLI failed: {' '.join(cmd)}")
    if as_json:
        return json.loads(result.stdout)
    return result.stdout


DATA_DIR.mkdir(exist_ok=True)
