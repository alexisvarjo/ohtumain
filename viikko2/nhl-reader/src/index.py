"""NHL Player Stats Viewer: fetches, filters, and displays player statistics."""

import requests
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from player import Player

console = Console()


def print_players(players: list):
    """Display a table of player statistics."""
    table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAVY)
    table.add_column("Released", style="cyan", justify="left")
    table.add_column("teams", style="magenta")
    table.add_column("goals", justify="center", style="green")
    table.add_column("assists", justify="center", style="yellow")
    table.add_column("points", justify="center", style="bold white")

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.points),
        )

    console.print(table)


def filter_by_nationality(nationality_code: str, players: list) -> list:
    """Return players matching the given nationality code."""
    return [p for p in players if p.nationality == nationality_code]


def sort_by_points(players: list):
    """Return players sorted by total points."""
    return sorted(players, key=lambda p: p.points, reverse=True)


class PlayerReader:  # pylint: disable=too-few-public-methods
    """Fetches and parses NHL player data from the API."""

    def __init__(self, url: str):
        self.url = url
        self.players = self.get_players()

    def get_players(self):
        """Fetch players from the API and return Player objects."""
        response = requests.get(self.url, timeout=10).json()
        players = []
        for player_dict in response:
            player = Player(player_dict)
            players.append(player)
        return players


class PlayerStats:  # pylint: disable=too-few-public-methods
    """Provides access to filtered player statistics."""

    def __init__(self, reader: PlayerReader):
        self.players = reader.players

    def top_scorers_by_nationality(self, nationality_code: str):
        """Return top-scoring players for a given nationality."""
        filtered = filter_by_nationality(nationality_code.upper(), self.players)
        sorted_players = sort_by_points(filtered)
        return sorted_players


def main():
    """main function"""
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    console.print(
        Panel(
            Text(
                (
                    "NHL 2024–25 Player Stats Viewer\n"
                    "Enter nationality codes (e.g., FIN, SWE, LAT, USA)\n"
                    "Type 'exit' to quit."
                ),
                justify="center",
                style="bold white",
            ),
            title="[cyan] NHL Stats[/cyan]",
            border_style="magenta",
            expand=False,
        )
    )

    while True:
        nationality = (
            console.input("[bold cyan]Enter nationality code:[/bold cyan] ")
            .strip()
            .upper()
        )

        if nationality in ["EXIT", "QUIT", "Q"]:
            console.print("\n[green]Goodbye! [/green]")
            break

        players = stats.top_scorers_by_nationality(nationality)

        if not players:
            console.print(
                f"[red]No players found for nationality '{nationality}'.[/red]\n"
            )
            continue

        header = Text(
            f" Season 2024–25 players from {nationality} ", style="bold white on black"
        )
        console.print(Panel(header, border_style="cyan", expand=False))

        print_players(players)
        console.print()


if __name__ == "__main__":
    main()
