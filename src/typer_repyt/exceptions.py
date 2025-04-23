from buzz import Buzz


class RepytError(Buzz):
    """
    Base class for exceptions used in the `typer_repyt` module.
    """

    pass


class ContextError(RepytError):
    pass


class ConfigError(RepytError):
    pass


class ConfigInitError(ConfigError):
    pass


class ConfigUnsetError(ConfigError):
    pass


class ConfigResetError(ConfigError):
    pass


class ConfigUpdateError(ConfigError):
    pass


class ConfigSaveError(ConfigError):
    pass


class BuildCommandError(RepytError):
    pass
