"""Kaggle のコンペページを取得し、docs/overview.md（Overview の各節）と docs/data.md（Data）に書き出す。

実行: tools/nvkg tools/fetch_competition_pages.py [出力ディレクトリ（既定: docs）]
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from runtime import competition_pages, html_to_markdown  # nvidia-kaggle プラグイン

# 出力ファイルごとに、読む順にページ名と見出しを並べる。
FILES = {
    "overview.md": [
        ("abstract", "Overview"),
        ("description", "Description"),
        ("background", "Background"),
        ("evaluation", "Evaluation"),
        ("timeline", "Timeline"),
        ("prizes", "Prizes"),
        ("code requirements", "Code Requirements"),
    ],
    "data.md": [
        ("data-description", "Data-Description"),
    ],
}


def main() -> None:
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    competition = os.environ.get("KAGGLE_COMPETITION", "").strip()
    if not competition:
        raise SystemExit("KAGGLE_COMPETITION にコンペのスラッグを設定してください")
    pages = competition_pages(competition)
    retrieved_at = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M JST")
    documents = {}
    for filename, sections in FILES.items():
        parts = [
            f"# {title}\n\n{html_to_markdown(pages[name]).strip()}\n"
            for name, title in sections
            if name in pages
        ]
        if not parts:
            raise SystemExit(
                f"{filename} の対象ページがありません。既存ファイルは変更しません"
            )
        tab = "data" if filename == "data.md" else "overview"
        source = f"https://www.kaggle.com/competitions/{competition}/{tab}"
        header = f"> 出典: {source}\n> 取得日時: {retrieved_at}\n\n"
        documents[filename] = header + "\n".join(parts)
    out_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in documents.items():
        (out_dir / filename).write_text(content, encoding="utf-8")
        print(f"{out_dir / filename} に書き出した")


if __name__ == "__main__":
    main()
