import typer
from abc import ABC, abstractmethod

class OutputHandler(ABC):
    """
    Abstract Base Class for handling all console output.
    Defines an interface for different output methods.
    """
    @abstractmethod
    def info(self, message: str):
        """Prints a standard informational message."""
        pass

    @abstractmethod
    def success(self, message: str):
        """Prints a success message."""
        pass

    @abstractmethod
    def error(self, message: str, bold: bool = True):
        """Prints an error message."""
        pass

    @abstractmethod
    def warn(self, message: str):
        """Prints a warning message."""
        pass


class TyperOutputHandler(OutputHandler):
    """An implementation of OutputHandler that uses Typer for rich console output."""

    def info(self, message: str):
        typer.echo(message)

    def success(self, message: str):
        typer.secho(message, fg=typer.colors.GREEN)

    def error(self, message: str, bold: bool = True):
        typer.secho(message, fg=typer.colors.RED, bold=bold)

    def warn(self, message: str):
        typer.secho(message, fg=typer.colors.YELLOW)