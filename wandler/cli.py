import typer
import importlib.metadata
from typing_extensions import Annotated
from .errors import TaskError, ConfigError
from .config import ConfigManager
from .engine import TaskRunner
from .output import TyperOutputHandler

config_manage = ConfigManager()
output = TyperOutputHandler()

app = typer.Typer(
    help="wandler: A smart, fast task orchestrator for Python projects.",
    add_completion=False,
    no_args_is_help=True,
    epilog="""For more info, run any command with the --help flag:
    
  $ wandler run --help
  $ wandler list --help
"""
)

@app.callback(invoke_without_command=True)
def callback(
        ctx: typer.Context,
        version: Annotated[
            bool, typer.Option(
                "--version",
                "-v",
                help="Show the version and exit.")
        ] = False,
):
    """
    For more info, run any command with the --help flag:
      $ wandler run --help
      $ wandler list --help
    """
    if version:
        try:
            # This reads the version from your pyproject.toml
            __version__ = importlib.metadata.version("wandler")
            typer.echo(__version__)
        except importlib.metadata.PackageNotFoundError:
            # Fallback if the package isn't installed
            typer.echo("wandler version (unknown: package not installed)")
        raise typer.Exit()

    # This prevents the callback from running when a subcommand is used
    if ctx.invoked_subcommand is not None:
        return


@app.command()
@app.command()
def run(task_name: str):
    """
    Run a specific task by name.

    Args:
        task_name (str): The name of the task to run.

    Returns:
        None
    """
    try:
        # 1. Manager delegates config work
        config = config_manage.get_config()
        base_dir = config_manage.get_config_path().parent

        # 2. Manager finds the specialist
        runner = TaskRunner(config, base_dir, output)

        # 3. Manager delegates the *actual work*
        runner.run_task(task_name)

    except ConfigError as e:
        output.error(str(e))  # Manager handles errors
    except TaskError as e:
        output.error(str(e))  # Manager handles errors

@app.command(name="list")
def list_tasks():
    """
    List all available tasks defined in the configuration file.

    Reads the configuration, validates it, and prints a formatted list
    of all task names along with their descriptions.

    Returns:
        None

    Raises:
        typer.Exit: If there is a configuration error.
    """
    try:
        config = config_manage.get_config()

        if not config.tasks:
            output.warn("No tasks found in the configuration file.")
            return

        output.info("Available tasks:")
        for task_name, task_details in config.tasks.items():
            description = task_details.description or "No description"
            line = f"{task_name:<20} - {description}"
            output.info(line)

    except ConfigError as e:
        output.error(str(e))
        raise typer.Exit(code=1)

def main():
    app()