from typing import Annotated

from typer import Typer, Argument
from typer_repyt import build_command, ArgDef

cli = Typer()


@cli.command()
def static(mite: Annotated[str, Argument(hidden=True)]):
    print(f"{mite=}")


def dynamic(mite: str):
    print(f"{mite=}")


build_command(
    cli,
    dynamic,
    ArgDef(name="mite", param_type=str, hidden=True),
)


if __name__ == "__main__":
    cli()
