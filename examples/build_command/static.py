from typing import Annotated

from typer import Typer, Argument, Option


cli = Typer()

@cli.command()
def static(
    mite1: Annotated[str, Argument(help="This is mighty argument 1")],
    dyna2: Annotated[int, Option(help="This is dynamic option 2")],
    dyna1: Annotated[str, Option(help="This is dynamic option 1")] = "default1",
    mite2: Annotated[int | None, Argument(help="This is mighty argument 2")] = None,
):
    """
    Just prints values of passed params
    """
    print(f"{dyna1=}, {dyna2=}, {mite1=}, {mite2=}")


if __name__ == "__main__":
    cli()
