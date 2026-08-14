"""Manage saved Castle Chess tournaments."""

import json
from pathlib import Path

from models.tournament import Tournament


class TournamentManager:
    """Load, create, and track tournaments."""

    def __init__(self, data_folder="data/tournaments"):
        self.data_folder = Path(data_folder)
        self.data_folder.mkdir(parents=True, exist_ok=True)
        self.tournaments = []

        for filepath in self.data_folder.glob("*.json"):
            try:
                with open(filepath) as fp:
                    data = json.load(fp)

                tournament = Tournament.from_dict(data)
                self.tournaments.append(tournament)

            except json.JSONDecodeError:
                print(filepath, "is invalid JSON file.")

    def create(
        self,
        name,
        venue,
        start_date,
        end_date,
        number_of_rounds,
    ):
        """Create and save a new tournament."""
        filename = name.replace(" ", "") + ".json"
        filepath = self.data_folder / filename

        tournament = Tournament(
            name=name,
            venue=venue,
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=number_of_rounds,
        )

        with open(filepath, "w") as fp:
            json.dump(tournament.to_dict(), fp, indent=4)

        self.tournaments.append(tournament)
        return tournament

    def save(self, tournament):
        """Save an existing tournament."""
        filename = tournament.name.replace(" ", "") + ".json"
        filepath = self.data_folder / filename

        with open(filepath, "w") as fp:
            json.dump(tournament.to_dict(), fp, indent=4)
