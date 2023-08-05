"""Exception type definitions related to expression evaluation."""

from .base import TtError


class EvaluationError(TtError):
    """An exception type for errors occurring in expression evaluation.

    Warning:
        This exception type should be sub-classed and is not meant to be raised
        explicitly.

    """


class DuplicateSymbolError(EvaluationError):
    """An exception type for user-specified duplicate symbols."""


class ExtraSymbolError(EvaluationError):
    """An exception for a passed token that is not a parsed symbol."""


class InvalidBooleanValueError(EvaluationError):
    """An exception for an invalid truth value passed in evaluation."""


class MissingSymbolError(EvaluationError):
    """An exception type for a missing token value in evaluation."""


class NoEvaluationVariationError(EvaluationError):
    """An exception type for when evaluation of an expression will not vary."""
