from statistics import Statistics

from matchers import All, And, HasAtLeast, HasFewerThan, Not, Or, PlaysIn
from player_reader import PlayerReader


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    matcher = And(
        HasAtLeast(70, "points"), Or(PlaysIn("COL"), PlaysIn("FLA"), PlaysIn("BOS"))
    )

    for player in stats.matches(matcher):
        print(player)


if __name__ == "__main__":
    main()
