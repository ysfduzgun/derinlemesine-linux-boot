import os
from pathlib import Path
import markdown

SRC_DIR = Path("src")
BUILD_DIR = Path("build")
TEMPLATE_PATH = Path("template/template.html")

def build_site():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    if not TEMPLATE_PATH.exists():
        return
    
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    md_files = list(SRC_DIR.glob("*.md"))
    
    if not md_files:
        return

    for src_path in md_files:
        title = src_path.stem  # .md uzantısı olmadan dosya adı
        html_name = f"{title}.html"
        dest_path = BUILD_DIR / html_name

        md_content = src_path.read_text(encoding="utf-8")
        html_ctx = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])

        html_content = template.replace("{title}", title).replace("{content}", html_ctx)

        dest_path.write_text(html_content, encoding="utf-8")

if __name__ == "__main__":
    build_site()

