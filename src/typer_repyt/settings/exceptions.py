from typer_repyt.constants import ExitCode
from typer_repyt.exceptions import RepytError


class SettingsError(RepytError):
    exit_code: ExitCode = ExitCode.GENERAL_ERROR


class SettingsInitError(SettingsError):
    pass


class SettingsUnsetError(SettingsError):
    pass


class SettingsResetError(SettingsError):
    pass


class SettingsUpdateError(SettingsError):
    pass


class SettingsSaveError(SettingsError):
    pass
