from typing import Any, Literal

import snick
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


def terminal_message(
    message: str,
    subject: str | None = None,
    subject_align: Literal["left", "right", "center"] = "left",
    color: str = "green",
    footer: str | None = None,
    footer_align: Literal["left", "right", "center"] = "left",
    indent: bool = True,
    markdown: bool = False,
):
    panel_kwargs: dict[str, Any] = dict(padding=1, title_align=subject_align, subtitle_align=footer_align)
    if subject is not None:
        panel_kwargs["title"] = f"[{color}]{subject}"
    if footer is not None:
        panel_kwargs["subtitle"] = f"[dim italic]{footer}[/dim italic]"
    text: str = snick.dedent(message)
    if indent:
        text = snick.indent(text, prefix="  ")
    content: str | Markdown = text
    if markdown:
        content = Markdown(text)
    console = Console()
    console.print()
    console.print(Panel(content, **panel_kwargs))
    console.print()


def simple_message(message: str, indent: bool = False, markdown: bool = False):
    text: str = snick.dedent(message)
    if indent:
        text = snick.indent(text, prefix="  ")
    content: str | Markdown = text
    if markdown:
        content = Markdown(text)
    console = Console()
    console.print()
    console.print(content)
    console.print()
