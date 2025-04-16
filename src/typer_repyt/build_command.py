import ast
from functools import reduce
import inspect
import textwrap
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast, Literal
from types import UnionType

import typer

from typer_repyt.constants import Sentinel
from typer_repyt.exceptions import RepytError


@dataclass
class ParamDef:
    """
    Define the necessary components to build a Typer `Option` or `Argument`.

    These elements are used by both `OptDef` and `ArgDef`.
    """

    name: str
    param_type: UnionType | type[Any]
    default: Any | None | Literal[Sentinel.NOT_GIVEN] = Sentinel.NOT_GIVEN
    help: str | None = None
    rich_help_panel: str | None = None
    show_default: bool | str = True


@dataclass
class OptDef(ParamDef):
    """
    Define the additional components to build a Typer `Option`.
    """

    prompt: bool | str = False
    confirmation_prompt: bool = False
    hide_input: bool = False
    override_name: str | None = None
    short_name: str | None = None
    callback: Callable[..., Any] | None = None
    is_eager: bool = False


@dataclass
class ArgDef(ParamDef):
    """
    Define the additional components to build a Typer `Argument`.
    """

    metavar: str | None = None
    hidden: bool = False
    envvar: str | list[str] | None = None
    show_envvar: bool = True


def build_command(cli: typer.Typer, func: Callable[..., None], *param_defs: ParamDef):
    """
    Build a Typer command dynamically based on a function template and list of argument definitions.

    Args:
        cli:        The Typer app that the command should be added to
        func:       A "template" function that will be used to build out the final function.
                    The name of the function will be preserved as will its docstring.
                    Though it is useful to define arguments for the function that match the opt_defs, it is not necessary.
                    It will, however, help with static type checking.
        param_defs: Argument definitions that will be used to dynamically build the Typer command.

    The following two command definitions are equivalent:

    ```python
    cli = typer.Typer()

    @cli.command()
    def static(
        mite1: Annotated[str, typer.Argument(help="This is mighty argument 1")],
        dyna2: Annotated[int, typer.Option(help="This is dynamic option 2")],
        dyna1: Annotated[str, typer.Option(help="This is dynamic option 1")] = "default1",
        mite2: Annotated[int | None, typer.Argument(help="This is mighty argument 2")] = None,
    ):
        '''
        Just prints values of passed params
        '''
        print(f"{dyna1=}, {dyna2=}, {mite1=}, {mite2=}")

    def dynamic(dyna1: str, dyna2: int, mite1: str, mite2: int | None):
        '''
        Just prints values of passed params
        '''
        print(f"{dyna1=}, {dyna2=}, {mite1=}, {mite2=}")

    build_command(
        cli,
        dynamic,
        OptDef(name="dyna1", param_type=str, help="This is dynamic option 1", default="default1"),
        OptDef(name="dyna2", param_type=int, help="This is dynamic option 2"),
        ArgDef(name="mite1", param_type=str, help="This is mighty argument 1"),
        ArgDef(name="mite2", param_type=int | None, help="This is mighty argument 2", default=None),
    )

    ```
    """
    # TODO: Add some examples to the docstring

    # These will hold the args and kwargs (with defaults) for the final constructed function
    args: list[ast.arg] = []
    kwonlyargs: list[ast.arg] = []
    kw_defaults: list[Any] = []

    # Create a local namespace for the compiled function
    namespace: dict[str, Any] = {}

    # Convert each ParamDef into an Annotated keyword argument for the constructed function
    for param_def in param_defs:
        param_args: list[Any] = []

        keywords: list[ast.keyword] = [
            ast.keyword(arg="help", value=ast.Constant(value=param_def.help)),
            ast.keyword(arg="rich_help_panel", value=ast.Constant(value=param_def.rich_help_panel)),
            ast.keyword(arg="show_default", value=ast.Constant(value=param_def.show_default)),
        ]

        # If the ParamDef is an OptDef, assemble args and keywords for it
        if isinstance(param_def, OptDef):
            if param_def.override_name:
                param_args.append(ast.Constant(value=f"--{param_def.override_name}"))
            if param_def.short_name:
                param_args.append(ast.Constant(value=f"-{param_def.short_name}"))
            if param_def.callback:
                keywords.append(ast.keyword(arg="callback", value=ast.Name(param_def.callback.__name__)))
                namespace[param_def.callback.__name__] = param_def.callback
            keywords.extend(
                [
                    ast.keyword(arg="prompt", value=ast.Constant(value=param_def.prompt)),
                    ast.keyword(arg="confirmation_prompt", value=ast.Constant(value=param_def.confirmation_prompt)),
                    ast.keyword(arg="hide_input", value=ast.Constant(value=param_def.hide_input)),
                    ast.keyword(arg="is_eager", value=ast.Constant(value=param_def.is_eager)),
                ]
            )

        # If the ParamDef is an ArgDef, assemble args and keywords for it
        elif isinstance(param_def, ArgDef):
            keywords.extend(
                [
                    ast.keyword(arg="metavar", value=ast.Constant(value=param_def.metavar)),
                    ast.keyword(arg="hidden", value=ast.Constant(value=param_def.hidden)),
                    ast.keyword(arg="show_envvar", value=ast.Constant(value=param_def.show_envvar)),
                ]
            )

            if isinstance(param_def.envvar, str):
                keywords.append(ast.keyword(arg="envvar", value=ast.Constant(value=param_def.envvar)))
            elif isinstance(param_def.envvar, list):
                keywords.append(
                    ast.keyword(
                        arg="envvar",
                        value=ast.List(elts=[ast.Constant(value=env) for env in param_def.envvar]),
                    )
                )

        # If the ParamDef is not an OptDef or ArgDef, raise an error indicating that it's unsupported
        else:
            raise RepytError(f"Unsupported parameter definition type: {type(param_def)}")

        # Get the type annotation for the opt/arg
        # Just found out that I didn't need to do this (yet) because Typer does not support Union types
        # I will keep it here in case it does soon: https://github.com/fastapi/typer/pull/1148
        type_expr: ast.Name | ast.BinOp
        if isinstance(param_def.param_type, UnionType):

            def bitor(left: ast.expr | type[Any], right: type[Any]) -> ast.BinOp:
                if not isinstance(left, ast.expr):
                    left = ast.Name(id=left.__name__)
                return ast.BinOp(left=left, op=ast.BitOr(), right=ast.Name(id=right.__name__))

            type_expr = reduce(bitor, param_def.param_type.__args__)
        else:
            type_expr = ast.Name(id=param_def.param_type.__name__)

        # Create the actual Annotated element using func, args, and keywords assembled above
        param_attr = "Option" if isinstance(param_def, OptDef) else "Argument"
        annotation = ast.Subscript(
            value=ast.Name(id="Annotated"),
            slice=ast.Tuple(
                elts=[
                    type_expr,
                    ast.Call(
                        func=ast.Attribute(value=ast.Name(id="typer"), attr=param_attr),
                        args=param_args,
                        keywords=keywords,
                    ),
                ],
            ),
        )

        # Add the constructed CLI option/argument.
        # If a default is not provided, it is added as an argument. Otherwise, it is added as a kwonlyarg
        arg = ast.arg(arg=param_def.name, annotation=annotation)
        if param_def.default is Sentinel.NOT_GIVEN:
            args.append(arg)
        else:
            kwonlyargs.append(arg)
            kw_defaults.append(ast.Constant(value=param_def.default))

    # Extract the function body from the template function
    source = textwrap.dedent(inspect.getsource(func)).strip()
    parsed_ast: ast.Module = ast.parse(source)
    RepytError.require_condition(
        len(parsed_ast.body) == 1, "Function template must contain exactly one function definition"
    )
    fdef: ast.FunctionDef = cast(ast.FunctionDef, parsed_ast.body[0])
    body = fdef.body

    # Add imports for Annotated, typer.Option, and NoneType
    annotated_import = ast.ImportFrom(module="typing", names=[ast.alias(name="Annotated")], level=0)
    typer_import = ast.Import(names=[ast.alias(name="typer")])
    nonetype_import = ast.ImportFrom(module="types", names=[ast.alias(name="NoneType")], level=0)

    # Create the function definition
    func_def = ast.FunctionDef(
        name=func.__name__,
        args=ast.arguments(
            args=args,
            kwonlyargs=kwonlyargs,
            kw_defaults=kw_defaults,
        ),
        body=body,
    )

    # Compile a module containing the imports and function definition
    module = ast.Module(body=[annotated_import, typer_import, nonetype_import, func_def])
    _set_ast_location(module)
    code = compile(module, filename="<ast>", mode="exec")

    # execute the compiled module
    exec(code, globals(), namespace)

    # Add the function to the Typer app
    cli.command()(namespace[func.__name__])


def _set_ast_location(node: ast.AST, lineno: int = 0, col_offset: int = 0):
    """
    Set the `lineno` and `col_offset` attributes for all nodes (that need them).

    This is necessary, because the constructed AST from `build_command` requires many nodes to have the `lineno` and
    `col_offset` values set. Even though these are not used for anything, it's important to set these values to produce
    a valid AST.
    """
    for child in ast.iter_child_nodes(node):
        _set_ast_location(child, lineno, col_offset)
    if "lineno" in node._attributes:
        setattr(node, "lineno", lineno)
    if "col_offset" in node._attributes:
        setattr(node, "col_offset", col_offset)
