from enum import Enum, Flag, auto


class Sentinel(Enum):
    """
    Define a Sentinel type.

    See this for an explanation of the use-case for sentinels: https://peps.python.org/pep-0661/
    """

    MISSING = auto()
    NOT_GIVEN = auto()


class Validation(Flag):
    """
    Defines whether validation should happen "before", "after", "both", or "none"
    """
    BEFORE = auto()
    AFTER = auto()
    BOTH = BEFORE | AFTER
    NONE = 0
