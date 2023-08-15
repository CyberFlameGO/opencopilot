import typer

from sdk import cli_chat
from sdk import cli_create_copilot
from sdk import cli_docker_run
from sdk import cli_docker_stop
from sdk import cli_eval
from sdk import cli_validate
from sdk.utils import print_utils

app = typer.Typer(add_completion=False)


@app.command(help="Create a Copilot")
def create():
    cli_create_copilot.main()
    print_utils.print_yellow("Recommended next step:")
    print_utils.print_yellow(" -> opencopilot start")


@app.command(help="Validate Copilot")
def validate():
    cli_validate.main()


@app.command(help="Start the Copilot")
def start():
    cli_docker_run.main()


@app.command(help="Restart the Copilot - reloads new data")
def restart():
    cli_docker_run.main()


@app.command(help="Stop the Copilot")
def stop():
    cli_docker_stop.main()


@app.command(help="Chat with the Copilot. Example: chat 'Hello, who are you?'")
def chat(message: str):
    cli_chat.main(message)


@app.command(help="Evaluate the copilot end to end with examples from copilots/<my-copilot>/eval_data/endtoend_human.json")
def evaluate():
    cli_eval.main()


if __name__ == "__main__":
    app()
