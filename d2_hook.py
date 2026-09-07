"""
mkdocs hook (see https://www.mkdocs.org/user-guide/configuration/#hooks) that
renders ```d2 fenced code blocks locally via the `d2` CLI.

Runs at on_page_markdown time, i.e. on the raw markdown text before any
markdown extension (including pymdownx.superfences, used by mermaid2) sees
it, so it can't interfere with how other fenced blocks are processed.
"""

import re
import subprocess
from pathlib import Path

FENCE_RE = re.compile(
    r'```d2(?:\s+alt="(?P<alt>[^"]*)")?\n(?P<source>.*?)\n```',
    re.DOTALL,
)


def on_page_markdown(markdown, page, config, files, **kwargs):
    if "```d2" not in markdown:
        return markdown

    page_dir = Path(page.file.abs_src_path).parent

    def render(match):
        source = match.group("source")
        alt = match.group("alt") or ""

        result = subprocess.run(
            [
                "d2",
                "--layout=elk",
                "--elk-nodeNodeBetweenLayers=45",
                "--elk-edgeNodeBetweenLayers=15",
                "--pad=5",
                "-",
                "-",
            ],
            input=source.encode(),
            capture_output=True,
            cwd=page_dir,
        )
        if result.returncode != 0:
            error = result.stderr.decode().strip()
            return f'<pre class="d2-error">D2 render error:\n{error}</pre>'

        svg = result.stdout.decode()
        svg = svg[svg.index("<svg") :]
        svg = svg.replace("<svg", f'<svg aria-label="{alt}"', 1)
        return f'<div class="d2-diagram">\n{svg}\n</div>'

    return FENCE_RE.sub(render, markdown)
