from typer import Typer
from typer_repyt import build_command, OptDef, ArgDef


cli = Typer()


def dynamic(dyna1: str, dyna2: int, mite1: str, mite2: int | None):
    """
    Just prints values of passed params
    """
    print(f"{dyna1=}, {dyna2=}, {mite1=}, {mite2=}")


build_command(
    cli,
    dynamic,
    OptDef(name="dyna1", param_type=str, help="This is dynamic option 1", default="default1"),
    OptDef(name="dyna2", param_type=int, help="This is dynamic option 2"),
    ArgDef(name="mite1", param_type=str, help="This is mighty argument 1"),
    ArgDef(name="mite2", param_type=int | None, help="This is mighty argument 2", default=None),
)

if __name__ == "__main__":
    cli()
