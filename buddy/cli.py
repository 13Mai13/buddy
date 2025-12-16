# buddy/cli.py
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from .db import list_repos
from .indexer import index_repo
from .rag import answer_question, generate_summary

app = typer.Typer(help="Buddy — your private AI onboarding tool for codebases.")
console = Console()


def _select_repo(repo: Optional[str]) -> str:
    repos = list_repos()
    if not repos:
        console.print(
            "[red]No repos indexed yet. Run `buddy init <path>` first.[/red]"
        )
        raise typer.Exit(1)

    if repo:
        if repo not in repos:
            console.print(
                f"[red]Repo '{repo}' not found. Available:[/red] {repos}"
            )
            raise typer.Exit(1)
        return repo

    if len(repos) == 1:
        return repos[0]

    console.print("[bold]Multiple repos indexed. Choose one:[/bold]")
    for i, r in enumerate(repos, start=1):
        console.print(f"{i}. {r}")
    choice = typer.prompt("Enter number", default="1")
    idx = int(choice) - 1
    return repos[idx]


@app.command()
def init(
    paths: list[Path] = typer.Argument(
        ..., exists=True, file_okay=False, dir_okay=True
    )
):
    """
    Index one or more repo directories.
    """
    for path in paths:
        console.print(Panel.fit(f"Indexing [bold]{path}[/bold]"))
        index_repo(path)
    console.print("[green]Done indexing.[/green]")


@app.command()
def ask(
    question: str = typer.Argument(...),
    repo: Optional[str] = typer.Option(None, "--repo", "-r"),
):
    """
    Ask Buddy a question about the codebase.
    """
    repo_root = _select_repo(repo)
    console.print(f"[bold]Repo:[/bold] {repo_root}")
    console.print(f"[bold]Question:[/bold] {question}\n")

    answer = answer_question(repo_root, question)
    console.print(Panel(answer, title="Answer", expand=True))


@app.command()
def summary(
    repo: Optional[str] = typer.Option(None, "--repo", "-r")
):
    """
    Generate a high-level onboarding summary for the codebase.
    """
    repo_root = _select_repo(repo)
    console.print(f"[bold]Repo:[/bold] {repo_root}")
    console.print("[bold]Generating summary...[/bold]\n")

    text = generate_summary(repo_root)
    console.print(Panel(text, title="Summary", expand=True))


if __name__ == "__main__":
    app()
