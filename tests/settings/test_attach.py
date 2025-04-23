import json
from pathlib import Path
from typing import cast

import pytest
import typer
from pydantic import BaseModel
from typer.testing import CliRunner

from typer_repyt.constants import Validation
from typer_repyt.exceptions import ConfigError, ContextError
from typer_repyt.settings.attach import attach_settings, get_settings

from tests.helpers import match_output
from tests.settings.models import DefaultSettingsModel, RequiredFieldsModel


class TestAttachSettings:

    def test_attach_settings__adds_settings_to_context(self, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            assert hasattr(ctx.obj, "settings")
            assert isinstance(ctx.obj.settings, DefaultSettingsModel)
            assert ctx.obj.settings.name == "jawa"
            assert ctx.obj.settings.planet == "tatooine"
            assert ctx.obj.settings.is_humanoid
            assert ctx.obj.settings.alignment == "neutral"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

    def test_attach_settings__fails_on_invalid_settings_by_default(self, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            pass

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 1

    def test_attach_settings__does_not_fail_on_invalid_settings_with_no_validation(self, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel, validation=Validation.NONE)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            assert hasattr(ctx.obj, "settings")
            assert isinstance(ctx.obj.settings, RequiredFieldsModel)
            assert not hasattr(ctx.obj.settings, "name")
            assert not hasattr(ctx.obj.settings, "planet")
            assert ctx.obj.settings.is_humanoid
            assert ctx.obj.settings.alignment == "neutral"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

    def test_attach_settings__fails_before_with_before_validation(self):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel, validation=Validation.BEFORE)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            print("in function body")

        expected_pattern = [
            "in function body",
        ]
        match_output(
            cli,
            exit_code=1,
            expected_pattern=expected_pattern,
            negative_pattern=True,
            exception_type=ConfigError,
            exception_pattern="Initial settings are invalid",
            prog_name="test",
        )

    def test_attach_settings__fails_after_with_after_validation(self):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel, validation=Validation.AFTER)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            print("in function body")

        expected_pattern = [
            "in function body",
        ]
        match_output(
            cli,
            exit_code=1,
            expected_pattern=expected_pattern,
            exception_type=ConfigError,
            exception_pattern="Final settings are invalid",
            prog_name="test",
        )

    @pytest.mark.parametrize(
        "model,exception_pattern",
        [
            (RequiredFieldsModel, "Initial settings are invalid"),
            (DefaultSettingsModel, "Final settings are invalid"),
        ],
    )
    def test_attach_settings__fails_before_and_after_with_both_validation(
        self,
        model: type[BaseModel],
        exception_pattern: str,
    ):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(model, validation=Validation.BOTH)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            print("in function body")
            settings = get_settings(ctx)
            setattr(settings, "alignment", "invalid-alignment")

        match_output(
            cli,
            exit_code=1,
            exception_type=ConfigError,
            exception_pattern=exception_pattern,
            prog_name="test",
        )

    def test_attach_settings__persist(self, fake_settings_path: Path, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel, persist=True)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            settings = cast(DefaultSettingsModel, get_settings(ctx))
            settings.name = "hutt"
            settings.planet = "nal hutta"
            settings.is_humanoid = False
            settings.alignment = "evil"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

        assert fake_settings_path.exists()
        data = json.loads(fake_settings_path.read_text())
        assert data == dict(
            name="hutt",
            planet="nal hutta",
            is_humanoid=False,
            alignment="evil",
        )

    def test_attach_settings__loads_settings_from_disk_if_file_exists(
        self,
        fake_settings_path: Path,
        runner: CliRunner,
    ):
        fake_settings_path.write_text(
            json.dumps(
                dict(
                    name="jawa",
                    planet="tatooine",
                    is_humanoid=True,
                    alignment="neutral",
                )
            )
        )
        cli = typer.Typer()

        @cli.command()
        @attach_settings(RequiredFieldsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            assert hasattr(ctx.obj, "settings")
            assert isinstance(ctx.obj.settings, RequiredFieldsModel)
            assert ctx.obj.settings.name == "jawa"
            assert ctx.obj.settings.planet == "tatooine"
            assert ctx.obj.settings.is_humanoid
            assert ctx.obj.settings.alignment == "neutral"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

    def test_attach_settings__show_no_footer(self):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel, show=True)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            pass

        expected_pattern = [
            "name.*jawa",
            "planet.*tatooine",
            "is-humanoid.*True",
            "alignment.*neutral",
        ]
        match_output(
            cli,
            expected_pattern=expected_pattern,
            prog_name="test",
        )

    def test_attach_settings__adds_footer_if_persisted(self, fake_settings_path: Path):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel, persist=True, show=True)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction, reportUnusedParameter]
            pass

        expected_pattern = [
            "name.*jawa",
            "planet.*tatooine",
            "is-humanoid.*True",
            "alignment.*neutral",
            f"saved to {str(fake_settings_path)[:40]}",
        ]
        match_output(
            cli,
            expected_pattern=expected_pattern,
            prog_name="test",
        )


class TestGetSettings:

    def test_get_settings__extracts_settings_from_context(self, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        @attach_settings(DefaultSettingsModel)
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            settings = get_settings(ctx)
            assert isinstance(settings, DefaultSettingsModel)
            assert settings.name == "jawa"
            assert settings.planet == "tatooine"
            assert settings.is_humanoid
            assert settings.alignment == "neutral"

        result = runner.invoke(cli, [], prog_name="test")
        assert result.exit_code == 0

    def test_get_settings__raises_error_with_no_attached_settings(self, runner: CliRunner):
        cli = typer.Typer()

        @cli.command()
        def noop(ctx: typer.Context):  # pyright: ignore[reportUnusedFunction]
            """
            Note that we can't use `pytest.raises` here, because if the error doesn't match, pytest will raise an
            exception that won't be caught, and the cli will just exit with a non-zero code.
            """
            try:
                get_settings(ctx)
            except ContextError as err:
                assert "settings is not bound to context" in err.message
            except Exception as err:
                pytest.fail(f"Unexpected error: {err}")
            else:
                pytest.fail("The test should have failed!")

        runner.invoke(cli, [], prog_name="test")
