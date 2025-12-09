from statistics import Statistics

from matchers import All, And, HasAtLeast, HasFewerThan, Not, PlaysIn
from player_reader import PlayerReader


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    matcher = And(HasFewerThan(2, "goals"), PlaysIn("NYR"))
    filtered_with_all = stats.matches(All())
    print(len(filtered_with_all))

    for player in stats.matches(matcher):
        print(player)


if __name__ == "__main__":
    main()
