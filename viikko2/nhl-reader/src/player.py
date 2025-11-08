"""Defines the Player data model for NHL statistics."""


class Player:  # pylint: disable=too-few-public-methods
    """Represents a single NHL player and their statistics."""

    def __init__(self, data):
        self.name = data["name"]
        self.nationality = data["nationality"]
        self.assists = data["assists"]
        self.goals = data["goals"]
        self.points = self.assists + self.goals
        self.team = data["team"]
        self.games = data["games"]

    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:2} + {self.assists:2} = {self.points:2}"
