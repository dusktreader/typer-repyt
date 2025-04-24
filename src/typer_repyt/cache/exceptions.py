from typer_repyt.exceptions import RepytError


class CacheError(RepytError):
    pass


class CacheInitError(CacheError):
    pass


class CacheStoreError(CacheError):
    pass


class CacheFreeError(CacheError):
    pass


class CacheClearError(CacheError):
    pass


class CacheLoadError(CacheError):
    pass
