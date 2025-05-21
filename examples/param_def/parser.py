import json
from typing import Annotated

from pydantic import BaseModel
from typer import Typer, Option
from typer_repyt import build_command, OptDef

class Dyna(BaseModel):
    c4: str
    semtex: int


def parser(val: str) -> Dyna:
    return Dyna(**json.loads(val))


cli = Typer()

@cli.command()
def static(dyna: Annotated[Dyna, Option(parser=parser)]):
    print(f"{dyna=}")


def dynamic(dyna: Dyna):
    print(f"{dyna=}")


build_command(cli, dynamic, OptDef(name="dyna", param_type=Dyna, parser=parser))


if __name__ == "__main__":
    cli()
