#!/usr/bin/env python3
"""Build a self-contained, dark-mode-aware HTML ebook from a Markdown file.

Usage: python3 build_html.py <input.md> <output.html> [title]
Requires: pip install markdown
"""
import sys
import pathlib

import markdown

def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src_path, out_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    title = sys.argv[3] if len(sys.argv) > 3 else src_path.stem
    body = markdown.markdown(
        src_path.read_text(), extensions=["tables", "toc", "fenced_code"]
    )
    html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>
body{{max-width:46em;margin:2em auto;padding:0 1em;font-family:-apple-system,"PingFang SC",sans-serif;line-height:1.75;color:#222}}
h1{{border-bottom:2px solid #444;padding-bottom:.3em;margin-top:2.5em}}
h2{{margin-top:2em;color:#1a4d80}}
table{{border-collapse:collapse;width:100%;font-size:.92em}}
td,th{{border:1px solid #ccc;padding:.4em .6em;text-align:left}}
th{{background:#f0f4f8}}
blockquote{{border-left:4px solid #1a4d80;margin:1em 0;padding:.5em 1em;background:#f6f9fc;color:#333}}
code{{background:#f2f2f2;padding:.1em .35em;border-radius:3px;font-size:.9em}}
pre code{{display:block;padding:1em;overflow-x:auto}}
@media(prefers-color-scheme:dark){{body{{background:#1b1b1f;color:#ddd}}blockquote{{background:#26303a;color:#ccc}}code{{background:#2c2c31}}th{{background:#26303a}}td,th{{border-color:#444}}h2{{color:#7ab3e0}}}}
</style></head><body>{body}</body></html>"""
    out_path.write_text(html)
    print(f"OK {out_path} ({out_path.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
