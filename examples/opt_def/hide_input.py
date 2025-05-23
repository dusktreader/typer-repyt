from typing import Annotated

from typer import Typer, Option
from typer_repyt import build_command, OptDef

cli = Typer()

@cli.command()
def static(dyna: Annotated[str, Option(prompt=True, confirmation_prompt=True, hide_input=True)]):
    print(f"{dyna=}")


def dynamic(dyna: str):
    print(f"{dyna=}")


build_command(
    cli,
    dynamic,
    OptDef(name="dyna", param_type=str, prompt=True, confirmation_prompt=True, hide_input=True),
)


if __name__ == "__main__":
    cli()
