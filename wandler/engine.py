from pathlib import Path
import shlex
import subprocess
from .models import Config, Task
from .errors import TaskError
from .output import TyperOutputHandler

class TaskRunner:
    """
    Orchestrates the execution of a task by finding its
    details and then running its command.
    """
    def __init__(self, config: Config, base_dir: Path, output: TyperOutputHandler):
        self.config = config
        self.base_dir = base_dir
        self.output = output

    def __get_task_details(self, task_name: str) -> Task:
        """
        Private "prep" method.
        Finds the Task object in the config or raises an error.
        """
        task = self.config.tasks.get(task_name)
        if not task:
            raise TaskError(f"Task '{task_name}' not found in the configuration.")
        return task

    def __execute_command(self, task: Task):
        """
        Private "specialist" method.
        Runs the task's command in a subprocess.
        """
        self.output.info(f"Running command: {task.command}")
        command_list = shlex.split(task.command)

        subprocess.run(
            command_list,
            cwd=self.base_dir,
            check=True
        )

    def run_task(self, task_name: str):
        """
        Public method to run a task by its name.

        This method orchestrates the two main steps:
        1. Find the task details.
        2. Execute the task's command.
        """
        try:
            task_to_run = self.__get_task_details(task_name)
            self.__execute_command(task_to_run)
            self.output.success(f"Task '{task_name}' completed successfully.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise TaskError(f"Task '{task_name}' failed!") from e