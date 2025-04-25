from buzz import Buzz


class RepytError(Buzz):
    """
    Base class for exceptions used in the `typer_repyt` module.
    """

    pass


class ContextError(RepytError):
    pass


class BuildCommandError(RepytError):
    pass
