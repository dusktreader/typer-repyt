import re
from typing import Any

import typer
from snick import strip_ansi_escape_sequences, strip_whitespace, dedent, indent
from typer.testing import CliRunner


runner = CliRunner()


def get_output(
    cli: typer.Typer,
    *args: str,
    exit_code: int = 0,
    env_vars: dict[str, str] | None = None,
    strip_terminal_controls: bool = True,
    **kwargs: Any,
) -> str:
    if env_vars is None:
        env_vars = {}
    result = runner.invoke(cli, args, env=env_vars, **kwargs)
    assert result.exit_code == exit_code
    output = result.stdout
    if strip_terminal_controls:
        output = strip_ansi_escape_sequences(output)
    return output


def get_help(cli: typer.Typer) -> str:
    return get_output(cli, "--help")


def check_output(
    cli: typer.Typer,
    *args: str,
    expected_substring: str | list[str] | None = None,
    exit_code: int = 0,
    env_vars: dict[str, str] | None = None,
    **kwargs: Any,
):
    output = get_output(cli, *args, exit_code=exit_code, env_vars=env_vars, **kwargs)
    if not expected_substring:
        return
    elif isinstance(expected_substring, str):
        expected_substring = [expected_substring]
    for es in expected_substring:
        assert es in output, output


def check_help(
    cli: typer.Typer,
    expected_substring: str | list[str] | None = None,
    env_vars: dict[str, str] | None = None,
    **kwargs: Any,
):
    check_output(cli, "--help", expected_substring=expected_substring, exit_code=0, env_vars=env_vars, **kwargs)


def match_output(
    cli: typer.Typer,
    *args: str,
    expected_pattern: str | list[str] | None = None,
    exit_code: int = 0,
    env_vars: dict[str, str] | None = None,
    **kwargs: Any,
):
    output = get_output(cli, *args, exit_code=exit_code, env_vars=env_vars, **kwargs)
    if not expected_pattern:
        return
    elif isinstance(expected_pattern, str):
        expected_pattern = [expected_pattern]
    for ep in expected_pattern:
        mangle_pattern = ep
        mangle_pattern = mangle_pattern.replace("[", r"\[")
        mangle_pattern = mangle_pattern.replace("]", r"\]")
        mangle_pattern = strip_whitespace(mangle_pattern)

        mangle_help_text = output
        mangle_help_text = strip_whitespace(mangle_help_text)

        rounded = ["╭", "─", "┬", "╮", "│", "├", "┼", "┤", "╰", "┴", "╯"]
        for char in rounded:
            mangle_help_text = mangle_help_text.replace(char, "")



        assert re.search(mangle_pattern, mangle_help_text) is not None, build_fail_message(
            ep, mangle_pattern, output, mangle_help_text
        )


def match_help(
    cli: typer.Typer,
    expected_pattern: str | list[str] | None = None,
    env_vars: dict[str, str] | None = None,
    **kwargs: Any,
):
    match_output(cli, "--help", expected_pattern=expected_pattern, exit_code=0, env_vars=env_vars, **kwargs)


def build_fail_message(pattern: str, mangled_pattern: str, output: str, mangled_output: str):
    return dedent(
        f"""
        Search pattern was not found in help_text

        Search Pattern:
        {pattern}

        "Mangled" Search Pattern:
        {repr(mangled_pattern)}

        Help Text:
        {indent(output, prefix="            ", skip_first_line=True)}

        "Mangled" Help Text:
        {repr(mangled_output)}
        """
    )
