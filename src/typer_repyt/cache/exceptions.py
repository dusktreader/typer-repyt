from typer_repyt.constants import ExitCode
from typer_repyt.exceptions import RepytError


class CacheError(RepytError):
    exit_code: ExitCode = ExitCode.GENERAL_ERROR


class CacheInitError(CacheError):
    pass


class CacheStoreError(CacheError):
    pass


class CacheClearError(CacheError):
    pass


class CacheLoadError(CacheError):
    pass
