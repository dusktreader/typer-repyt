from typing import cast

import typer
from pydantic import BaseModel
from snick import dedent

from typer_repyt.settings import attach_settings, get_settings


class ExampleSettings(BaseModel):
    name: str = "jawa"
    planet: str = "tatooine"
    alignment: str = "neutral"


cli = typer.Typer()


@cli.command()
@attach_settings(ExampleSettings)
def report(ctx: typer.Context, loud: bool = False):
    settings: ExampleSettings = cast(ExampleSettings, get_settings(ctx))
    text: str = dedent(
        f"""
        Look at this {settings.name} from {settings.planet}. It's soooo {settings.alignment}!
        """
    )
    if loud:
        text = text.upper()

    print(text.format(ctx=ctx))


if __name__ == "__main__":
    cli()
