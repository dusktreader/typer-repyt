from typer_repyt.exceptions import RepytError


class SettingsError(RepytError):
    pass


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
